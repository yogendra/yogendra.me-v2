const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  page.setViewport({ width: 1024, height: 768 });
  await page.goto('https://news.ycombinator.com',
    { waitUntil: 'networkidle' }
  );
  await page.pdf({
    path: 'hn.pdf',
    format: 'A4'
  });
  await browser.close();
})();
