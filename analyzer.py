import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


class Analyzer:
    def __init__(self, records, validations):
        self.records = records
        self.validations = validations
        self.df = None


    def to_dataframe(self):
        rows = []
        for rec, val in zip(self.records, self.validations):
            row = {**rec, **val}
            rows.append(row)
        self.df = pd.DataFrame(rows)
        return self.df


    def save_csv(self, path='jumia_audit_seo.csv'):
        if self.df is None:
            self.to_dataframe()
        self.df.to_csv(path, index=False)
        print(f"CSV saved -> {path}")


    def plot_dashboard(self, out='jumia_dashboard.png'):
        if self.df is None:
            self.to_dataframe()
        fig, axes = plt.subplots(2,2, figsize=(12,10))
        # Distribution des erreurs_count
        axes[0,0].hist(self.df['errors_count'], bins=range(0,7))
        axes[0,0].set_title('Distribution des erreurs par page')
        # Top pages problématiques
        top = self.df.sort_values('errors_count', ascending=False).head(10)
        axes[0,1].barh(top['url'].astype(str), top['errors_count'])
        axes[0,1].set_title('Top pages problématiques')
        # Répartition par type d'erreur (count)
        error_types = ['title','meta_description','h1','images_alt','content','h2']
        counts = {e: (self.df[e]=='ERROR').sum() for e in error_types}
        axes[1,0].bar(counts.keys(), counts.values())
        axes[1,0].set_title('Répartition par type d\'erreur')
        axes[1,0].tick_params(axis='x', rotation=30)
        # Evolution potentielle (simulé): pages corrigées -> errors_count reduced
        # simple scatter: current errors vs desc_words
        axes[1,1].scatter(self.df['desc_words'], self.df['errors_count'])
        axes[1,1].set_xlabel('Words in description')
        axes[1,1].set_ylabel('Errors count')
        axes[1,1].set_title('Corrélation longueur contenu vs erreurs')
        plt.tight_layout()
        plt.savefig(out)
        print(f"Dashboard saved -> {out}")