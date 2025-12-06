import time
import requests
from bs4 import BeautifulSoup

class JumiaScraper:
    def __init__(self, user_agent, delay=2, timeout=10):
        self.headers = {"User-Agent": user_agent}
        self.delay = delay
        self.timeout = timeout


    def fetch(self, url):
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            time.sleep(self.delay)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"[WARN] Failed to fetch {url}: {e}")
            return None


    def parse_product(self, url, html):
            if not html:
                return None
            soup = BeautifulSoup(html, "lxml")
            # Title
            title_tag = soup.find('title')
            title = title_tag.get_text(strip=True) if title_tag else ''
            # Meta description
            meta_desc = ''
            md = soup.find('meta', attrs={'name': 'description'})
            if md and md.get('content'):
                meta_desc = md['content'].strip()
            # Hn
            h1s = [h.get_text(strip=True) for h in soup.find_all('h1')]
            h2s = [h.get_text(strip=True) for h in soup.find_all('h2')]
            # Images
            imgs = soup.find_all('img')
            img_count = len(imgs)
            img_no_alt = sum(1 for i in imgs if not i.get('alt'))
            # Description text: try common selectors used by Jumia
            desc_text = ''
            desc = soup.select_one('#description') or soup.select_one('.product-description') or soup.select_one('.markup')
            if desc:
                desc_text = desc.get_text(separator=' ', strip=True)
            # Price (try common selectors)
            price = ''
            p = soup.select_one(".price") or soup.select_one(".prices") or soup.find(attrs={'data-test': 'product-price'})
            if p:
                price = p.get_text(strip=True)
            # Category breadcrumb
            category = ''
            bc = soup.select('.breadcrumb a') or soup.select('.bds a')
            if bc and len(bc) >= 2:
                category = bc[-1].get_text(strip=True)
            # Word count
            word_count = len(desc_text.split()) if desc_text else 0


            return {
            'url': url,
            'title': title,
            'title_len': len(title),
            'meta_desc': meta_desc,
            'meta_desc_len': len(meta_desc),
            'h1_count': len(h1s),
            'h1s': h1s,
            'h2_count': len(h2s),
            'img_count': img_count,
            'img_no_alt': img_no_alt,
            'desc_words': word_count,
            'price': price,
            'category': category,
            }