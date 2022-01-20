---
title: "Sudo With Touch ID"
date: 2022-01-20T03:43:49Z
draft: false
categories:
  - Productivity
tags:
  - mac
---
Security and convinience are not best of the friends. Good password/pin practices are not convinient (long, different for each system, random). Biometric authentication is somewhat a good compromise.

<!-- more -->

Logging into your machine is a very repeatative task. I do it enough time is a day to be annoyed of long passwords. Additionally, I work a lot on command line so I do find myself running commands with `sudo` a lot. Here is something that help me reduce some annoyance out of these.

You can setup your mac (may be other fingerprint enabled linux system) to use fingerprint based authentication. Most Mac users use this for login purpose. But till today I did not think about useing fingerprint for `sudo` commands. After a quick search I stumbled on the original port on iMore.

_Original Post_
https://www.imore.com/how-use-sudo-your-mac-touch-id

## Alternative Method 1: Via vi

If you are like me, and prefer using Terminal and vi, here is the method

1. Open `/private/etc/pam.d/sudo` in vi

   ```bash
   sudo vi /private/etc/pam.d/sudo
   ```

2. Goto line 2 and start a new line (`2Go` - [2] + [Shift + G] + [o])

3. Paste this line

   ```text
   auth sufficient pam_tid.so
   ```

4. Exit edit mode - [Esc]

5. Save and quit (`:wq!` - [:] +[w] + [q] + [!] + [Enter])

## Alternative Method 2: One Liner

Just run this command

```bash
sudo sed -ie '1 a\
auth       sufficient     pam_tid.so
' /private/etc/pam.d/sudo
```

Or this if you have gnu-sed on your mac

```bash
sudo gsed -i '1 a auth       sufficient     pam_tid.so' /private/etc/pam.d/sudo
```

## But Why

Its very common for enterprises to sync local password with your IDP (Example: Okta).
I use a very long and different (for every system) passwords.
I can get away with the hassle by using a password manager.
My personal favorite is [Safe In Cloud](https://www.safe-in-cloud.com).

So, there is no way I can type it over and over again, every time I lock my machine
or run commands with `sudo`. Additionally, I didnot want to put `NOPASSWD` in
`sudoers` config. I find that risky, as I run all sorts of random scripts on my
machine. So, using TouchID instead of password seems like a safe thing.

I have also used the PIV function of Yubikey for PIN based login, instead of
password. That works too. But since I do find myself in public places with really smart people, giving away PIN is a big possibility. So, biometric lock seems safer.
