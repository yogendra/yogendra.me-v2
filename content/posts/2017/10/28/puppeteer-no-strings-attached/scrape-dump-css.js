const puppeteer = require('puppeteer');

let scrape = async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  await page.setRequestInterceptionEnabled(true);
  page.on('request', r => { r.continue(); })
  page.on('response', r => {
    const url = r.url;
    if (url.endsWith("css")) {
      r.text().then(s => {
        console.log("// Source:" + url);
        console.log(s);
      });
    }
  });
  await page.goto('http://books.toscrape.com/');
  await browser.close();
};
scrape();
