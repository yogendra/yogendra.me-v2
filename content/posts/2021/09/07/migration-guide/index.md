---
title: Migration Guide
---

## From Hexo to Hugo


1. Setup Hugo site with menu and theme etc.
    1. Create site

        ```bash
        hugo new site . --force
        ```

    1. Add theme [link]()

    1. Configure `_config.toml` as per theme specs
        1. Add Menus / Links / Social links
        1. Change author name
1. Page migration
1. Post Migration
1. Copy `<hexo_site>/source/_posts/*` to `<hugo_site>/content/posts`
    1. Delete all the non Markdown files

        ```bash
        cd $SITE_ROOT/content/posts
        find . -type f | grep -v .md\$ --color=never | xargs rm
        ```


1. Copy `<hexo_site>/source/_posts/*` to `<hugo_site>/static`

    1. Delete all the Markdown files

        ```bash
        cd $SITE_ROOT/static
        find . -type f | grep -v .md --color=never | xargs rm
        ```

1. Change `_config.toml`

    1. Permalink

        ```toml
        [permalinks]
        posts = "/:year/:month/:day/:title/"
        ```
    1.

