class SEOValidator:
    def __init__(self):
        pass

    def validate(self, record):
        # returns dict of checks with status 'OK' or 'ERROR' and messages
        r = {}
        # Title: optimal 50-60
        tl = record.get('title_len', 0)
        r['title'] = 'OK' if 50 <= tl <= 60 else 'ERROR'
        r['title_msg'] = f"{tl} chars"
        # Meta description: optimal 150-160? (note in the brief there are two lines; we follow given table)
        mdl = record.get('meta_desc_len', 0)
        r['meta_description'] = 'OK' if 40 <= mdl <= 70 else 'ERROR'
        r['meta_description_msg'] = f"{mdl} chars"
        # H1: exactly 1 and >=120 chars considered ERROR per brief (brief ambiguous: treat absent or >1 as ERROR)
        h1c = record.get('h1_count', 0)
        r['h1'] = 'OK' if h1c == 1 else 'ERROR'
        r['h1_msg'] = f"{h1c} H1(s)"
        # Images ALT: expect 100% images have alt
        imgc = record.get('img_count', 0)
        img_no_alt = record.get('img_no_alt', 0)
        if imgc == 0:
            r['images_alt'] = 'ERROR'
            r['images_alt_msg'] = 'No images'
        else:
            pct_no_alt = img_no_alt / imgc
            r['images_alt'] = 'OK' if pct_no_alt == 0 else 'ERROR'
            r['images_alt_msg'] = f"{img_no_alt}/{imgc} images missing ALT ({pct_no_alt:.0%})"
        # Content length: >200 words
        words = record.get('desc_words', 0)
        r['content'] = 'OK' if words >= 200 else 'ERROR'
        r['content_msg'] = f"{words} words"
        # H2: at least 2
        h2c = record.get('h2_count', 0)
        r['h2'] = 'OK' if h2c >= 2 else 'ERROR'
        r['h2_msg'] = f"{h2c} H2(s)"


        # Aggregate
        r['errors_count'] = sum(1 for v in ['title','meta_description','h1','images_alt','content','h2'] if r[v]=='ERROR')
        return r