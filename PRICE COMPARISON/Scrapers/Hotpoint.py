# hotpoint_side_by_side.py
"""
Prototype scraper for Hotpoint Kenya: Side-by-Side fridges.
- Fetches the category page for Side-by-Side fridges
- Collects product links (one at a time)
- Visits each product page and extracts:
    site, category, product_name, url, price_raw, price_numeric, old_price_raw, old_price_numeric, timestamp
- Appends results into output/hotpoint_side_by_side.csv
Requirements: requests, beautifulsoup4, lxml, pandas (optional)
"""

import requests, re, csv, os
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BASE = "https://hotpoint.co.ke"
CATEGORY_URL = "https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/side-by-side/"
CSV_PATH = "output/hotpoint_side_by_side.csv"
TIMEOUT = 15

def numeric_from_text(txt: str):
    if not txt:
        return None
    cleaned = re.sub(r"[^\d\.,]", "", txt).strip()
    if not cleaned:
        return None
    # Heuristic normalization
    if ',' in cleaned and '.' in cleaned:
        if cleaned.rfind('.') > cleaned.rfind(','):
            cleaned = cleaned.replace(',', '')
        else:
            cleaned = cleaned.replace('.', '').replace(',', '.')
    else:
        if ',' in cleaned and '.' not in cleaned:
            cleaned = cleaned.replace(',', '')
    try:
        return float(cleaned)
    except ValueError:
        return None

def fetch(url):
    s = requests.Session()
    r = s.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r.text

def extract_product_links_from_category(html):
    """
    Simple approach: find '/catalogue/' hrefs in the category HTML.
    Filter duplicates and non-product links.
    """
    urls = set()
    # anchor hrefs
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # product pages on site appear to include '/catalogue/' and an underscore id or slug
        if "/catalogue/" in href and not href.endswith("/category/"):
            full = urljoin(BASE, href)
            # filter out anchor to the category itself
            if "category" in full and full.rstrip("/").endswith("side-by-side"):
                continue
            urls.add(full.split("?")[0])  # strip query
    # also minimal regex fallback
    if not urls:
        for m in re.finditer(r'href="(/catalogue/[^"]+)"', html):
            urls.add(urljoin(BASE, m.group(1)))
    return sorted(urls)

def parse_product_page(html, url):
    soup = BeautifulSoup(html, "lxml")
    # product title heuristics
    title = None
    if soup.select_one("h1"):
        title = soup.select_one("h1").get_text(" ", strip=True)
    else:
        if soup.title:
            title = soup.title.get_text(" ", strip=True)
    # look for price text: page often contains 'KES 349,995  KES 424,995'
    # we'll search for patterns with KES or numbers near keyword 'KES'
    text = soup.get_text(" ", strip=True)
    # find all occurrences like 'KES 349,995' or 'KSh' etc.
    price_matches = re.findall(r"(?:KES|KSh|KES)\s*[0-9\.,]+", text, flags=re.IGNORECASE)
    # deduplicate and preserve order
    seen = []
    for p in price_matches:
        if p not in seen:
            seen.append(p)
    current_raw = None
    old_raw = None
    if seen:
        # On Hotpoint product pages, listing shows current price first, then old price.
        # Example: "KES 349,995  KES 424,995" -> seen likely ['KES 349,995','KES 424,995']
        current_raw = seen[0]
        if len(seen) > 1:
            # choose the second as old price if it is larger
            old_raw = seen[1]
    else:
        # fallback: look for any number with thousands separators
        m = re.search(r"([0-9]{1,3}(?:[,\.][0-9]{3})+(?:\.[0-9]{1,2})?)", text)
        if m:
            current_raw = m.group(1)

    current_num = numeric_from_text(current_raw) if current_raw else None
    old_num = numeric_from_text(old_raw) if old_raw else None

    return {
        "site": "Hotpoint",
        "category": "Fridges/Side-by-Side",
        "product_name": title or url.split("/")[-1],
        "url": url,
        "price_raw": current_raw or "",
        "price_numeric": current_num or "",
        "old_price_raw": old_raw or "",
        "old_price_numeric": old_num or "",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def append_to_csv(records, path=CSV_PATH):
    fieldnames = ["site", "category", "product_name", "url",
                  "price_raw", "price_numeric", "old_price_raw", "old_price_numeric", "timestamp"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_header = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for r in records:
            writer.writerow(r)

def main(limit=None, verbose=True):
    print("Fetching category page:", CATEGORY_URL)
    cat_html = fetch(CATEGORY_URL)
    links = extract_product_links_from_category(cat_html)
    if verbose:
        print(f"Found {len(links)} product links (will process sequentially).")
    results = []
    count = 0
    for link in links:
        if limit and count >= limit:
            break
        try:
            if verbose:
                print(f"[{count+1}] fetching product: {link}")
            p_html = fetch(link)
            rec = parse_product_page(p_html, link)
            if verbose:
                print("  ->", rec["price_raw"], rec["price_numeric"])
            results.append(rec)
            count += 1
        except Exception as e:
            print("Failed to fetch/parse", link, ":", e)
    if results:
        append_to_csv(results)
        print("Saved", len(results), "records to", CSV_PATH)
    else:
        print("No results to save. Check the category URL or HTML structure.")

if __name__ == "__main__":
    # For prototype run only first N products to validate
    main(limit=13)
