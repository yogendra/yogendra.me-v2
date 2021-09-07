const SELECTOR_BOOK_IMAGE = '#default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > div.image_container > a > img';
const puppeteer = require('puppeteer');

let scrapeSite1 = async (browser) => {
  const page = await browser.newPage();
  await page.goto('http://books.toscrape.com/');
  await page.waitFor(1000);
  await page.click(SELECTOR_BOOK_IMAGE);
  await page.waitFor(2000);
  const result = await page.evaluate(() => {
    let title = document.querySelector('h1').innerText;
    let price = document.querySelector('.price_color').innerText;

    return {
      title,
      price
    }

  });
  return result;
}
let scrape = async () => {
  const browser = await puppeteer.launch({ headless: false });
  const result = await Promise.all([
    scrapeSite1(browser),
    scrapeSite1(browser),
    scrapeSite1(browser),
    scrapeSite1(browser),
    scrapeSite1(browser)
  ]);
  await browser.close();
  return result;

};
scrape().then((value) => {
  console.log(value); // Success!
});
