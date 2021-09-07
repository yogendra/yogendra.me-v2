'use strict';
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    page.setViewport({ width: 1024, height: 768 });
    await page.goto('https://www.google.com',
        { waitUntil: 'networkidle' }
    );
    await page.screenshot(
        { path: 'screenshot.png' }
    );
    await browser.close();
})();
