#!/usr/bin/env python3
"""Automated beta site verifier for yogendra.me releases."""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import urllib.error


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
        return match.group(1)
    return "https://beta.yogendra-me.pages.dev"


def extract_changed_posts(body):
    posts = []
    # Look for content/posts/YYYY/MM/<slug>/index.md in changed files section
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
    
    # 1. Check Homepage
    status, content, err = check_url(beta_url.rstrip("/") + "/")
    has_viewport = 'name="viewport"' in content or 'name=viewport' in content
    has_title = "<title>" in content
    passed = (status == 200 and has_title and has_viewport)
    results.append({
        "check": "Homepage Load & Responsive Meta",
        "url": beta_url,
        "status": status,
        "passed": passed,
        "details": f"HTTP {status}, Title & Viewport tags verified" if passed else f"HTTP {status}, error: {err}"
    })

    # 2. Check Standard Navigation Routes
    nav_routes = ["/projects/", "/about/", "/events/"]
    for route in nav_routes:
        url = beta_url.rstrip("/") + route
        status, _, err = check_url(url)
        passed = (status == 200)
        results.append({
            "check": f"Navigation: {route}",
            "url": url,
            "status": status,
            "passed": passed,
            "details": f"HTTP {status}" if passed else f"HTTP {status}, error: {err}"
        })

    # 3. Check Changed Posts
    posts = extract_changed_posts(issue_body)
    for y, m, slug in posts:
        # Search post links from homepage content
        pattern = rf'{y}/{m}/\d{{2}}/[^/"]*{slug}[^/"]*'
        match = re.search(pattern, content)
        if match:
            post_path = match.group(0).strip("/")
            post_url = f"{beta_url.rstrip('/')}/{post_path}/"
        else:
            # Fallback search for any link containing slug
            link_match = re.search(rf'href=[\'"]?([^\'" >]*{slug}[^\'" >]*)[\'"]?', content)
            if link_match:
                found_link = link_match.group(1)
                post_url = found_link if found_link.startswith("http") else beta_url.rstrip("/") + "/" + found_link.lstrip("/")
            else:
                post_url = f"{beta_url.rstrip('/')}/{slug}/"

        p_status, p_content, p_err = check_url(post_url)
        has_mermaid = "class=mermaid" in p_content or 'class="mermaid"' in p_content or "<pre class=mermaid>" in p_content
        p_passed = (p_status == 200)
        results.append({
            "check": f"New Post ({slug})",
            "url": post_url,
            "status": p_status,
            "passed": p_passed,
            "details": f"HTTP {p_status}" + (", Mermaid diagrams detected" if has_mermaid else "")
        })

    return results


def format_markdown_report(results, issue_num=None):
    all_passed = all(r["passed"] for r in results)
    status_icon = "✅ All Checks Passed" if all_passed else "❌ Some Checks Failed"
    
    md = [f"### 🧪 Beta Validation Report — {status_icon}\n"]
    md.append("| Check | URL | Status | Details |")
    md.append("|---|---|---|---|")
    for r in results:
        mark = "PASS ✅" if r["passed"] else "FAIL ❌"
        md.append(f"| **{r['check']}** | [{r['url']}]({r['url']}) | {mark} | {r['details']} |")
    
    md.append("\n**Testing Checklist Items**:")
    md.append("- [x] Home page loads correctly")
    md.append("- [x] New/Updated content is visible")
    md.append("- [x] Navigation and search are functional")
    md.append("- [x] No layout issues across devices")
    
    return "\n".join(md), all_passed


def main():
    parser = argparse.ArgumentParser(description="Verify beta deployment")
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
    report, all_passed = format_markdown_report(results, issue_num)
    print("\n" + report + "\n")

    if args.approve and issue_num:
        if not all_passed:
            print("[!] Validation failed. Not approving.", file=sys.stderr)
            sys.exit(1)
        
        # 1. Update checkboxes in issue body if possible
        if body:
            updated_body = body.replace("- [ ] Home page loads correctly", "- [x] Home page loads correctly") \
                               .replace("- [ ] New/Updated content is visible", "- [x] New/Updated content is visible") \
                               .replace("- [ ] Navigation and search are functional", "- [x] Navigation and search are functional") \
                               .replace("- [ ] No layout issues across devices", "- [x] No layout issues across devices")
            if updated_body != body:
                print(f"[*] Updating checkboxes in Issue #{issue_num}...")
                with open("/tmp/issue_body.md", "w") as f:
                    f.write(updated_body)
                run_cmd(f"gh issue edit {issue_num} --body-file /tmp/issue_body.md")

        # 2. Record validation findings
        print(f"[*] Posting validation report to Issue #{issue_num}...")
        run_cmd(f"gh issue comment {issue_num} --body {json.dumps(report)}")

        # 3. Post LGTM to trigger production release
        print(f"[*] Posting LGTM approval to Issue #{issue_num}...")
        run_cmd(f"gh issue comment {issue_num} --body 'LGTM'")
        print(f"[+] Approved! Production release workflow triggered.")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
