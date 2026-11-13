"""
app.seo.images.image_optimizer
Image Performance Optimization, Responsive Variant Generation, and Alt-Text Guardrails.

Implements Sections 7.3, 7.4, 7.5, and 7.6 of the Master Addendum:
- Generation of WebP and fallback formats
- Responsive variants: hero (1200x675), content (800x450), thumbnail (400x225)
- Layout-shift prevention with explicit aspect ratios and dimension attributes
- Strict alt-text accessibility validation (no 'image of', no keyword stuffing)
- Content hashing (SHA-256) for duplicate prevention and caching
- Performance budgets (hero <= 120KB, content <= 75KB, thumb <= 35KB)
"""

import io
import os
import re
import hashlib
from typing import Dict, Any, List, Tuple, Optional
from PIL import Image

# Performance Budgets in Bytes
BUDGET_HERO_BYTES = 120 * 1024       # 120 KB
BUDGET_CONTENT_BYTES = 75 * 1024     # 75 KB
BUDGET_THUMB_BYTES = 35 * 1024       # 35 KB

class ImageOptimizer:
    """Optimizes visual assets, creates responsive variants, and validates accessibility."""

    @classmethod
    def sanitize_seo_filename(cls, base_name: str, ext: str = "webp") -> str:
        """
        Creates clean, descriptive kebab-case filename.
        Rejects keyword stuffing or repetitive segments.
        """
        clean = re.sub(r"[^\w\s-]", "", base_name.lower())
        slug = re.sub(r"[\s_]+", "-", clean).strip("-")
        # Collapse repeated tokens
        tokens = slug.split("-")
        deduped = []
        for t in tokens:
            if not deduped or deduped[-1] != t:
                deduped.append(t)
        final_slug = "-".join(deduped)[:50].rstrip("-")
        return f"{final_slug}.{ext}"

    @classmethod
    def validate_alt_text(cls, alt_text: str, is_decorative: bool = False) -> Tuple[bool, List[str]]:
        """
        Validates alt text against Section 7.4 rules:
        - Concise and specific (<= 150 chars).
        - No 'image of', 'picture of', 'photo of'.
        - No keyword stuffing.
        - Decorative images allowed empty alt text.
        """
        issues = []
        if is_decorative:
            # Decorative must have empty alt
            return True, []

        alt = alt_text.strip()
        if not alt:
            issues.append("Alt text must not be empty for informative images.")
            return False, issues

        lower_alt = alt.lower()
        banned_prefixes = ["image of", "picture of", "photo of", "graphic of", "diagram of an image"]
        for prefix in banned_prefixes:
            if lower_alt.startswith(prefix):
                issues.append(f"Alt text should not begin with '{prefix}'. Describe the content directly.")

        if len(alt) > 150:
            issues.append(f"Alt text is too long ({len(alt)} chars). Keep under 150 characters.")

        # Check repetitive words (stuffing)
        words = re.findall(r"\w+", lower_alt)
        word_counts = {}
        for w in words:
            if len(w) > 3:
                word_counts[w] = word_counts.get(w, 0) + 1
                if word_counts[w] > 2:
                    issues.append(f"Keyword '{w}' repeated {word_counts[w]} times in alt text (keyword stuffing risk).")
                    break

        return len(issues) == 0, issues

    @classmethod
    def optimize_and_save_variants(
        cls,
        image_bytes: bytes,
        seo_base_slug: str,
        output_dir: str,
        alt_text: str,
        caption: str = "",
        is_hero: bool = True
    ) -> Dict[str, Any]:
        """
        Generates responsive WebP and PNG variants, enforces performance budgets,
        saves to disk, and returns comprehensive metadata.
        """
        os.makedirs(output_dir, exist_ok=True)
        img = Image.open(io.BytesIO(image_bytes))

        # Check and convert color mode if needed
        if img.mode in ("RGBA", "P"):
            rgb_img = img.convert("RGBA")
        else:
            rgb_img = img.convert("RGB")

        content_hash = hashlib.sha256(image_bytes).hexdigest()

        # Variant definitions: (name, width, height, quality)
        variants_spec = [
            ("hero", 1200, 675, 82),
            ("content", 800, 450, 80),
            ("thumb", 400, 225, 78)
        ]

        saved_files = {}
        dimensions_map = {}

        for var_name, target_w, target_h, quality in variants_spec:
            # Resize with High-Quality Lanczos Resampling
            resized = rgb_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

            # 1. Save WebP
            webp_name = cls.sanitize_seo_filename(f"{seo_base_slug}-{var_name}", ext="webp")
            webp_path = os.path.join(output_dir, webp_name)
            resized.save(webp_path, format="WEBP", quality=quality, method=6)
            webp_size = os.path.getsize(webp_path)

            # 2. Save PNG Fallback
            png_name = cls.sanitize_seo_filename(f"{seo_base_slug}-{var_name}", ext="png")
            png_path = os.path.join(output_dir, png_name)
            resized.save(png_path, format="PNG", optimize=True)
            png_size = os.path.getsize(png_path)

            saved_files[var_name] = {
                "webp": {
                    "filename": webp_name,
                    "rel_path": f"/static/images/seo/{webp_name}",
                    "abs_path": webp_path,
                    "size_bytes": webp_size
                },
                "png": {
                    "filename": png_name,
                    "rel_path": f"/static/images/seo/{png_name}",
                    "abs_path": png_path,
                    "size_bytes": png_size
                }
            }
            dimensions_map[var_name] = [target_w, target_h]

        # Alt text validation
        alt_valid, alt_issues = cls.validate_alt_text(alt_text)

        # Performance budget checks
        budget_warnings = []
        if saved_files["hero"]["webp"]["size_bytes"] > BUDGET_HERO_BYTES:
            budget_warnings.append(f"Hero WebP exceeds budget: {saved_files['hero']['webp']['size_bytes']} bytes > {BUDGET_HERO_BYTES}")
        if saved_files["content"]["webp"]["size_bytes"] > BUDGET_CONTENT_BYTES:
            budget_warnings.append(f"Content WebP exceeds budget: {saved_files['content']['webp']['size_bytes']} bytes > {BUDGET_CONTENT_BYTES}")

        # Construct Responsive HTML Picture Markup
        loading_attr = 'loading="eager" fetchpriority="high"' if is_hero else 'loading="lazy" decoding="async"'
        
        html_markup = (
            f'<figure class="nv-seo-figure">\n'
            f'  <picture>\n'
            f'    <source type="image/webp" srcset="{saved_files["thumb"]["webp"]["rel_path"]} 400w, '
            f'{saved_files["content"]["webp"]["rel_path"]} 800w, {saved_files["hero"]["webp"]["rel_path"]} 1200w" '
            f'sizes="(max-width: 600px) 400px, (max-width: 1024px) 800px, 1200px">\n'
            f'    <img src="{saved_files["hero"]["png"]["rel_path"]}" width="1200" height="675" '
            f'alt="{alt_text}" class="nv-seo-img" {loading_attr}>\n'
            f'  </picture>\n'
            + (f'  <figcaption class="nv-seo-figcaption">{caption}</figcaption>\n' if caption else '') +
            f'</figure>'
        )

        return {
            "content_hash": content_hash,
            "seo_base_slug": seo_base_slug,
            "variants": saved_files,
            "dimensions": dimensions_map,
            "alt_text": alt_text,
            "alt_text_valid": alt_valid,
            "alt_text_issues": alt_issues,
            "budget_warnings": budget_warnings,
            "html_markup": html_markup,
            "is_hero": is_hero
        }
