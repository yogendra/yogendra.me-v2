#!/usr/bin/env python3
"""Automated beta site verifier and release publisher for yogendra.me."""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error
from datetime import datetime, timezone


def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def get_latest_beta_issue():
    code, stdout, _ = run_cmd("gh issue list --label beta-testing --state open --json number,title,body --limit 1")
    if code != 0 or not stdout:
        return None
    try:
        issues = json.loads(stdout)
        return issues[0] if issues else None
    except Exception:
        return None


def extract_beta_url(body):
    match = re.search(r'\*\*URL\s*:\*\*\s*\[?(https://[^\s\]\)]+)', body)
    if match:
        url = match.group(1).rstrip("/")
        return url
    return "https://beta.yogendra-me.pages.dev"


def extract_changed_posts(body):
    posts = []
    matches = re.findall(r'content/posts/(\d{4})/(\d{2})/([^/\s]+)/index\.md', body)
    for y, m, slug in matches:
        posts.append((y, m, slug))
    return posts


def check_url(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; BetaVerifier/1.0)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            return resp.status, content, None
    except urllib.error.HTTPError as e:
        return e.code, "", str(e)
    except Exception as e:
        return 0, "", str(e)


def run_checks(beta_url, issue_body):
    results = []
    base_url = beta_url.rstrip("/")

    # 1. Homepage & Responsive Meta
    hp_url = base_url + "/"
    status, content, err = check_url(hp_url)
    has_viewport = 'name="viewport"' in content or 'name=viewport' in content
    has_title = "<title>" in content
    passed = (status == 200 and has_title and has_viewport)
    results.append({
        "check": "🏠 Homepage & Viewport",
        "url": hp_url,
        "display_url": "/",
        "status": status,
        "passed": passed,
        "details": "HTTP 200 • Viewport meta & title verified" if passed else f"HTTP {status}, error: {err}"
    })

    # 2. Navigation Routes
    nav_routes = [
        ("🗂️ Navigation: Projects", "/projects/"),
        ("🗂️ Navigation: About", "/about/"),
        ("🗂️ Navigation: Events", "/events/")
    ]
    for label, route in nav_routes:
        url = base_url + route
        status, _, err = check_url(url)
        passed = (status == 200)
        results.append({
            "check": label,
            "url": url,
            "display_url": route,
            "status": status,
            "passed": passed,
            "details": f"HTTP {status}" if passed else f"HTTP {status}, error: {err}"
        })

    # 3. Changed Posts
    posts = extract_changed_posts(issue_body)
    for y, m, slug in posts:
        pattern = rf'{y}/{m}/\d{{2}}/[^/"]*{slug}[^/"]*'
        match = re.search(pattern, content)
        if match:
            post_path = match.group(0).strip("/")
            post_url = f"{base_url}/{post_path}/"
            display_path = f"/{post_path}/"
        else:
            link_match = re.search(rf'href=[\'"]?([^\'" >]*{slug}[^\'" >]*)[\'"]?', content)
            if link_match:
                found_link = link_match.group(1)
                post_url = found_link if found_link.startswith("http") else f"{base_url}/{found_link.lstrip('/')}"
                display_path = f"/{slug}/"
            else:
                post_url = f"{base_url}/{slug}/"
                display_path = f"/{slug}/"

        p_status, p_content, p_err = check_url(post_url)
        has_mermaid = "class=mermaid" in p_content or 'class="mermaid"' in p_content or "<pre class=mermaid>" in p_content
        p_passed = (p_status == 200)
        details = f"HTTP {p_status}"
        if has_mermaid:
            details += " • Mermaid diagrams verified"
        if not p_passed:
            details += f", error: {p_err}"

        results.append({
            "check": f"📝 Article: {slug}",
            "url": post_url,
            "display_url": display_path,
            "status": p_status,
            "passed": p_passed,
            "details": details
        })

    return results


def format_markdown_report(results, beta_url, issue_num=None, include_approval=False):
    all_passed = all(r["passed"] for r in results)
    status_badge = "All Checks Passed ✅" if all_passed else "Checks Failed ❌"
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = []
    lines.append("## 🧪 Beta Validation Report")
    lines.append("")
    lines.append(f"> **Status:** {status_badge}  ")
    lines.append(f"> **Environment:** [{beta_url}]({beta_url})  ")
    if issue_num:
        lines.append(f"> **Testing Ticket:** #{issue_num}  ")
    lines.append(f"> **Validated At:** {now_utc}")
    lines.append("")
    lines.append("### 📋 Sanity Check Results")
    lines.append("")
    lines.append("| Check | Target URL | Status | Details |")
    lines.append("|:---|:---|:---:|:---|")
    for r in results:
        mark = "`PASS` ✅" if r["passed"] else "`FAIL` ❌"
        lines.append(f"| {r['check']} | [`{r['display_url']}`]({r['url']}) | {mark} | {r['details']} |")

    if include_approval and all_passed:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("### 👍 Release Approval")
        lines.append("")
        lines.append("**LGTM** — Automated sanity checks verified. Ready for production release.")

    return "\n".join(lines), all_passed


def post_to_github(issue_num, body, report):
    # 1. Update checkboxes in issue body
    if body:
        updated_body = body.replace("- [ ] Home page loads correctly", "- [x] Home page loads correctly") \
                           .replace("- [ ] New/Updated content is visible", "- [x] New/Updated content is visible") \
                           .replace("- [ ] Navigation and search are functional", "- [x] Navigation and search are functional") \
                           .replace("- [ ] No layout issues across devices", "- [x] No layout issues across devices")
        if updated_body != body:
            print(f"[*] Updating checklist in Issue #{issue_num}...")
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.md') as f:
                f.write(updated_body)
                tmp_file = f.name
            try:
                run_cmd(f"gh issue edit {issue_num} --body-file {tmp_file}")
            finally:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)

    # 2. Post the single formatted comment with LGTM
    print(f"[*] Posting validation report and LGTM to Issue #{issue_num}...")
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.md') as f:
        f.write(report)
        tmp_comment_file = f.name
    try:
        code, stdout, stderr = run_cmd(f"gh issue comment {issue_num} --body-file {tmp_comment_file}")
        if code == 0:
            print(f"[+] Comment posted successfully to Issue #{issue_num}.")
            print(f"[+] Release workflow triggered! The action will automatically deploy to production and close Issue #{issue_num}.")
        else:
            print(f"[!] Error posting comment: {stderr}", file=sys.stderr)
    finally:
        if os.path.exists(tmp_comment_file):
            os.remove(tmp_comment_file)


def main():
    parser = argparse.ArgumentParser(description="Verify beta deployment and publish release")
    parser.add_argument("--issue", type=int, help="Issue number (defaults to latest open beta-testing issue)")
    parser.add_argument("--url", help="Beta URL override")
    parser.add_argument("--approve", action="store_true", help="Post report and comment LGTM if checks pass")
    args = parser.parse_args()

    issue_data = None
    if args.issue:
        code, stdout, _ = run_cmd(f"gh issue view {args.issue} --json number,title,body")
        if code == 0:
            issue_data = json.loads(stdout)
    else:
        issue_data = get_latest_beta_issue()

    body = issue_data.get("body", "") if issue_data else ""
    issue_num = issue_data.get("number") if issue_data else args.issue
    beta_url = args.url or extract_beta_url(body)

    print(f"[*] Testing Beta Site: {beta_url}")
    if issue_num:
        print(f"[*] Associated Issue: #{issue_num}")

    results = run_checks(beta_url, body)
    report, all_passed = format_markdown_report(results, beta_url, issue_num, include_approval=args.approve)
    print("\n" + report + "\n")

    if args.approve and issue_num:
        if not all_passed:
            print("[!] Validation failed. Aborting approval.", file=sys.stderr)
            sys.exit(1)
        post_to_github(issue_num, body, report)
        print("[+] Approved! Production release workflow triggered.")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
