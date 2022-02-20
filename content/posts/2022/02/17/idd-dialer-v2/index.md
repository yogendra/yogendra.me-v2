---
title: "IDD Dialer V2"
date: 2022-02-17T10:44:29Z
draft: false
thumbnail: app-icon.png
---

I have release IDD Dialer v2. Complete rewrite of v1. It uses the standard Android call management service to dial IDD numbers. Check out the [project page][idd-dialer]

<!-- more -->

![IDD Dialer V2:right](app-icon.png)

## Why IDD Dialer?

I created [IDD Dialer] out of personal need in mid 2010s. How to make it easily to call people using the IDD service.

This generally requires adding few digits in front of the country code in the phone number. Price difference is significant between regular rates and IDD rates. IDD calls cost 10% (or less) of a regular international call.

So, add prefix to each number in phone book is too much of an ask. And when you change your provider, or use another IDD service, then what? So, this had to be automated.

## Why I build an IDD Dialer?

I was using an app in past. But developer stopped maintaining it. It was unlisted from the Play Store. I looked around and found apps that were doing too much. Asking for contact book access, wifi, GPS, etc. Moreover, I didn't want to change my calling pattern. Open the phone app, tap the number in or select from contact book, and press Call. Any extra step (even one) would be, one step too many.

This led to build IDD Dialer (v1). It worked, I had 100+ people using it. My father was my biggest client. He started using it right away.

## What happened then?

Subsequently my (and for most others) calling pattern changed. Most people I know are on messaging platforms so IDD calls kind of faded off.
I stopped maintaining the app I realized that I was working with some really Whatsapp/Viber.

I stopped maintaining (see the theme) the app. And it was banned form Play Store for API violation of something. Apparently, I was using same APIs that malware uses to hurt people.

## Then why V2?

Pandemic has changed our habits. My 'old customers' asked about the app. I was short on time, so didn't pay much attention. But when work situation changed last year, I wanted to give mobile development a try. A quick assessment revealed that my old app was beyond saving. So I ditched it. I also found the new improved way of making this, using [Call Redirection Service]. This looked clean and simple enough. So, back to drawing board.

## What next?

I can't promise what will happen next. But I want to make sure that any serious user/enthusiast has the chance to revive this project if I am unable to. So, I have open-sourced the app. It does not have any automated build/publish or much documentation. Any contributions are also welcome. Project is located in my [github].

[idd dialer]: /projects/idd-v2
[call redirection service]: https://developer.android.com/reference/android/telecom/CallRedirectionService
[github]: https://github.com/yogendra/idd
