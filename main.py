from scraper import JumiaScraper
from validator import SEOValidator
from analyzer import Analyzer
import sys


USER_AGENT = 'JumiaSEO-AuditBot/1.0 (+mailto:your-email@example.com)'


# Replace these sample product URLs with real Jumia product pages (category: Electronique)
SEED_URLS = [
    'https://www.jumia.ma/kraft-line-aspirateur-12-en-1-a-main-3000w-a-fil-technologie-sans-sac-cyclonique-66383548.html',
    'https://www.jumia.ma/siera-refrigerateur-avec-congelateur-en-haut-190l-dp-27-silver-54007434.html',
    'https://www.jumia.ma/schleizer-mini-four-electrique-10-litre-thermostat-230-c-66416510.html',
    'https://www.jumia.ma/taurus-bouilloire-en-inox-sidon-1500-w-18l-acier-inoxydable-2-ans-de-garantie-67262234.html',
    'https://www.jumia.ma/siera-refrigerateur-avec-congelateur-en-haut-190l-dp-27-silver-54007434.html',
    'https://www.jumia.ma/cafetiere-trento-machines-a-cafe-expresso-20barsmoulin-a-cafe-2ans-de-garantie-taurus-mpg1420547.html'
    ]
MAX_PAGES = 100




def main(urls):
    scraper = JumiaScraper(USER_AGENT)
    validator = SEOValidator()
    records = []
    validations = []


    total = min(len(urls), MAX_PAGES)
    for i, url in enumerate(urls[:MAX_PAGES], start=1):
        print(f"Page {i}/{total} -> {url}")
        html = scraper.fetch(url)
        rec = scraper.parse_product(url, html)
        if rec is None:
            # create placeholder with URL so CSV shows it
            rec = {'url': url, 'title':'', 'title_len':0,'meta_desc':'','meta_desc_len':0,'h1_count':0,'h1s':[], 'h2_count':0,'img_count':0,'img_no_alt':0,'desc_words':0,'price':'','category':''}
        val = validator.validate(rec)
        records.append(rec)
        validations.append(val)


    analyzer = Analyzer(records, validations)
    df = analyzer.to_dataframe()
    analyzer.save_csv()
    analyzer.plot_dashboard()


    # executive summary
    total_pages = len(df)
    total_errors = df['errors_count'].sum()
    top_errors = df.sort_values('errors_count', ascending=False).head(5)['url'].tolist()
    summary = (
        f"Audit Jumia (sample {total_pages} pages) : total erreurs détectées = {int(total_errors)}.\n"
        f"Top pages problématiques :\n" + '\n'.join(top_errors)
        )
    with open('jumia_executive_summary.txt','w', encoding='utf-8') as f:
        f.write(summary)
    print('\nExecution terminée. Fichiers: jumia_audit_seo.csv, jumia_dashboard.png, jumia_executive_summary.txt')


if __name__ == '__main__':
    if not SEED_URLS:
        print('ERREUR: Ajoute au moins 1 URL dans SEED_URLS de main.py pour tester (commence par 5).')
        sys.exit(1)
    main(SEED_URLS)