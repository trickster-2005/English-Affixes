"""Build the static site from the Markdown sources in md/.

Usage: python3 build.py   (writes *.html next to this script)
"""
import re, html, unicodedata, pathlib
import markdown
from markdown.extensions.toc import TocExtension

ROOT = pathlib.Path(__file__).parent

PAGES = [
    # slug, md file, short title, description
    ("affixes", "md/affixes.md", "英文詞綴主題大全",
     "依 affixes.org 的 29 個主題整理字首、字尾與組合形式，每個詞綴附常用例字、中文意義、構詞拆解與詞源。"),
    ("roots", "md/roots.md", "英文字根大全",
     "約 110 個最常見的拉丁語與希臘語字根，依意義分成 12 類，附例字、拆解與同根字族。"),
    ("pie", "md/pie.md", "印歐語根與同源字",
     "從原始印歐語追溯英語本土字、拉丁系與希臘系的同源關係，含格林定律等入門說明。"),
]


def gh_slug(value, separator="-"):
    """GitHub-style heading slug (keeps CJK), so links inside the Markdown keep working."""
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value).strip().lower()
    out = []
    for ch in value:
        cat = unicodedata.category(ch)
        if ch in " -_":
            out.append("-" if ch == " " else ch)
        elif cat[0] in ("L", "N") or cat == "Mn":
            out.append(ch)
    return "".join(out)


def count_words(md_text):
    core = re.findall(r"^\| [^|]+? \| /", md_text, re.M)
    inline = re.findall(r"[A-Za-z][A-Za-z' -]* /[^/|\n]+/", md_text)
    return len(core), len(core) + len(inline)


def render(md_text):
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists",
                    TocExtension(slugify=gh_slug, toc_depth="2-3", permalink=False)],
        output_format="html5",
    )
    body = md.convert(md_text)
    return body, md.toc_tokens


def decorate(body):
    # wrap tables for horizontal scrolling on small screens
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    # mark IPA so it can use a font with good phonetic glyphs
    body = re.sub(r"(?<![\w<])/([^/<>\n]{1,80})/(?![\w>])",
                  lambda m: f'<span class="ipa">/{m.group(1)}/</span>'
                  if not re.search(r"[\u3000-\u9fff\uff00-\uffef]", m.group(1)) else m.group(0),
                  body)
    return body


def toc_html(tokens):
    parts = ['<ul class="toc">']
    for t in tokens:  # h1 level holds h2 children
        items = t["children"] if t["level"] == 1 else [t]
        for h2 in items:
            kids = h2.get("children", [])
            name = html.escape(html.unescape(re.sub(r"<[^>]+>", "", h2["name"])))
            if kids:
                parts.append(f'<li class="toc-h2"><details><summary><a href="#{h2["id"]}">{name}</a></summary><ul>')
                for h3 in kids:
                    n3 = html.escape(html.unescape(re.sub(r"<[^>]+>", "", h3["name"])))
                    parts.append(f'<li class="toc-h3"><a href="#{h3["id"]}">{n3}</a></li>')
                parts.append("</ul></details></li>")
            else:
                parts.append(f'<li class="toc-h2"><a href="#{h2["id"]}">{name}</a></li>')
    parts.append("</ul>")
    return "\n".join(parts)


def nav(active):
    links = [("index", "首頁")] + [(s, t) for s, _, t, _ in PAGES]
    out = []
    for s, t in links:
        cls = ' class="active" aria-current="page"' if s == active else ""
        out.append(f'<a href="{s}.html"{cls}>{html.escape(t)}</a>')
    return "".join(out)


HEAD = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="assets/style.css">
</head>
"""


def build_doc(slug, src, title, desc):
    text = (ROOT / src).read_text(encoding="utf-8")
    body, tokens = render(text)
    body = decorate(body)
    page = HEAD.format(title=html.escape(title) + "｜英文構詞學習筆記", desc=html.escape(desc)) + f"""<body class="doc">
<header class="topbar">
  <button class="menu-btn" aria-label="開啟目錄" aria-controls="sidebar" aria-expanded="false">☰ 目錄</button>
  <nav class="sitenav">{nav(slug)}</nav>
</header>
<aside id="sidebar" class="sidebar" aria-label="目錄">
  <div class="sidebar-head">
    <a class="home" href="index.html">← 首頁</a>
    <div class="doc-title">{html.escape(title)}</div>
    <input type="search" class="toc-filter" placeholder="篩選目錄（例如 -tion、spect）" aria-label="篩選目錄">
  </div>
  <nav class="toc-wrap">
{toc_html(tokens)}
  </nav>
</aside>
<main class="content" id="top">
{body}
<footer class="foot">
  <a href="index.html">回首頁</a> · <a href="#top" class="totop">回到頂端 ↑</a>
</footer>
</main>
<div class="scrim" hidden></div>
<script src="assets/site.js"></script>
</body>
</html>
"""
    (ROOT / f"{slug}.html").write_text(page, encoding="utf-8")
    return count_words(text), len([1 for t in tokens for _ in t.get("children", [])])


def build_index(stats):
    cards = []
    for slug, _, title, desc in PAGES:
        core, total = stats[slug]
        cards.append(f"""<a class="card" href="{slug}.html">
  <h3>{html.escape(title)}</h3>
  <p>{html.escape(desc)}</p>
  <span class="meta">約 {round(total, -2):,} 個附音標的單字</span>
</a>""")
    page = HEAD.format(title="英文構詞學習筆記：詞綴・字根・印歐語根",
                       desc="英文詞綴、拉丁希臘字根與印歐語根的中文學習筆記，所有例字附美式 IPA 音標。") + f"""<body class="home-page">
<header class="topbar">
  <nav class="sitenav">{nav("index")}</nav>
</header>
<main class="home-main">
  <section class="hero">
    <h1>英文構詞學習筆記</h1>
    <p class="lede">把英文單字拆成「詞綴＋字根」，再往上追到印歐語的共同祖先。三份筆記由淺入深，所有例字都附上中文意義與<strong>美式 IPA 音標</strong>。</p>
  </section>

  <section class="cards">
    {"".join(cards)}
  </section>

  <section class="prose">
    <h2>建議閱讀順序</h2>
    <ol>
      <li><strong>英文詞綴主題大全</strong>：先認識字首、字尾，學會「拆字」。</li>
      <li><strong>英文字根大全</strong>：掌握拉丁語、希臘語字根，理解單字的意義核心。</li>
      <li><strong>印歐語根與同源字</strong>：看見 <em>foot</em>、<em>pedal</em>、<em>tripod</em> 為何是同一個字，把零散的字串成家族。</li>
    </ol>

    <h2>資料來源</h2>
    <ul>
      <li><strong>主題分類與詞綴清單</strong>：Michael Quinion 的 <em>Dictionary of Affixes</em>（網站 <a href="https://www.affixes.org/" rel="noopener">affixes.org</a>；原書為牛津大學出版社 2002 年出版的 <em>Ologies and Isms</em>）。本站只沿用其主題架構與詞綴名稱，例字、中文解釋與拆解皆為另行撰寫。</li>
      <li><strong>印歐語根</strong>：字根寫法與詞源路徑主要參考 Calvert Watkins, <em>The American Heritage Dictionary of Indo-European Roots</em>（第三版），並以 <a href="https://www.etymonline.com/" rel="noopener">Etymonline</a> 與 <a href="https://en.wiktionary.org/" rel="noopener">Wiktionary</a> 交叉查證。書中或學界仍有爭議的說法，頁面上標註「一說」。</li>
      <li><strong>音標</strong>：以 <a href="https://github.com/cmusphinx/cmudict" rel="noopener">CMU Pronouncing Dictionary</a>（美式發音）自動轉換為 IPA，字典未收的字以 <a href="https://github.com/espeak-ng/espeak-ng" rel="noopener">eSpeak NG</a> 產生，再人工修正複合字、名詞／動詞重音差異與字首讀音。</li>
      <li><strong>詞頻</strong>：補充中高級單字時，以 <a href="https://github.com/rspeer/wordfreq" rel="noopener">wordfreq</a> 的英語詞頻排名挑選常用但不冷僻的字。</li>
    </ul>

    <h2>製作方式</h2>
    <p>內容由 Claude（Anthropic 的 AI 助理）依照使用者的需求逐步整理撰寫，流程如下：</p>
    <ol>
      <li>依 affixes.org 的主題建立架構，為每個詞綴挑選 7–15 個常用例字，寫出中文意義、構詞拆解與一兩句詞源說明。</li>
      <li>以詞頻表篩選候選字，人工剔除「長得像但不同源」的字（例如 <em>database</em> 與字尾 <em>-ase</em> 無關）。</li>
      <li>用程式為所有例字加上美式 IPA 音標，並檢查重音、音節與表格格式。</li>
      <li>以 Python-Markdown 把 Markdown 原稿轉成網頁，自動產生左側目錄。原稿保留在 <code>md/</code> 資料夾。</li>
    </ol>
    <p class="note">AI 整理的內容難免有疏漏，尤其是詞源。若發現錯誤，歡迎到 GitHub 開 issue 指正；重要的詞源請以上列字典為準。</p>
  </section>
</main>
<footer class="foot home-foot">英文構詞學習筆記 · 原稿見 <code>md/</code> 資料夾</footer>
</body>
</html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    stats = {}
    for slug, src, title, desc in PAGES:
        stats[slug], n = build_doc(slug, src, title, desc)
        print(slug, stats[slug], "toc h3:", n)
    build_index(stats)
    print("index.html")
