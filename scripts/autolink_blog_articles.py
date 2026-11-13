import os
import re
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

BLOG_DIR = r"c:\Users\Bhaskr Singh\Downloads\AI Numrology\app\static\blog"

# Canonical internal links dictionary: (Regex pattern, canonical url, link text anchor)
AUTOLINK_RULES = [
    (r"\bLo Shu Grid\b", "/tools/lo-shu-grid/", "Lo Shu Grid"),
    (r"\bLife Path Number\b", "/tools/life-path-calculator/", "Life Path Number"),
    (r"\bChaldean Numerology\b", "/tools/name-numerology/", "Chaldean Numerology"),
    (r"\bName Balancing\b", "/tools/name-balancing/", "Name Balancing"),
    (r"\bName Correction\b", "/tools/name-balancing/", "Name Correction"),
    (r"\bMobile Numerology\b", "/tools/mobile-numerology/", "Mobile Numerology"),
    (r"\bCompatibility Calculator\b", "/tools/compatibility-calculator/", "Compatibility Calculator"),
    (r"\bPersonal Year Calculator\b", "/tools/blessing-years/", "Personal Year Calculator"),
    (r"\bPersonal Year\b", "/tools/blessing-years/", "Personal Year"),
    (r"\bCharm AI\b", "/charm-ai/", "Charm AI"),
    (r"\bReports Catalogue\b", "/reports_catalogue/", "Reports Catalogue"),
    (r"\bSample Reports\b", "/sample_roadmap/", "Sample Reports"),
    (r"\bHTML Sitemap\b", "/sitemap/", "HTML Sitemap"),
]

def autolink_html_content(html: str, filename: str) -> tuple[str, int]:
    # Match the article body section to avoid touching header, footer, meta, or JSON-LD
    body_match = re.search(r"(<article[\s\S]*?</article>)", html, re.IGNORECASE)
    if not body_match:
        # Fallback to main or blog-content if <article> not found
        body_match = re.search(r"(<div class=\"blog-content\"[\s\S]*?</div>\s*</div>)", html, re.IGNORECASE)
        if not body_match:
            return html, 0
    
    article_block = body_match.group(1)
    modified_article = article_block
    total_links_added = 0
    
    for pattern, url, anchor in AUTOLINK_RULES:
        # Don't link to the current file's topic if redundant
        if filename.replace(".html", "") in url.lower():
            continue
            
        # Check if URL is already linked in the article block
        if f'href="{url}"' in modified_article or f"href='{url}'" in modified_article:
            continue
            
        # Function to replace only the first occurrence outside existing <a> tags and headings
        def replace_first_unlinked(match_obj):
            nonlocal total_links_added
            # Check context: are we inside an <a> tag or <h1-h6>?
            start_pos = match_obj.start()
            # Look backwards from start_pos to find last open tag
            preceding_text = modified_article[:start_pos]
            last_a_open = preceding_text.rfind("<a ")
            last_a_close = preceding_text.rfind("</a>")
            if last_a_open > last_a_close:
                # Inside an existing anchor tag! Do not replace
                return match_obj.group(0)
            
            # Check if inside heading
            for h in range(1, 7):
                last_h_open = preceding_text.rfind(f"<h{h}")
                last_h_close = preceding_text.rfind(f"</h{h}>")
                if last_h_open > last_h_close:
                    return match_obj.group(0)
                    
            total_links_added += 1
            matched_text = match_obj.group(0)
            return f'<a href="{url}" class="nv-autolink" title="Explore {anchor} on Numeros Vision">{matched_text}</a>'

        # Replace only the first occurrence in the article
        regex = re.compile(pattern, re.IGNORECASE)
        
        # Split by existing <a>...</a> tags so we never touch text inside them
        parts = re.split(r"(<a\b[^>]*>.*?</a>)", modified_article, flags=re.DOTALL | re.IGNORECASE)
        replaced = False
        new_parts = []
        for part in parts:
            if part.lower().startswith("<a") and part.lower().endswith("</a>"):
                new_parts.append(part)
            elif not replaced:
                new_part, count = regex.subn(replace_first_unlinked, part, count=1)
                new_parts.append(new_part)
                if count > 0:
                    replaced = True
            else:
                new_parts.append(part)
        modified_article = "".join(new_parts)

    new_html = html.replace(article_block, modified_article)
    return new_html, total_links_added

def run():
    files = [f for f in os.listdir(BLOG_DIR) if f.endswith(".html") and f != "index.html"]
    print(f"Scanning {len(files)} blog articles for contextual autolinking...")
    
    total_modified = 0
    total_links = 0
    for filename in sorted(files):
        filepath = os.path.join(BLOG_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        updated_content, links_added = autolink_html_content(content, filename)
        if links_added > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"  [✓] {filename}: added {links_added} contextual autolinks")
            total_modified += 1
            total_links += links_added
        else:
            print(f"  [-] {filename}: already fully linked")
            
    print(f"\nDone! Modified {total_modified}/{len(files)} articles. Total internal autolinks injected: {total_links}")

if __name__ == "__main__":
    run()
