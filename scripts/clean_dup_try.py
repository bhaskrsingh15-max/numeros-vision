with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

dup = """      } catch (e) {
        console.warn('Hero sync notification:', e);
      }
    }
      } catch (e) {
        console.warn('Hero sync notification:', e);
      }
    }"""

fixed = """      } catch (e) {
        console.warn('Hero sync notification:', e);
      }
    }"""

if dup in text:
    text = text.replace(dup, fixed, 1)
    with open('app/static/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Cleaned duplicate try/catch in index.html")
else:
    print("Exact dup not found, checking whitespace variants...")
    import re
    p = re.compile(r'(\}\s*catch\s*\(e\)\s*\{\s*console\.warn\(\'Hero sync notification:\',\s*e\);\s*\}\s*\}\s*)\}\s*catch\s*\(e\)\s*\{\s*console\.warn\(\'Hero sync notification:\',\s*e\);\s*\}\s*\}')
    if p.search(text):
        text = p.sub(r'\1', text, count=1)
        with open('app/static/index.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Regex cleaned duplicate try/catch in index.html")
    else:
        print("Regex also did not match")
