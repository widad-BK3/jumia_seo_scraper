# Jumia SEO Scraper (Data-driven SEO Audit)


## Installation
1. Crée un environnement virtuel Python 3.8+:
python -m venv venv
source venv/bin/activate # ou venv\Scripts\activate
2. Installer les dépendances:
pip install -r requirements.txt


## Usage
1. Modifier la liste `SEED_URLS` dans `main.py` avec 5 URLs pour tester.
2. Lancer:
python main.py


Résultats:
- `jumia_audit_seo.csv`
- `jumia_dashboard.png`
- `jumia_executive_summary.txt`


Notes:
- Respectez robots.txt et les conditions d'utilisation.
- Le code attend au maximum 100 URLs (défini dans main.py).