with open('app/static/charm_ai.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update formatMarkdown
old_format_md = """    function formatMarkdown(str) {
      if (!str) return '';
      let s = str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      s = s.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color:#8B6914;">$1</strong>');
      s = s.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
      const lines = s.split('\\n');
      let out = [];
      let inList = false;
      for (let line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('•') || trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          const itemContent = trimmed.replace(/^[•\\-\\*]\\s*/, '');
          if (!inList) {
            out.push('<ul style="margin:8px 0; padding-left:20px; list-style-type:disc; color:#523E28; font-size:0.90rem; line-height:1.6;">');
            inList = true;
          }
          out.push(`<li style="margin-bottom:4px;">${itemContent}</li>`);
        } else {
          if (inList) {
            out.push('</ul>');
            inList = false;
          }
          if (trimmed) {
            out.push(`<p style="margin-bottom:10px; line-height:1.65; color:#523E28;">${trimmed}</p>`);
          }
        }
      }
      if (inList) out.push('</ul>');
      return out.join('');
    }"""

new_format_md = """    function formatMarkdown(str) {
      if (!str) return '';
      // Strip any accidental raw HTML tags from engine or LLM
      let s = str
        .replace(/<div[\\s\\S]*?<\\/div>/gi, '')
        .replace(/<a[\\s\\S]*?<\\/a>/gi, '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

      // Format markdown headings
      s = s.replace(/^###\\s*(.*$)/gim, '<h4 style="font-family:\'Cormorant Garamond\',serif; font-size:1.25rem; font-weight:700; color:#8B6914; margin:16px 0 8px;">$1</h4>');
      s = s.replace(/^##\\s*(.*$)/gim, '<h3 style="font-family:\'Cormorant Garamond\',serif; font-size:1.35rem; font-weight:700; color:#523E28; margin:18px 0 10px;">$1</h3>');
      s = s.replace(/^#\\s*(.*$)/gim, '<h2 style="font-family:\'Cormorant Garamond\',serif; font-size:1.5rem; font-weight:700; color:#523E28; margin:20px 0 12px;">$1</h2>');

      // Bold and italics
      s = s.replace(/\\*\\*\\*(.*?)\\*\\*\\*/g, '<strong style="color:#8B6914;"><em>$1</em></strong>');
      s = s.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color:#8B6914;">$1</strong>');
      s = s.replace(/\\*(.*?)\\*/g, '<em>$1</em>');

      const lines = s.split('\\n');
      let out = [];
      let inList = false;

      for (let line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('•') || trimmed.startsWith('\\u2022') || trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          const itemContent = trimmed.replace(/^([•\\u2022\\-\\*]\\s*)/, '');
          if (!inList) {
            out.push('<ul style="margin:8px 0 12px; padding-left:22px; list-style-type:disc; color:#523E28; font-size:0.92rem; line-height:1.68;">');
            inList = true;
          }
          out.push(`<li style="margin-bottom:6px;">${itemContent}</li>`);
        } else {
          if (inList) {
            out.push('</ul>');
            inList = false;
          }
          if (trimmed.startsWith('<h') || trimmed.startsWith('</h')) {
            out.push(trimmed);
          } else if (trimmed) {
            out.push(`<p style="margin-bottom:10px; line-height:1.7; color:#523E28;">${trimmed}</p>`);
          }
        }
      }
      if (inList) out.push('</ul>');
      return out.join('');
    }"""

if old_format_md in html:
    html = html.replace(old_format_md, new_format_md)
    print("Replaced formatMarkdown successfully!")
else:
    print("Notice: old formatMarkdown exact string not matched, checking with normalized whitespace...")
    import re
    html = re.sub(r'function formatMarkdown\(str\)\s*\{[\s\S]*?return out\.join\(\'\'\);\s*\}', new_format_md.strip(), html)
    print("Replaced formatMarkdown via regex!")

with open('app/static/charm_ai.html', 'w', encoding='utf-8') as f:
    f.write(html)
