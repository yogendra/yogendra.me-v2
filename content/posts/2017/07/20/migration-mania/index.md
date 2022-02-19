---
title: "Migration Mania"
date: 2017-07-20 22:13:49
draft: false
categories:
  - Technology
  - DevOps
tags:
  - "web"
  - "blog"
  - "cd/ci"
  - "git"
thumbnail: html-js-css.png
---

I am embarking on this new journey to use [Static Site Generator](https://www.staticgen.com/).

<!--more-->

![type-icon-right](html-js-css.png)

So far, I have managed to setup:

- [Hugo](https://gohugo.io) base project
- [GitHub repository](https://www.github.com/yogendra/yogendra.me)
- [Travis CI](https://travis-ci.org/yogendra/yogendra.me) based build and deploy

I have a shared hosting service (for many years now) so I want to use that to host my site. This added some (small) challenges in my journey. I will share my experience, so far and in future, in this post. One thing that I really like is how natural I find this. After all I am a _Programmer_.

## How can you use my work?

You can fork my repository (link above) and follow the simple instruction on the `README.md` to start using. I will use my own repository for instructions here.

Before you start, get these softwares and setup correctly

- [Hugo](https://gohugo.io/getting-started/installing/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Travis CI Client](https://github.com/travis-ci/travis.rb#installation)
- [Firebase CLI](https://firebase.google.com/docs/cli/)
- [autoenv](https://github.com/kennethreitz/autoenv) _(Optional but Highly Recommended)_

I use [autoenv](https://github.com/kennethreitz/autoenv) to manager per-project shell environment. It executes `.env` file in the directory when you `cd` into it. This is optional but very useful.

## Clone and Change

```shell
git clone git@github.com:yogendra/yogendra.me.git
cd yogendra.me
git submodule update --init --recursive
```

Here are some changes that you should consider:

- You should probably delete `site/content/*` and `site/static/*` (or not).
- You **should** change information in `config.toml`, consider changing:
  - googleAnalytics
  - baseUrl
  - title
  - author
  - description
  - githubUsername
  - \[menu.icon\] links

## Run and Test

You can run development server using following command

```shell
hugo server -s site -wDEF -b http://localhost:1313 --navigateToChanged --cleanDestinationDir -d dev
```

What the hell! Read instruction in `hugo server --help` to understand what each of those switches mean. We are asking hugo to:

- -w : watch for changes
- -D : build draft
- -E : build expired pages
- -F : build future date page,
- -b : set base url to `http://localhost:1313`
- --navigateToChanged : navigate browser to updated file
- --cleanDestinationDir: Delete all the files that might be there in destination dir
- -d : Destination dir to store files into

You can add your own content using command like

```shell
cd site
hugo new post/<post-name.md>
```

When you want to prepare actual deployment, you can use following command

```shell
hugo -s site -d public
```

## Configure Firebase

I recommend using [Firebase](https://firebase.google.com). Read the [hosting guide](https://firebase.google.com/docs/hosting/) and get familiar with the concept and commands.

First, login to firebase from cli. This needs to be done only once. If you have already done this for any other prohect, you can skip this step

```shell
$ firebase login
```

Now you need to initialize firebase setting for the project. This will run as a wizard. Follow onscreen instructions.

```shell
$ firebase init hosting
```

You may test your firebase configuration by deploying changes directly from your machine

```shell
$ firebase deploy
```

**Important:** _Choose "N" for "Configure as a single-page app (rewrite all urls to /index.html)?". Also, don't overwrite files under `public/`_

## Configure Travis CI

_Based on [Travis CI - Firebase Deployment](https://docs.travis-ci.com/user/deployment/firebase/)_

Create a new project on Travis CI website website. Login to Travis CI via `travis` command.

```shell
$ travis login
```

Get a deployment token from firebase, for using in travis ci build environment.

```shell
$ firebase login:ci
```

This should generate a string that looks like `1/AD7sdasdasdKJA824OvEFc1c89Xz2ilBlaBlaBla`.
Use following command to encrypt this string and use in `.travis.yml`.

```shell
$ travis encrypt "1/AD7sdasdasdKJA824OvEFc1c89Xz2ilBlaBlaBla" --add
SUPER-SECRET-ENCRYPTED-VALUE
```

Replace `deploy` key in `.travis.yml` with folowing text. Remember to change `SUPER-SECRET-ENCRYPTED-VALUE` with text from last command output

```yaml
deploy:
  provider: firebase
  token:
    secure: "SUPER-SECRET-ENCRYPTED-VALUE"
  on:
    branch: master
```

That's it! Don't forget to checkin your changes.
