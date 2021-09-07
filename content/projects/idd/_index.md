---
title: IDD Dialer
date: 2018-04-14 12:49:18
thumbnailImage: app-icon.png
---

# [Direct APK Download Here][download]

![type-icon-right](app-icon.png "IDD")
IDD Dialer is a simple utility application for Android. It simplifies usage of IDD service, Calling Cards, etc.

Most of the times, using these services requires you to either put custom numbers in your address book or copy-paste-edit phone numbers. Example, if you want to dial `+911234567890`, and idd service needs you to put `018`. So, you are expected to dial `018911234567890`.

You could store the number as expected by the service provider, in addressbook. But when you change service, well good luck updating all the numbers. Other option is to copy-paste numbers on dialer screen and prefix with whatever you need to.

![Number Replacement][number-replace-image]

This is _unacceptable_ in 2018. So, I made this app to just replace the phone number on-the-fly. No more storing cutom prefixed numbers.
This application replaces `+` in the your outgoing number with another prefix.

# How does it work?

![type-icon-right](settings.png "IDD Settings")

This app replaces `+` in the outgoing calls with the **prefix** that you supplied in the settings. It will skip this replacement for any number that starts with your local ISD code. So if you are in Singapore and using StarHub IDD service, you may have following settings (See image):

> - Enabled: Yes
> - Prefix: 018
> - Local ISD Code: 65

# What Next?

I plan to opensource this project. Also, I plan to improve this application with better controls, wizards, etc. But I don't have a timeline for this. But keep your comments and feedback coming.

Post your feedback here in comments.

# [Direct APK Download Here][download]

[Terms & Conditions][tnc] | [Privacy Policy][privacy-policy]

[download]: https://drive.google.com/file/d/15IO80cdZgxTb1HsYO51fbB701CWSXE_K/view
[number-replace-image]: number-replace-image.png
[icon]: app-icon.png
[example-starhub]: example-starhub.png
[privacy-policy]: /projects/idd/privacy_policy.html
[tnc]: /projects/idd/terms_and_conditions.html
