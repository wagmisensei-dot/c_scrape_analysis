import fetch from "node-fetch";
import * as cheerio from "cheerio";
import dotenv from "dotenv";
dotenv.config();


async function scrapeChrono24(reference) {
  const url = `https://www.chrono24.com/search/index.htm?query=${encodeURIComponent(reference)}`;

  console.log("Scraping", url);

  const res = await fetch(url, {
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36",
    },
  });

  const html = await res.text();
  const $ = cheerio.load(html);

  const prices = [];

  $(".search-result-item").each((i, el) => {
    const price = $(el).find(".text-bold").text().trim();
    const title = $(el).find(".headline-3").text().trim();
    prices.push({ title, price });
  });

  console.log("Found listings:", prices);
}

scrapeChrono24("Rolex 1601");
