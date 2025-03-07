import asyncio
from playwright.async_api import async_playwright
import json
from urllib.parse import urljoin, urlparse

async def extract_product_links(page, domain, url):
    """Extracts category/product pages from the given domain"""
    print(f"Visiting: {url}")
    
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(3000)

    links = await page.locator("a").evaluate_all("elements => elements.map(el => el.href)")
    
    links = [urljoin(url, link) for link in links if link and "javascript:void(0)" not in link]

    filtered_urls = []
    for url in links:
        parsed_url = urlparse(url)
        
        if parsed_url.netloc not in {domain, f"www.{domain}.com"}:
            continue

        if parsed_url.query or parsed_url.fragment:
            continue

        path_segments = parsed_url.path.strip("/").split("/")
        
        if len(path_segments) == 1 and path_segments[0]:
            filtered_urls.append(url)
    
    unwanted_paths = {
        "/contactus", "/giftcard", "/myntrainsider", "/my/orders", "/sitemap",
        "/aboutus", "/help", "/terms", "/privacy", "/returns", "/shipping"
    }
    category_pages = [url for url in filtered_urls if urlparse(url).path not in unwanted_paths]

    print(f"Extracted category pages length: {len(category_pages)}")
    return category_pages

async def extract_buy_links(page, domain, url):
    """Extracts product buy links from category pages"""
    print(f"Extracting buy links from: {url}")
    
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(3000)

    links = await page.locator("a").evaluate_all("elements => elements.map(el => el.href)")
    links = [urljoin(url, link) for link in links if link and "javascript:void(0)" not in link]

    buy_links = [link for link in links if "buy" in link.lower()]

    return buy_links

async def save_results(name, results):
    """Saves the extracted links into a JSON file"""
    with open(f"{name}.json", "w") as f:
        json.dump(results, f, indent=4)

async def crawl_domains(domains):
    """Main crawling function"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        results = {}

        for domain in domains:
            print(f"\nCrawling: {domain}")
            page = await browser.new_page()

            try:
                category_pages = await extract_product_links(page, domain, f"https://www.{domain}.com/")
                results[domain] = {}

                for category_url in category_pages[:5]:
                    print(f"\nExtracting from category: {category_url}")
                    buy_links = await extract_buy_links(page, domain, category_url)
                    results[domain][category_url] = buy_links

            except Exception as e:
                print(f"Error crawling {domain}: {e}")

            await page.close()
        
        await browser.close()
        await save_results("filtered_buy_links", results)
        print("\n Crawling completed!")

    return results

domains = ["myntra"]
product_urls = asyncio.run(crawl_domains(domains))