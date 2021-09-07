---
layout: post
title: Puppeteer - No Strings Attached
date: 2017-10-28 23:52:08
category:
  - Talk
tags:
  - gdg
  - testing
thumbnail: logo.png
---

I am a Co-Manager for [Google Developer Group - Singapore][24] ([FB][25]). And today was our annual [GDG-SG DevFest 2017][15] event. Apart from being an organizer, I was also a speaker. I gave a short talk on [Puppeteer][1]. This post is (almost) a transcript of my speech today. Slides can be found [here][17]

<!--more-->

![GDG-SG][gdg-collage]

![][slides-001]

## Overview

[Puppeteer][1] is a [Node JS][2] API published by Chrome team. It is an API to control Chrome browser via [DevTools Protocol][4]. Puppeteer was released shortly after the Chrome 59. This version of Chrome brought us [Headless Chrome][3]. It requires [Node JS][2] version 6.4+. I would recommend using version 7.5+, so you can use `async/await` feature from [ES2017][5].

### Features

It connects with browser using [Chrome DevTools Protocol][6]. Hence, it works with [Chrome][13]/[Chromium][12] only, and not with other browsers.

Puppeteer can work in headless environment. This makes it a good candidate tool for unit/acceptance/functional tests in a CI environment. It can simulate keyboard, mouse and touch events. So, if you are building a responsive application for desktop and mobile devices, you can use Puppeteer for testing. It also brings the PDF and screenshot capabilities out of box. You can capture PDF and screenshot for whole or part of the page.

Puppeteer allows you to trap console output and web requests. If you have a requirement to "flag" any console output, you may put traps in your test cases for it. If you want to mock a back-end server request (json/xml), you can intercept those request and provide mock response for it.

It has API for performance tracing. So you can use it for recording page load performance and trace any bottlenecks. One of the biggest advantage, of having latest Chromium or Chrome being driven by the API, is [Blink Engine][7]. It is a shiny new layout engine from Chromium project and replaces [WebKit][8] engine. I am not aware about any short comings with WebKit, but I am guessing that Chromium has outgrown WebKit zone.

### Use cases

I have found Puppeteer most useful in browser automation. I have done multiple personal projects for browser automation (I am a lazy guy). Puppeteer offers a simple clean API interface for this, and that in itself is a great selling point. You can use if for frontend testing, e2e testing, etc.

Server side rendering (SSR) is another great use case for this API. You can easily render your single page applications' view on server side and send them to client. This is very useful when you have deep nested view and deep-linking facility in your application.

If you have written apps in Spring Web MVC to produce PDF, you would be aware of maintenance nightmares. You had to maintain each View (HTML and PDF) separately. I eventually started using PhantomJS on server side and reused HTML view to generate PDF with it. You get absolutely great looking PDF out of box with Puppeteer. Its identical to what you get in the PDF print in regular Chrome.

Web crawling and scraping is one of the easiest things to do with Puppeteer. You can easily navigate to pages, retrieve details and process them in a nested fashion.

## Puppeteer And Others

Browser automation and e2e testing is a very busy area. Lots of options for frameworks, APIs, Tools and Platforms. As a result, there are many competing tools in this space. Puppeteer emerges as a good replacement for a few of them.

### PhantomJS

[PhantomJS][9] was one of the first tools that I used for headless browsing. I used it for generating server side PDF. However, recent events force us to move on to other tooling. Primary maintainer of PhantomJS, Vitaly, has stepped down. In his departing note, he expressed excitement about the new Headless Chrome experience. That's fair! And I agree with his point of view.

### The 'Selenium' Empire

[Selenium][10] is probably the most used browser automation and testing tool for frontend. It is the "Automation Emperor" for me. It has the most comprehensive coverage in terms of languages and target browsers. It has language binding for Java, Node, Ruby, Python, etc. You name it and it has language binding for it. And on the other side, it has web driver for every browser or browser like system. It has drivers for all browsers, Chrome, Safari, Firefox, Opera, etc. It also has drivers for like ok PhantomJS and Appium.

They have managed to achieve the most unimaginable feat. They have got these giants on a common footing. It enjoy a lot of love and support from community, including myself. So, why am I even talking about puppeteer.

That brings me nicely into the next piece. Architecture-wise Selenium and Puppeteer are slightly different. Selenium achieve browser automation though an intermediate proxy, the [WebDriver][11]. WebDriver is a per-browser component implementing remote control capabilities. It exposes an restful API interface. A language binding uses these APIs to interact and control browser.

![][slides-012]

Puppeteer takes a leaner approach to this and taps straight into the DevTools protocol of the browser. This makes it possible to easily keep keep with browser features and automation API, in sync.

## Demo

Lets go through some samples to understand the development with Puppeteer.

### Installation

Puppeteer is a Node JS API. Its published as an NPM package. You can install it in you project with simple `npm install`

```shell
$ npm i --save-dev puppeteer
> puppeteer@0.12.0 install /Users/user/.nvm/project1/node_modules/puppeteer
> node install.js

Downloading Chromium r508693 - 72.6 Mb [====================] 100% 0.0s
Chromium downloaded to /Users/monkey/project1/lib/node_modules/puppeteer/.local-chromium/mac-508693
+ puppeteer@0.12.0
added 42 packages in 223.254s
```

Notice how it has also downloaded Chromium. This ensures that it has a compatible version of chromium always. You can skip Chromium download and run it with your own installation of Chrome / Chromium. You can skip download by setting an `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD` environment variable. And you can provide executable path to alternate Chrome or Chromium in you code.

### Screenshot

Taking a screenshot in an automation tool is like a "Hello World!" thing.

```javascript screenshot.js
"use strict";
const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://www.google.com", { waitUntil: "networkidle" });
  await page.screenshot({ path: "screenshot.png" });
  await browser.close();
})();
```

[Source](screenshot.js)

If you are not familiar with `async/await`, I would recommend reading [this][5]. Most methods in Puppeteer API return a Promise. `await` ensures that you wait for a promise to resolve or reject before proceeding to next instruction. Line **5**, invokes `launch()`, which launches Chromium. You can specify launch options as an object parameter, like `puppeteer.launch({headless: false})`. See all the options in [documentation][14] page. Line **6** creates a new tab with `newPage()` method. `goto()` method on line **7** navigates page to a URL. `waitUntil` ensures that page and its and related assets (js/images/css) are loaded, before promise is resolved.

On line **10-12**, `screenshot()` method captures an image of output and stores it in `screenshot.png`. This looks plain and simple. And that is what made me like this API. It is clean and simple.

You can run this with following command

```shell
$ node screenshot.js
$
```

This produces `screenshot.png` in the current directory.

![][screenshot.png]

### PDF

This is the single biggest reason for me to use Puppeteer. PDF generation is a breeze! Heres how you can do it.

```javascript pdf.js
"use strict";
const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://news.ycombinator.com", { waitUntil: "networkidle" });
  await page.pdf({
    path: "hn.pdf",
    format: "A4",
  });
  await browser.close();
})();
```

[Source](pdf.js)

We will now generate PDF from hacker news landing page. Code is not very different from what we saw in screenshot example. Line **20-23** generates PDF instead of screenshot. And thats it. You can specify paper size for the PDF in the optional argument. Look at [documentation][16] for more options. Its output would be identical to "Print PDF" function of Chrome or Chromium. It uses print media css.

![][hn]
[Link to actual extracted PDF][hn-pdf]

### Web Scraping

I have used Puppeteer most for this. In my work environment I have need for integration via web pages. There are case where I don't have access to a data API for integration. Puppeteer can make it possible for you to expose a "web" site as a JSON api.

```javascript scrape.js
`use strict`;

const SELECTOR_BOOK_IMAGE =
  "#default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > div.image_container > a > img";
const puppeteer = require("puppeteer");

let scrape = async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto("http://books.toscrape.com/");
  await page.waitFor(1000);
  await page.click(SELECTOR_BOOK_IMAGE);
  await page.waitFor(2000);
  const result = await page.evaluate(() => {
    let title = document.querySelector("h1").innerText;
    let price = document.querySelector(".price_color").innerText;
    return {
      title,
      price,
    };
  });
  await browser.close();
  return result;
};
scrape().then((value) => {
  console.log(value); // Success!
});
```

[Source](scrape.js)

We first goto "books.toscrape.com" and click on first image (line 11) on the page. First image on page is referred via `SELECTOR_BOOK_IMAGE` css selector. This triggers a navigation to a details page.

On line 13, a function is dispatched for evaluation on the DOM. This function goes through DOM element (`h1` and element with class `price_color` ) and extracts text (`innerText`).

You can simply run this with `node` command.

```shell
$ node scrape.js
{ title: 'A Light in the Attic', price: '£51.77' }
```

You will see browser window for this example. This is because of line **7**, where I have opted for `{headless: false}`. This is to show scraping in action.

**Disclaimer:** Be very careful what you scrape. You can/will run into legal and licensing issues very quickly.

## Final Thoughts

Puppeteer is a very promising project. In a very short period (< 6 month) it has gotten great support from community. I have read many posts covering this API. I am confident about the future of this project. I am looking forward to a growing and thriving community for this.

It is a very good replacement for PhantomJS. However, my key concern as at the moment are:

- Google Cloud Function (GCF) does not support Node JS 6.4+. So, you have to use cloud VM or Container service to run this in cloud. Hopefully next version of LTS will be 8+, and will bring all the goodness of async/await into the mix
- Lack of support for non-Chrome based browser could be discouraging for many developers. We all want to keep tool/library dependency low and single codebase for testing. If you project demands multi-browser testing, you will end up in a fractured state. Better stick with WebDriver/Selenium. May be WebDriver will adopt some part of Puppeteer API.

I also found the e2e testing support very _unclean_. Its possible, workable, but now readable. I would like to see a very clean integration with likes of cucumber, mocha, chai, etc.

### Links

Here are some links that I used for preparing my presentation.

- [Puppeteer Home][1]
- [Try Puppeteer in Browser][18]
- [Puppetron][19] ([Demo][20])
- [Getting Started with Headless Chrome - Eric Bidelman][21]
- [Getting Started with Puppeteer and Headless Chrome Web Scraping - Emad Ehsan][22]
- [A Guide to Automating and Scraping - Brandon Morelli][23]

### Questions

**Can I use Puppeteer for extracting data and localizing?**
Technically, Yes. You can setup data pipeline to crawl and extract data. You case store it in database or some other persistent store. You can use a workflow to review, edit and publish. Be very careful about licensing. Don't crawl/scrape data without author's consent.

**Can you run multiple tabs simultaneously?**
Yes. You can use `newPage()` method to create multiple tabs. And for each tab you can have a different execution code. I have tried it with 2 tabs. Here is a code sample for the last example (scraping) that does same thing but five times, concurrently.

```javascript scrape-multi.js
const SELECTOR_BOOK_IMAGE =
  "#default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > div.image_container > a > img";
const puppeteer = require("puppeteer");

let scrapeSite = async (browser) => {
  const page = await browser.newPage();
  await page.goto("http://books.toscrape.com/");
  await page.waitFor(1000);
  await page.click(SELECTOR_BOOK_IMAGE);
  await page.waitFor(2000);
  const result = await page.evaluate(() => {
    let title = document.querySelector("h1").innerText;
    let price = document.querySelector(".price_color").innerText;

    return {
      title,
      price,
    };
  });
  return result;
};
let scrape = async () => {
  const browser = await puppeteer.launch({ headless: false });
  const result = await Promise.all([
    scrapeSite(browser),
    scrapeSite(browser),
    scrapeSite(browser),
    scrapeSite(browser),
    scrapeSite(browser),
  ]);
  await browser.close();
  return result;
};
scrape().then((value) => {
  console.log(value); // Success!
});
```

[Source](scrape-multi.js)

**Can I extract CSS from the pages with this?**
I have not tried it, but as you can evaluate any valid javascript code using API, you should be able to extract that.

Below is a code that dumps each css being accessed by the page.

```javascript scrape-dump-css.js
const puppeteer = require("puppeteer");

let scrape = async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  await page.setRequestInterceptionEnabled(true);
  page.on("request", (r) => {
    r.continue();
  });
  page.on("response", (r) => {
    const url = r.url;
    if (url.endsWith("css")) {
      r.text().then((s) => {
        console.log("// Source:" + url);
        console.log(s);
      });
    }
  });
  await page.goto("http://books.toscrape.com/");
  await browser.close();
};
scrape();
```

[Source](scrape-dump-css.js)

## Thanks

My father ([Shri. Noratan Rampuria][26]) has always been very supportive of my life and career choices. And he showed his support once again. He was there for my talk and had looked happy. Thanks papa 🙏!
![][special-thanks]

Many ex and current colleagues were also at the event and showed their support. Thanks folks🤝!

Thanks to [Bharathi][27] and [Hari][28] (GDG Mangement team) for the opportunity to speak. Well, it was more like _push_ to speak 😀. [Manikantan K][29], [Hui Yi][30], [Dirk Primbs][31] and David from Google Developer Relations for supporting GDG-SG - "Thank you". And [Jason Zaman][32] for incepting the idea "Want to be at a conference? Just speak on something".

[1]: https://github.com/GoogleChrome/puppeteer
[2]: https://www.nodejs.org
[3]: https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md
[4]: https://github.com/ChromeDevTools/devtools-protocol
[5]: https://medium.com/@tmvvr/ecmascript-async-await-to-the-rescue-fc379ff89146
[6]: https://chromedevtools.github.io/devtools-protocol/
[7]: https://www.chromium.org/Blink
[8]: https://webkit.org
[9]: https://phantomjs.org
[10]: https://www.seleniumhq.org/
[11]: https://www.seleniumhq.org/projects/webdriver/
[12]: https://www.chromium.org
[13]: https://www.google.com/chrome
[14]: https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md#puppeteerlaunchoptions
[15]: https://www.gdg-sg.org/2017/10/gdg-devfest-2017.html
[16]: https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md#pagepdfoptions
[17]: https://drive.google.com/open?id=0B6Mr-G5qbPLPT0JCTWl0N0w5M2s
[18]: https://try-puppeteer.appspot.com/
[19]: https://puppetron.now.sh/
[20]: https://www.youtube.com/watch?v=n4sRp3qe_1Y
[21]: https://developers.google.com/web/updates/2017/04/headless-chrome
[22]: https://medium.com/@e_mad_ehsan/getting-started-with-puppeteer-and-chrome-headless-for-web-scrapping-6bf5979dee3e
[23]: https://codeburst.io/a-guide-to-automating-scraping-the-web-with-javascript-chrome-puppeteer-node-js-b18efb9e9921
[24]: https://www.gdg-sg.org
[25]: https://www.facebook.com/gdgsgorg
[26]: https://twitter.com/nmrampuria
[27]: https://www.facebook.com/bharathi.subramanian.73
[28]: https://www.facebook.com/hari1prasath
[29]: https://www.facebook.com/manikantan.krish
[30]: https://twitter.com/heliumlif
[31]: https://twitter.com/dirkprimbs
[32]: https://twitter.com/perfinion
[gdg-collage]: gdg-collage.jpg
[slides-001]: slides.001.jpeg
[slides-012]: slides.012.jpeg
[screenshot.png]: screenshot.png
[hn]: hn.jpg
[special-thanks]: special-thanks.jpg
[hn-pdf]: hn.pdf
[puppeteer-logo]: logo.png
