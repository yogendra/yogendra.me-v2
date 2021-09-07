---
title: ' yogendra/trusty32 - Announcing my first vagrant box'
tags:
  - devops
  - vagrant
  - devops
id: 277
categories:
  - Technology
date: 2014-12-11 23:08:49
thumbnailImage: vagrant-ubuntu.png
---

I have finally released my first vagrant box. Its been a long time coming, but it's here now. How to get it?

<!--more-->

Create a new vagrant project with:

``` shell
vagrant init yogendra/trusty32
```

_Or_

1. Create/update your Vagrantfile as

  ``` ruby Vagrantfile
  # -*- mode: ruby -*-
  # vi: set ft=ruby :

  # Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
  VAGRANTFILE_API_VERSION = "2"

  Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "yogendra/trusty32"
  end

  ```

1. Run this

  ``` shell
  vagrant up --provider vmware_fusion
  ```

That's it.

If you are new to Vagrant, read [this tutorial](https://docs.vagrantup.com/v2/getting-started/)to get started
