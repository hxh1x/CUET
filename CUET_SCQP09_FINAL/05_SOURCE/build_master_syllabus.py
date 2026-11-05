# -*- coding: utf-8 -*-
"""Build the SCQP09 learning-ordered syllabus PDF from the classified PYQ bank."""
import csv
import html
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taxonomy_data import ROWS

try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except (ImportError, OSError):
    HAS_WEASYPRINT = False

BASE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(BASE, ".."))
OUT = os.path.join(PKG, "01_MASTER_SYLLABUS")
CSV_PATH = os.path.join(PKG, "02_QUESTION_BANK", "SCQP09_Question_Bank_2024-2026.csv")
YEARS = ["2024", "2025", "2026"]

# ---------------------------------------------------------------------------
# Data preparation
# ---------------------------------------------------------------------------
questions = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
key_counts = Counter((q["subject"], q["topic"], q["subtopic"]) for q in questions)

for row in ROWS:
    c = Counter()
    for k in row["keys"]:
        for q in questions:
            if (q["subject"], q["topic"], q["subtopic"]) == k:
                c[q["year"]] += 1
    row["counts"] = {y: c[y] for y in YEARS}
    row["total"] = sum(row["counts"].values())
    if row.get("priority_override"):
        row["priority"] = row["priority_override"]
    elif row["total"] >= 5:
        row["priority"] = "P0"
    elif row["total"] >= 3:
        row["priority"] = "P1"
    elif row["total"] >= 1:
        row["priority"] = "P2"
    else:
        row["priority"] = "P3"

# Validate coverage and question bank counts
assert len(questions) == 225, f"Expected exactly 225 questions, got {len(questions)}"
for y in YEARS:
    y_count = sum(1 for q in questions if q.get("year") == y)
    assert y_count == 75, f"Expected 75 questions for year {y}, got {y_count}"

used = Counter()
for row in ROWS:
    for k in row["keys"]:
        used[k] += 1
missing = [k for k in key_counts if used[k] == 0]
dupes = [k for k, n in used.items() if n > 1]
assert not missing, f"Unmapped keys: {missing}"
assert not dupes, f"Duplicate keys: {dupes}"
assert sum(row["total"] for row in ROWS) == len(questions) == 225

SUBJECTS = [
    ("Mathematics", "Mathematics", "M"),
    ("Thinking & Decision Making", "Thinking & Decision Making", "T"),
    ("Digital Fundamentals", "Digital Fundamentals", "G"),
    ("Data Structures & Algorithms", "Data Structures & Algorithms", "D"),
    ("Operating Systems", "Operating Systems", "O"),
    ("Low-yield official CS", "Low-yield official topics", "R"),
]

subj_counts = defaultdict(Counter)
for q in questions:
    subj_counts[q["subject"]][q["year"]] += 1
# merge rare into low-yield
for y in YEARS:
    subj_counts["Low-yield official CS"][y] += subj_counts["Rare / Legacy CS"][y]
    subj_counts["Rare / Legacy CS"][y] = 0

def esc(s):
    return html.escape(str(s), quote=False)

def pct(n, d):
    return f"{100*n/d:.1f}%"

def priority_class(p):
    return {"P0": "p0", "P1": "p1", "P2": "p2", "P3": "p3"}.get(p, "p3")

def count_pills(row):
    parts = []
    for y in YEARS:
        n = row["counts"][y]
        cls = "zero" if n == 0 else ""
        parts.append(f'<span class="ypill {cls}"><b>{y[2:]}</b> {n}</span>')
    return "".join(parts)

def bullets(text):
    items = [x.strip() for x in text.split("|") if x.strip()]
    return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"

def subject_total(s):
    return sum(subj_counts[s][y] for y in YEARS)

# Subject-level module and priority counts for the Section 3 overview
glance_rows = []
for s, label, prefix in SUBJECTS:
    rs = [r for r in ROWS if r["subject"] == s]
    qn = sum(r["total"] for r in rs)
    mod_totals = Counter()
    for r in rs:
        mod_totals[r["module"]] += r["total"]
    top_mod, top_n = mod_totals.most_common(1)[0]
    glance_rows.append(
        f"<tr><td><b>{esc(label)}</b></td><td class='c'>{len(rs)}</td>"
        f"<td class='c'><b>{qn}</b></td><td class='c'>{pct(qn, len(questions))}</td>"
        f"<td>{esc(top_mod)} <span class='muted'>({top_n})</span></td></tr>"
    )
glance_rows.append(
    f"<tr><td><b>Total</b></td><td class='c'><b>{len(ROWS)}</b></td>"
    f"<td class='c'><b>{sum(r['total'] for r in ROWS)}</b></td><td class='c'><b>100%</b></td>"
    f"<td>Calculus (21)</td></tr>"
)

# Build subject sections
section_numbers = {}
card_html = {}
for s, label, prefix in SUBJECTS:
    rows = [r for r in ROWS if r["subject"] == s]
    cards = []
    for r in rows:
        example = ""
        if r.get("example"):
            example = f'<div class="pyq"><span class="pyqlabel">PYQ signal</span> {esc(r["example"])}</div>'
        cards.append(f"""
        <div class="card {priority_class(r['priority'])}">
          <div class="cardhead">
            <div class="cardtitle"><span class="code">{r['id']}</span> {esc(r['title'])}</div>
            <div class="cardbadges">
              <span class="prio {priority_class(r['priority'])}">{r['priority']}</span>
              {count_pills(r)}
            </div>
          </div>
          <div class="cardmodule">{esc(r['module'])}</div>
          <div class="cardbody">
            <div class="learn"><div class="minilabel">What to learn</div>{bullets(r['learn'])}</div>
            <div class="asked"><div class="minilabel">How it is asked</div>{bullets(r['asked'])}</div>
          </div>
          {example}
        </div>""")
    card_html[s] = "\n".join(cards)

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = r"""
@page {
  size: A4;
  margin: 18mm 15mm 17mm 15mm;
  @top-left {
    content: "SCQP09 · Complete Learning-Ordered Syllabus";
    font-family: Lato, "DejaVu Sans", sans-serif;
    font-size: 7.5pt;
    color: #7b8794;
    letter-spacing: .04em;
  }
  @top-right {
    content: "2024–2026 PYQ edition";
    font-family: Lato, "DejaVu Sans", sans-serif;
    font-size: 7.5pt;
    color: #7b8794;
  }
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-family: Lato, "DejaVu Sans", sans-serif;
    font-size: 8pt;
    color: #7b8794;
  }
}
@page cover {
  margin: 0;
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-center { content: none; }
}
@page toc {
  @top-left { content: none; }
  @top-right { content: none; }
}
html { font-size: 9.2pt; }
body {
  font-family: Lato, "DejaVu Sans", sans-serif;
  color: #1c2733;
  line-height: 1.42;
  margin: 0;
}
h1, h2, h3, h4 { font-family: Lato, "DejaVu Sans", sans-serif; color: #12355b; margin: 0; }
h1 { font-size: 20pt; line-height: 1.15; margin: 0 0 5mm 0; }
h2 { font-size: 15pt; line-height: 1.2; margin: 0 0 3mm 0; padding-bottom: 2mm; border-bottom: 1.2pt solid #d9e2ec; }
h3 { font-size: 11.5pt; margin: 6mm 0 2.5mm 0; color: #1f5f7a; }
h4 { font-size: 9.8pt; margin: 4mm 0 1.5mm 0; color: #12355b; }
p { margin: 0 0 2.2mm 0; }
ul { margin: 0; padding-left: 4.2mm; }
li { margin: 0 0 0.8mm 0; }
strong { color: #12355b; }
.small { font-size: 8.2pt; color: #52606d; }
.muted { color: #61707f; }
.center { text-align: center; }
.pagebreak { break-before: page; }
.avoid { break-inside: avoid; }

/* Cover */
.cover {
  page: cover;
  height: 297mm;
  width: 210mm;
  background: #12355b;
  color: #ffffff;
  position: relative;
  overflow: hidden;
}
.cover .band {
  position: absolute; top: 0; left: 0; width: 210mm; height: 9mm;
  background: #e09f3e;
}
.cover .inner { position: absolute; top: 32mm; left: 20mm; width: 170mm; }
.cover .kicker { font-size: 9pt; letter-spacing: .22em; text-transform: uppercase; color: #9fd3dc; margin-bottom: 5mm; }
.cover h1 { color: #ffffff; font-size: 38pt; line-height: 1.02; margin-bottom: 5mm; letter-spacing: -0.01em; }
.cover .sub { font-size: 15pt; line-height: 1.3; color: #d7e7ee; margin-bottom: 9mm; font-weight: 300; }
.cover .rule { width: 40mm; height: 1.4mm; background: #e09f3e; margin: 0 0 8mm 0; }
.cover .evidence { display: flex; gap: 4mm; margin: 0 0 12mm 0; }
.cover .evbox { border: 0.5pt solid #4d7898; border-radius: 2mm; padding: 4mm 5mm; min-width: 36mm; }
.cover .evbox .n { font-size: 22pt; font-weight: 700; color: #ffffff; line-height: 1; }
.cover .evbox .l { font-size: 7.5pt; color: #a9c6d6; letter-spacing: .06em; text-transform: uppercase; margin-top: 1.5mm; }
.cover .bottom { position: absolute; bottom: 22mm; left: 20mm; width: 170mm; font-size: 8.5pt; color: #a9c6d6; }
.cover .bottom b { color: #ffffff; }
.cover .edition { position: absolute; top: 22mm; right: 20mm; font-size: 8pt; letter-spacing: .14em; color: #9fd3dc; text-transform: uppercase; }

/* TOC */
.toc { page: toc; }
.toc h2 { border: none; margin-bottom: 6mm; }
.toc a { color: #1c2733; text-decoration: none; }
.toc .l1 { font-size: 10.5pt; font-weight: 700; margin: 4.5mm 0 1.2mm 0; }
.toc .l2 { font-size: 9pt; margin: 1.2mm 0 1.2mm 7mm; color: #3d4c5a; }
.toc a::after { content: leader('.') target-counter(attr(href), page); color: #7b8794; }

/* Headings and sections */
.section { break-before: page; }
.section-intro { font-size: 10pt; color: #3d4c5a; margin-bottom: 5mm; }
.kicker { font-size: 7.8pt; letter-spacing: .18em; text-transform: uppercase; color: #1f7a8c; font-weight: 700; margin-bottom: 2mm; }

/* Boxes */
.grid2 { display: flex; gap: 5mm; }
.grid2 > div { flex: 1; }
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }
.grid3 > .box { margin: 0; }
.box { background: #f4f7fa; border: 0.5pt solid #d9e2ec; border-radius: 2mm; padding: 4mm 4.5mm; margin: 0 0 4mm 0; }
.box h4 { margin-top: 0; }
.box.accent { border-left: 3pt solid #1f7a8c; background: #f0f8fa; }
.box.warn { border-left: 3pt solid #e09f3e; background: #fdf8ee; }
.box.dark { background: #12355b; color: #ffffff; border: none; }
.box.dark h4, .box.dark strong { color: #ffffff; }
.box.dark p, .box.dark li { color: #d7e7ee; }
.box.dark ol { font-size: 8.1pt; line-height: 1.32; }
.box.dark ol li { margin-bottom: 0.6mm; }
.statrow { display: flex; gap: 3mm; margin: 0 0 5mm 0; }
.stat { flex: 1; background: #ffffff; border: 0.6pt solid #d9e2ec; border-top: 2.5pt solid #1f7a8c; border-radius: 1.5mm; padding: 3.5mm 4mm; }
.stat .n { font-size: 18pt; font-weight: 700; color: #12355b; line-height: 1; }
.stat .l { font-size: 7.6pt; text-transform: uppercase; letter-spacing: .07em; color: #61707f; margin-top: 1.5mm; }

/* Tables */
table { width: 100%; border-collapse: collapse; margin: 0 0 4.5mm 0; font-size: 8.4pt; }
thead { display: table-header-group; }
th { background: #12355b; color: #ffffff; text-align: left; padding: 2.2mm 2mm; font-weight: 700; font-size: 7.8pt; letter-spacing: .02em; }
td { padding: 1.9mm 2mm; border-bottom: 0.5pt solid #d9e2ec; vertical-align: top; }
tr { break-inside: avoid; }
tbody tr:nth-child(even) { background: #f7f9fb; }
td.num, th.num { text-align: right; white-space: nowrap; }
td.c, th.c { text-align: center; }
.table-note { font-size: 7.6pt; color: #61707f; margin-top: -3mm; margin-bottom: 4mm; }

/* Bars */
.bars { margin: 0 0 5mm 0; }
.bar { display: flex; align-items: center; margin: 0 0 2.2mm 0; font-size: 8.3pt; }
.bar .name { width: 40mm; color: #3d4c5a; }
.bar .track { flex: 1; height: 5.5mm; background: #edf1f5; border-radius: 1mm; overflow: hidden; margin: 0 2mm; }
.bar .fill { height: 5.5mm; background: #1f7a8c; border-radius: 1mm; }
.bar .val { width: 13mm; text-align: right; font-weight: 700; color: #12355b; }

/* Cards */
.card { border: 0.6pt solid #d9e2ec; border-left: 3pt solid #9fb3c8; border-radius: 1.5mm; padding: 3.2mm 3.8mm 3mm 3.8mm; margin: 0 0 3.2mm 0; break-inside: avoid; background: #ffffff; }
.card.p0 { border-left-color: #c0392b; }
.card.p1 { border-left-color: #e09f3e; }
.card.p2 { border-left-color: #1f7a8c; }
.card.p3 { border-left-color: #9fb3c8; }
.cardhead { display: flex; justify-content: space-between; align-items: flex-start; gap: 3mm; }
.cardtitle { font-size: 10pt; font-weight: 700; color: #12355b; line-height: 1.25; }
.code { display: inline-block; font-size: 7.2pt; font-weight: 700; color: #ffffff; background: #1f7a8c; border-radius: 1mm; padding: 0.7mm 1.4mm; margin-right: 1.2mm; vertical-align: 1px; letter-spacing: .03em; }
.cardmodule { font-size: 7.2pt; text-transform: uppercase; letter-spacing: .09em; color: #7b8794; margin: 1mm 0 2.2mm 0; }
.cardbadges { display: flex; gap: 1.2mm; flex-shrink: 0; align-items: center; }
.prio { display: inline-block; font-size: 6.8pt; font-weight: 700; color: #fff; border-radius: 1mm; padding: 0.8mm 1.4mm; letter-spacing: .05em; }
.prio.p0 { background: #c0392b; }
.prio.p1 { background: #d68910; }
.prio.p2 { background: #1f7a8c; }
.prio.p3 { background: #7b8794; }
.ypill { display: inline-block; font-size: 6.6pt; color: #3d4c5a; background: #edf1f5; border-radius: 1mm; padding: 0.8mm 1.2mm; white-space: nowrap; }
.ypill b { color: #12355b; font-weight: 700; }
.ypill.zero { opacity: .48; }
.cardbody { display: flex; gap: 4.5mm; }
.cardbody > div { flex: 1; }
.minilabel { font-size: 6.8pt; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: #1f7a8c; margin-bottom: 1mm; }
.cardbody ul { font-size: 7.9pt; padding-left: 3.6mm; line-height: 1.35; }
.cardbody li { margin-bottom: 0.5mm; }
.pyq { margin-top: 2.2mm; padding-top: 1.8mm; border-top: 0.5pt dashed #cfd8e3; font-size: 7.6pt; color: #52606d; }
.pyqlabel { font-size: 6.5pt; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #c0392b; margin-right: 1.5mm; }

/* Archetypes */
.arche { border: 0.6pt solid #d9e2ec; border-radius: 2mm; padding: 3.5mm 4mm; margin: 0 0 3mm 0; break-inside: avoid; }
.arche .top { display: flex; justify-content: space-between; gap: 3mm; margin-bottom: 1.5mm; }
.arche .name { font-weight: 700; color: #12355b; font-size: 9.6pt; }
.arche .tag { font-size: 7pt; background: #edf1f5; color: #52606d; border-radius: 1mm; padding: 0.8mm 1.5mm; white-space: nowrap; }
.arche .q { font-style: italic; color: #3d4c5a; margin: 1.2mm 0; }
.arche .do { font-size: 8.2pt; color: #1c2733; }

/* Stage path */
.path { margin: 0 0 6mm 0; }
.stage { display: flex; gap: 3mm; align-items: stretch; margin-bottom: 2.2mm; }
.stage .num { width: 13mm; background: #12355b; color: #fff; font-weight: 700; font-size: 12pt; border-radius: 1.5mm; display: flex; align-items: center; justify-content: center; }
.stage .body { flex: 1; background: #f4f7fa; border: 0.5pt solid #d9e2ec; border-radius: 1.5mm; padding: 2.6mm 3.5mm; }
.stage .body b { font-size: 9.6pt; }
.stage .body span { font-size: 8.2pt; color: #52606d; }

/* Plan */
.weeks td:first-child { font-weight: 700; color: #1f5f7a; white-space: nowrap; }
.checklist li { list-style: none; margin-left: -4mm; }
.checklist li::before { content: "☐"; color: #1f7a8c; font-weight: 700; margin-right: 2mm; }

/* Formula sheets */
.formula h3 { margin-top: 5mm; }
.formula table { font-size: 8.2pt; }
.formula td:first-child { width: 38%; font-weight: 700; color: #12355b; }
.symbol { font-family: "DejaVu Serif", "DejaVu Sans", serif; }

/* Two-column blocks */
.cols2 { column-count: 2; column-gap: 7mm; }
.cols2 .box { break-inside: avoid; }

/* Tighten Appendix B so the closing summary fits on the final page */
#sB h3 { margin-top: 4mm; }
#sB .section-intro { margin-bottom: 4mm; }
"""

# ---------------------------------------------------------------------------
# Content helpers
# ---------------------------------------------------------------------------
def subject_header(s, label, blurb, stats, target, nature):
    return f"""
    <h2 id="sec-{s.replace(' ', '-').lower()}">{label}</h2>
    <p class="section-intro">{blurb}</p>
    <div class="statrow">
      <div class="stat"><div class="n">{subject_total(s)}</div><div class="l">questions · 2024–26</div></div>
      <div class="stat"><div class="n">{stats}</div><div class="l">year-wise split</div></div>
      <div class="stat"><div class="n">{target}</div><div class="l">target time / score</div></div>
    </div>
    <div class="box accent"><strong>Nature of the block.</strong> {nature}</div>
    """

# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------
parts = []
parts.append(f"""<!doctype html>
<html><head><meta charset="utf-8"><title>SCQP09 Complete Learning-Ordered Syllabus</title>
<style>{CSS}</style></head><body>""")

# ---------------- COVER ----------------
parts.append("""
<div class="cover">
  <div class="band"></div>
  <div class="edition">Edition 2026–27</div>
  <div class="inner">
    <div class="kicker">CUET-PG · Paper Code SCQP09</div>
    <h1>Complete<br>Learning-Ordered<br>Syllabus</h1>
    <div class="rule"></div>
    <div class="sub">Computer Science &amp; Information Technology<br>
    Subject → Topic → Subtopic → What to learn → How it is asked</div>
    <div class="evidence">
      <div class="evbox"><div class="n">225</div><div class="l">actual questions decoded</div></div>
      <div class="evbox"><div class="n">3</div><div class="l">papers · 2024, 2025, 2026</div></div>
      <div class="evbox"><div class="n">92</div><div class="l">study modules</div></div>
    </div>
    <div style="font-size:10pt;color:#d7e7ee;max-width:145mm;line-height:1.5;">
      A preparation map built from the actual paper — not a generic syllabus.
      Every module below is tied to real questions, real weightage and the exact
      way the examiner asks it.
    </div>
  </div>
  <div class="bottom">
    <b>Evidence base:</b> SCQP09 papers of 19 Mar 2024 (Shift 3), 27 Mar 2025 (Shift 2), 11 Mar 2026 (Shift 2),
    plus the current NTA SCQP09 syllabus. &nbsp;·&nbsp; Prepared 1 November 2026.
  </div>
</div>
""")

# ---------------- TOC ----------------
toc_items = [
    ("s1", "1. The exam in numbers", "Pattern, weightage and what changed"),
    ("s2", "2. The learning order", "Why this sequence, and the 16-week path"),
    ("s3", "3. The master syllabus", "92 modules, in the order you should learn them"),
]
for s, label, prefix in SUBJECTS:
    toc_items.append((f"sec-{s.replace(' ', '-').lower()}", f"3.{SUBJECTS.index((s,label,prefix))+1} {label}", ""))
toc_items += [
    ("s4", "4. How questions are asked", "Ten archetypes, wording decoder and traps"),
    ("s5", "5. Weightage and trends", "The 20 highest-yield topics"),
    ("s6", "6. High-yield vs low-yield", "What to master, what to cover once, what to drop"),
    ("s7", "7. The 16-week plan", "Week-by-week schedule and a 6-week crash plan"),
    ("s8", "8. Exam-day strategy", "Three passes, time boxing and guessing"),
    ("sA", "Appendix A. Formula and fact sheet", "Rapid revision"),
    ("sB", "Appendix B. Method and sources", "How this document was built"),
]

toc_html = ['<div class="toc"><div class="kicker">Contents</div><h2>What is inside</h2>']
for anchor, title, sub in toc_items:
    if sub:
        toc_html.append(f'<div class="l1"><a href="#{anchor}">{title}</a></div><div class="l2">{sub}</div>')
    else:
        toc_html.append(f'<div class="l2"><a href="#{anchor}">{title}</a></div>')
toc_html.append("</div>")
parts.append("\n".join(toc_html))

# ---------------- SECTION 1: EXAM IN NUMBERS ----------------
parts.append("""
<div class="section" id="s1">
  <div class="kicker">Section 1</div>
  <h2>The exam in numbers</h2>
  <p class="section-intro">Only three papers matter for this edition: 2024, 2025 and 2026. The paper changed shape in 2024 (all-domain, 75 questions), then changed speed in 2025 (90 minutes). The table below is the factual base for every recommendation in this document.</p>

  <table>
    <thead><tr><th>Paper</th><th>Date &amp; shift</th><th class="c">Questions</th><th class="c">Marks</th><th class="c">Duration</th><th class="c">Marking</th><th class="c">Part A?</th></tr></thead>
    <tbody>
      <tr><td><b>2024</b></td><td>19 March 2024 · Shift 3</td><td class="c">75</td><td class="c">300</td><td class="c">105 min</td><td class="c">+4 / −1</td><td class="c">No</td></tr>
      <tr><td><b>2025</b></td><td>27 March 2025 · Shift 2</td><td class="c">75</td><td class="c">300</td><td class="c">90 min</td><td class="c">+4 / −1</td><td class="c">No</td></tr>
      <tr><td><b>2026</b></td><td>11 March 2026 · Shift 2</td><td class="c">75</td><td class="c">300</td><td class="c">90 min</td><td class="c">+4 / −1</td><td class="c">No</td></tr>
    </tbody>
  </table>
  <div class="table-note">Source: first page of each official NTA question paper (duration and total marks are printed on the paper). All questions are compulsory, subject-specific and bilingual.</div>

  <h3>Subject weightage: the only three-year pattern that matters</h3>
  <table>
    <thead><tr><th>Subject block</th><th class="c">2024</th><th class="c">2025</th><th class="c">2026</th><th class="c">Total / 225</th><th class="c">Average share</th><th>What it means</th></tr></thead>
    <tbody>
      <tr><td><b>Mathematics</b></td><td class="c">30</td><td class="c">20</td><td class="c">20</td><td class="c">70</td><td class="c">31.1%</td><td>Largest block; 2024 was an outlier.</td></tr>
      <tr><td><b>Thinking &amp; Decision Making</b></td><td class="c">15</td><td class="c">15</td><td class="c">20</td><td class="c">50</td><td class="c">22.2%</td><td>Growing; fastest scoring block.</td></tr>
      <tr><td><b>Data Structures &amp; Algorithms</b></td><td class="c">10</td><td class="c">13</td><td class="c">12</td><td class="c">35</td><td class="c">15.6%</td><td>Stable core.</td></tr>
      <tr><td><b>Digital Fundamentals</b></td><td class="c">10</td><td class="c">13</td><td class="c">12</td><td class="c">35</td><td class="c">15.6%</td><td>Stable and highly learnable.</td></tr>
      <tr><td><b>Operating Systems</b></td><td class="c">9</td><td class="c">14</td><td class="c">11</td><td class="c">34</td><td class="c">15.1%</td><td>Volatile but always present.</td></tr>
      <tr><td><b>DBMS / other CS</b></td><td class="c">1</td><td class="c">0</td><td class="c">0</td><td class="c">1</td><td class="c">0.4%</td><td>One conflict-serializability question.</td></tr>
    </tbody>
  </table>

  <div class="bars">
    <div class="bar"><div class="name">Mathematics</div><div class="track"><div class="fill" style="width:100%"></div></div><div class="val">31.1%</div></div>
    <div class="bar"><div class="name">Thinking &amp; Decision</div><div class="track"><div class="fill" style="width:71.4%"></div></div><div class="val">22.2%</div></div>
    <div class="bar"><div class="name">DSA</div><div class="track"><div class="fill" style="width:50.2%"></div></div><div class="val">15.6%</div></div>
    <div class="bar"><div class="name">Digital</div><div class="track"><div class="fill" style="width:50.2%"></div></div><div class="val">15.6%</div></div>
    <div class="bar"><div class="name">Operating Systems</div><div class="track"><div class="fill" style="width:48.6%"></div></div><div class="val">15.1%</div></div>
    <div class="bar"><div class="name">DBMS / other</div><div class="track"><div class="fill" style="width:1.3%"></div></div><div class="val">0.4%</div></div>
  </div>

  <div class="box dark">
    <h4>Five conclusions that drive the whole plan</h4>
    <ol style="margin:0;padding-left:5mm;">
      <li><b>Mathematics is the largest single block.</b> 70 of 225 questions. Even in the leaner 2025/2026 papers it is 20 questions — more than any other subject.</li>
      <li><b>TDM is the best return on time.</b> 50 questions, no prerequisites, and 2026 raised it to 20. It is the block where speed can be trained fastest.</li>
      <li><b>The CS core is remarkably stable.</b> DSA + Digital + OS = 104 questions (46.2%), and each paper kept the three between 29 and 40 questions.</li>
      <li><b>2026 changed the format, not the syllabus.</b> Match-the-list, arrange-the-order and assertion–reason questions increased sharply. Content remained the same five blocks.</li>
      <li><b>The clock is now the main enemy.</b> 90 minutes for 75 questions = 72 seconds per question. The paper rewards recognition and elimination, not long derivations.</li>
    </ol>
  </div>

  <h3>What changed across the three papers</h3>
  <table>
    <thead><tr><th>Dimension</th><th>2024</th><th>2025</th><th>2026</th><th>Preparation implication</th></tr></thead>
    <tbody>
      <tr><td>Duration</td><td>105 min</td><td>90 min</td><td>90 min</td><td>Practise at 72 sec/question, not 84.</td></tr>
      <tr><td>Math share</td><td>30</td><td>20</td><td>20</td><td>Do not over-index on the 2024 math spike.</td></tr>
      <tr><td>TDM share</td><td>15</td><td>15</td><td>20</td><td>Treat TDM as a daily subject, not a filler.</td></tr>
      <tr><td>OS share</td><td>9</td><td>14</td><td>11</td><td>OS numericals are non-negotiable.</td></tr>
      <tr><td>Question format</td><td>Direct MCQs dominate</td><td>More matching</td><td>Match + arrange + assertion–reason</td><td>Train format conversion, not only content.</td></tr>
      <tr><td>General awareness</td><td>0</td><td>0</td><td>4 (anomaly)</td><td>Do not start a current-affairs regime.</td></tr>
    </tbody>
  </table>

  <h3>The three-year DNA, paper by paper</h3>
  <div class="grid2" style="gap:3mm;">
    <div class="box" style="border-top:2.5pt solid #1f7a8c;"><h4>2024 · the math outlier</h4>
      <p><b>Math 30 · TDM 15 · DSA 10 · Digital 10 · OS 9</b></p>
      <p>105 minutes. Math alone was 40% of the paper. The CS core was comparatively light, and there was one DBMS question.</p>
      <p class="small">Use it for: a hard math drill and a first diagnostic. Do not use its subject split as a forecast.</p>
    </div>
    <div class="box" style="border-top:2.5pt solid #e09f3e;"><h4>2025 · the CS-heavy paper</h4>
      <p><b>Math 20 · TDM 15 · OS 14 · DSA 13 · Digital 13</b></p>
      <p>90 minutes. The CS core rose to 40 questions; OS had its highest share. Math fell to 20 but remained the largest single subject.</p>
      <p class="small">Use it for: OS and DSA numericals, and a 90-minute full mock.</p>
    </div>
    <div class="box" style="border-top:2.5pt solid #c0392b;"><h4>2026 · the format shift</h4>
      <p><b>TDM 20 · Math 20 · DSA 12 · Digital 12 · OS 11</b></p>
      <p>90 minutes. TDM became the joint-largest block. Match/arrange/assertion–reason formats increased sharply; four GK questions appeared as an anomaly.</p>
      <p class="small">Use it for: format training and TDM speed. It is the closest to the current style.</p>
    </div>
  </div>

  <div class="box accent">
    <strong>How to read the three years together.</strong> Do not average blindly and do not chase the last paper. The stable core is <b>Math (20–30) + TDM (15–20) + CS core (30–40)</b>. Prepare for Math 20 and TDM 20 as the base case, keep enough math depth for a 30-question spike, and assume the CS core will be 30–35. That single planning assumption covers all three papers.
  </div>
</div>
""")

# ---------------- SECTION 2: LEARNING ORDER ----------------
parts.append("""
<div class="section" id="s2">
  <div class="kicker">Section 2</div>
  <h2>The learning order</h2>
  <p class="section-intro">The syllabus is not a list to be studied alphabetically. Some blocks unlock others: algebra unlocks calculus; logarithms unlock complexity; digital memory unlocks OS memory; trees and queues unlock OS scheduling and file systems. The order below follows those dependencies and front-loads the highest-weight, most reusable material.</p>

  <div class="path">
    <div class="stage"><div class="num">1</div><div class="body"><b>Mathematics toolkit</b><br><span>Sets · counting · probability · statistics · algebra · matrices</span></div></div>
    <div class="stage"><div class="num">2</div><div class="body"><b>Mathematics core</b><br><span>Coordinate geometry · calculus (limits, continuity, differentiation, integration)</span></div></div>
    <div class="stage"><div class="num">3</div><div class="body"><b>Digital Fundamentals</b><br><span>Number systems · Boolean algebra · combinational · sequential · memory</span></div></div>
    <div class="stage"><div class="num">4</div><div class="body"><b>Data Structures &amp; Algorithms</b><br><span>Complexity · linear structures · trees · graphs · sorting · hashing</span></div></div>
    <div class="stage"><div class="num">5</div><div class="body"><b>Operating Systems</b><br><span>Processes · scheduling · synchronization · deadlock · memory · virtual memory · I/O</span></div></div>
    <div class="stage"><div class="num">6</div><div class="body"><b>Integrated revision</b><br><span>Full papers · error log · formula sheet · speed drills</span></div></div>
  </div>

  <div class="box warn">
    <strong>Parallel track:</strong> Thinking &amp; Decision Making does not depend on any other block. Start it on day one and do 30–40 minutes daily alongside the core sequence. Do not wait until the end — it is 22% of the paper and the easiest place to gain speed.
  </div>

  <h3>Why this order and not the paper order</h3>
  <table>
    <thead><tr><th>Stage</th><th>Weeks</th><th>What you study</th><th>Why it comes here</th></tr></thead>
    <tbody>
      <tr><td><b>1. Toolkit</b></td><td>1–3</td><td>Sets, counting, probability, statistics, algebra, logs, progressions</td><td>Every later math chapter uses these. TDM arithmetic also improves immediately.</td></tr>
      <tr><td><b>2. Math core</b></td><td>4–7</td><td>Coordinate geometry, calculus</td><td>Calculus is the single largest math topic (21 questions). Coordinate geometry is second (15).</td></tr>
      <tr><td><b>3. Digital</b></td><td>8–9</td><td>Number systems, Boolean, K-map, circuits, memory</td><td>Short, self-contained, high-scoring. Memory basics are needed for OS.</td></tr>
      <tr><td><b>4. DSA</b></td><td>10–12</td><td>Complexity, lists, stacks, trees, graphs, sorting, hashing</td><td>Logarithms and summation from math make complexity easy; queues/trees are reused in OS.</td></tr>
      <tr><td><b>5. OS</b></td><td>13–14</td><td>Processes, scheduling, deadlock, memory, virtual memory, I/O</td><td>Needs DSA (queues, trees) and digital (memory). Best studied after both.</td></tr>
      <tr><td><b>6. Revision</b></td><td>15–16</td><td>Full papers, error log, formula sheet, speed</td><td>Only works after all five blocks have been seen once.</td></tr>
    </tbody>
  </table>

  <h3>The six rules behind the sequence</h3>
  <div class="grid3">
    <div class="box"><h4>1. Prerequisite first</h4><p>Do not start calculus before you can solve quadratics, inequalities and functions. Do not start complexity before logarithms and series.</p></div>
    <div class="box"><h4>2. Weight before novelty</h4><p>Math and TDM are 53% of the paper. They get the first eight weeks and daily time, even if OS feels more “interesting”.</p></div>
    <div class="box"><h4>3. Short blocks early</h4><p>Digital is compact and self-contained. Finishing it in two weeks gives an early confidence boost and unlocks OS memory.</p></div>
    <div class="box"><h4>4. Numerical before theory</h4><p>In OS and DSA, learn the formula/algorithm first, then the theory. The paper asks “compute”, “arrange” and “match” more than “define”.</p></div>
    <div class="box"><h4>5. TDM daily, not weekly</h4><p>Reasoning is a skill, not a chapter. Twenty minutes daily beats a four-hour Sunday block.</p></div>
    <div class="box"><h4>6. Revise by retrieval</h4><p>Every module ends with “how it is asked”. Cover the answer, attempt the archetype, then check. Reading notes is not revision.</p></div>
  </div>

  <h3>Stage gates: do not advance until you can…</h3>
  <table>
    <thead><tr><th>Stage</th><th>Gate test (closed book, timed)</th></tr></thead>
    <tbody>
      <tr><td><b>1. Math toolkit</b></td><td>Solve a quadratic, a log equation, an AP/GP question and a three-set Venn problem without notes.</td></tr>
      <tr><td><b>2. Math core</b></td><td>Differentiate and integrate standard forms, find a tangent, and identify a conic from its equation.</td></tr>
      <tr><td><b>3. Digital</b></td><td>Convert bases, fill a K-map, identify a flip-flop, and compute memory capacity from address lines.</td></tr>
      <tr><td><b>4. DSA</b></td><td>State the standard complexities, traverse a tree, and explain BFS vs DFS with their data structures.</td></tr>
      <tr><td><b>5. OS</b></td><td>Compute WT/TAT, check a safe sequence, translate a paging address, and compare page-replacement algorithms.</td></tr>
      <tr><td><b>6. Revision</b></td><td>Attempt 65+ questions at 80%+ accuracy in a strict 90-minute mock, with a written error log.</td></tr>
    </tbody>
  </table>
  <div class="box accent">
    <strong>If a gate fails, do not restart the stage.</strong> Repair the specific module that failed, retest it in 48 hours, and keep the rest of the sequence moving. A stage gate is a diagnosis, not a punishment.
  </div>
</div>
""")

# ---------------- SECTION 3: MASTER SYLLABUS ----------------
parts.append(f"""
<div class="section" id="s3">
  <div class="kicker">Section 3</div>
  <h2>The master syllabus</h2>
  <p class="section-intro">Each card is one study module. The order inside a subject is the order you should learn it. The three small pills show how many questions came from 2024, 2025 and 2026. The priority badge tells you how much depth to invest.</p>

  <div class="grid2">
    <div class="box"><h4>How to read a card</h4>
      <p><b>What to learn</b> is the minimum concept set for that module. If you can explain every bullet and solve one example of each, you are ready for the exam level.</p>
      <p><b>How it is asked</b> is the actual question behaviour observed in the three papers — not a guess.</p>
      <p><b>PYQ signal</b> gives a real question or a close paraphrase so you know the flavour.</p>
    </div>
    <div class="box"><h4>Priority legend</h4>
      <p><span class="prio p0">P0</span> &nbsp;5+ questions across three years. Master every bullet. This is where ranks are built.</p>
      <p><span class="prio p1">P1</span> &nbsp;3–4 questions. Learn the standard patterns and one numerical variant.</p>
      <p><span class="prio p2">P2</span> &nbsp;1–2 questions. Learn the definition, one formula and one example.</p>
      <p><span class="prio p3">P3</span> &nbsp;Official but untested recently, or an anomaly. Cover once; do not let it displace P0/P1.</p>
    </div>
  </div>

  <h3>92 modules at a glance</h3>
  <table>
    <thead><tr><th>Subject block</th><th class="c">Modules</th><th class="c">Questions</th><th class="c">Share</th><th>Largest module (questions)</th></tr></thead>
    <tbody>{''.join(glance_rows)}</tbody>
  </table>
  <div class="table-note">Counts are the actual 2024–2026 question totals, not estimates. A card is one study module; several cards can share a module name (for example, six calculus cards). “Largest module” aggregates all cards with that module name.</div>

  <div class="box accent">
    <h4>Four rules for using the cards</h4>
    <div class="grid2">
      <div>
        <p><b>1. Follow the order.</b> Subject order, then card order, is the learning sequence. Jumping to a later card usually means missing a prerequisite.</p>
        <p><b>2. Read the pills first.</b> 24 / 25 / 26 counts tell you whether a topic is a recurring earner or a one-off. A gray pill is not failure — it is information.</p>
      </div>
      <div>
        <p><b>3. Test with “How it is asked”.</b> Close the card and answer each bullet from memory. If you can do that, the module is exam-ready; rereading “What to learn” is not revision.</p>
        <p><b>4. Stop at the depth line.</b> P0 gets every bullet, P1 gets the standard pattern, P2 gets one example, P3 gets one page. Spending P0 time on P3 is how syllabi become unfinished.</p>
      </div>
    </div>
  </div>
</div>
""")

# Subject sections
subject_blurbs = {
    "Mathematics": (
        "The largest block in all three papers. It is formula-driven and highly predictable: the same eight families reappear with different numbers. The order below goes from the toolkit (sets, counting, algebra) to the two heavyweights (coordinate geometry and calculus).",
        "30 / 20 / 20",
        "32 min · 18–22 correct",
        "Most questions are one- or two-step. The examiner rarely asks a proof. The difficulty comes from (a) choosing the right formula under time pressure, and (b) match/statement formats that hide four small calculations inside one question. Learn the standard results cold; then drill speed."
    ),
    "Thinking & Decision Making": (
        "Fifty questions, no prerequisites, and the most forgiving block if you train deliberately. It is also the most format-sensitive: series, analogy and coding questions can be solved by pattern recognition in under a minute. Run this as a daily parallel track.",
        "15 / 15 / 20",
        "18 min · 16–19 correct",
        "The paper tests speed and pattern recognition, not deep logic. Almost every question is a self-contained puzzle. The main risk is spending three minutes on one puzzle; the main opportunity is banking 15+ correct answers in 15 minutes."
    ),
    "Digital Fundamentals": (
        "A compact, rule-based block that rewards accuracy. Number systems, Boolean algebra and K-maps are almost free marks; memory and sequential circuits need a little more care. Study this before OS so that memory terminology is already familiar.",
        "10 / 13 / 12",
        "12 min · 9–12 correct",
        "The questions are short and formulaic. Most are direct conversions, simplifications, circuit identification or memory facts. There are almost no multi-step numericals. This is the best block for a high-accuracy, low-time pass."
    ),
    "Data Structures & Algorithms": (
        "The conceptual core of the CS section. The paper favours properties, invariants, complexity and matching over long code traces. Learn the standard data structures, their operations and their complexities, then practise the match/arrange formats.",
        "10 / 13 / 12",
        "14 min · 9–12 correct",
        "Expect a mix of definitions (“which is not an application of stack”), complexity ordering, tree/graph properties and pseudocode arrangement. Only a few questions require a full trace. Memorise the standard tables and invariants."
    ),
    "Operating Systems": (
        "The most numerical CS block: scheduling, paging, EAT, Banker's algorithm and page replacement. It is also the most volatile in weight (9–14), so do not skip it in a lean year. The theory questions are usually matching or classification.",
        "9 / 14 / 11",
        "14 min · 8–11 correct",
        "Half the block is formula-based, half is terminology. The numericals are repetitive once you know the formula; the theory questions test whether you can distinguish similar concepts (deadlock vs starvation, paging vs segmentation, prevention vs avoidance)."
    ),
    "Low-yield official CS": (
        "These topics appear in the official syllabus but barely appear in the three papers. They are included so the syllabus is complete, not because they deserve equal time. Cover them once, late, with a one-page summary each.",
        "1 / 0 / 0",
        "3 min · 0–1 correct",
        "Do not build a full DBMS or CN preparation block from this document. The evidence is clear: 1 DBMS question in 225, 0 CN questions. If your target year's official syllabus explicitly includes them, keep a layer/protocol table and a transaction/normalization summary; otherwise, skip after one reading."
    ),
}

endcaps = {
    "Thinking & Decision Making": """
  <h3>Last-mile TDM drill</h3>
  <table>
    <thead><tr><th>Question type</th><th>First 30 seconds</th><th>Common trap</th></tr></thead>
    <tbody>
      <tr><td><b>Number / letter series</b></td><td>Write differences; if not constant, write ratios; then check squares/cubes and two interleaved series.</td><td>Assuming one rule must fit every term.</td></tr>
      <tr><td><b>Analogy</b></td><td>Say the relation as a full sentence, including its direction.</td><td>Reversing the pair or using a looser relation.</td></tr>
      <tr><td><b>Odd one out</b></td><td>Find the property shared by three options; the fourth violates it.</td><td>Choosing a secondary property instead of the defining one.</td></tr>
      <tr><td><b>Coding–decoding</b></td><td>Write alphabet positions; test forward/backward shift and reversal.</td><td>Mixing letter-position and number codes.</td></tr>
      <tr><td><b>Blood relations / direction</b></td><td>Draw the tree or compass immediately; do not hold it in your head.</td><td>Confusing left/right after a turn; missing a generation.</td></tr>
      <tr><td><b>Syllogism</b></td><td>Draw the most unfavourable Venn diagram for the conclusion.</td><td>Converting “some” into “all”, or assuming existence.</td></tr>
    </tbody>
  </table>
  <p class="small"><b>Daily drill:</b> 20 mixed questions in 18 minutes. Log every miss by question type, not by question — the type is what you fix.</p>
""",
    "Digital Fundamentals": """
  <h3>Digital: facts that cover most questions</h3>
  <table>
    <thead><tr><th>Fact</th><th>Value / rule</th></tr></thead>
    <tbody>
      <tr><td><b>2's-complement range</b></td><td>n bits: −2ⁿ⁻¹ to 2ⁿ⁻¹−1. Overflow occurs when the carry into and out of the sign bit differ.</td></tr>
      <tr><td><b>Multiplexer</b></td><td>A 2ⁿ:1 MUX needs n select lines; a tree of 2:1 MUXes for 2ⁿ:1 needs 2ⁿ−1 MUXes.</td></tr>
      <tr><td><b>Decoder</b></td><td>n inputs → 2ⁿ outputs; each output corresponds to one minterm.</td></tr>
      <tr><td><b>Flip-flop states</b></td><td>n flip-flops → 2ⁿ states; a mod-N counter needs ⌈log₂N⌉ flip-flops.</td></tr>
      <tr><td><b>Memory capacity</b></td><td>Capacity = 2^(address lines) × word size; address lines = log₂(number of words).</td></tr>
      <tr><td><b>K-map</b></td><td>Groups of 1, 2, 4, 8; Gray-code adjacency; wrap-around allowed; don't-cares may be 0 or 1.</td></tr>
      <tr><td><b>IEEE 754 single</b></td><td>1 sign + 8 exponent (bias 127) + 23 mantissa; normals are (−1)ˢ × 1.M × 2^(E−127).</td></tr>
    </tbody>
  </table>
  <p class="small"><b>Accuracy rule:</b> label MSB/LSB and the bit width before you convert or add. Most digital errors are position errors, not concept errors.</p>
""",
    "Data Structures & Algorithms": """
  <h3>DSA: the complexity table to write from memory</h3>
  <table>
    <thead><tr><th>Operation / algorithm</th><th class="c">Best</th><th class="c">Average</th><th class="c">Worst</th></tr></thead>
    <tbody>
      <tr><td><b>Binary search</b> (sorted array)</td><td class="c">O(1)</td><td class="c">O(log n)</td><td class="c">O(log n)</td></tr>
      <tr><td><b>Merge sort</b></td><td class="c">O(n log n)</td><td class="c">O(n log n)</td><td class="c">O(n log n)</td></tr>
      <tr><td><b>Quick sort</b></td><td class="c">O(n log n)</td><td class="c">O(n log n)</td><td class="c">O(n²)</td></tr>
      <tr><td><b>Heap sort</b></td><td class="c">O(n log n)</td><td class="c">O(n log n)</td><td class="c">O(n log n)</td></tr>
      <tr><td><b>BST search</b></td><td class="c">O(1)</td><td class="c">O(log n)</td><td class="c">O(n)</td></tr>
      <tr><td><b>Hash search</b></td><td class="c">O(1)</td><td class="c">O(1)</td><td class="c">O(n)</td></tr>
      <tr><td><b>BFS / DFS</b></td><td class="c">—</td><td class="c">O(V+E)</td><td class="c">O(V+E)</td></tr>
      <tr><td><b>Dijkstra</b> (binary heap)</td><td class="c">—</td><td class="c">O((V+E) log V)</td><td class="c">O((V+E) log V)</td></tr>
    </tbody>
  </table>
  <p class="small"><b>Memory hook:</b> “log n for halving, n log n for sorting by comparison, n² for pairwise work, V+E for graph traversal.” If an option violates the hook, it is usually wrong.</p>
""",
    "Operating Systems": """
  <h3>OS: the five numerical templates</h3>
  <table>
    <thead><tr><th>Numerical</th><th>Template / check</th></tr></thead>
    <tbody>
      <tr><td><b>CPU scheduling</b></td><td>TAT = CT − AT; WT = TAT − BT; draw the Gantt chart before computing. For RR, keep the ready queue in arrival order.</td></tr>
      <tr><td><b>Deadlock bound</b></td><td>n processes, each needing at most m units: n(m−1)+1 units guarantee no deadlock.</td></tr>
      <tr><td><b>Paging bits</b></td><td>Offset = log₂(page size); page-number bits = log₂(number of pages); virtual bits = page bits + offset.</td></tr>
      <tr><td><b>EAT</b></td><td>EAT = (1−p)·m + p·s. Convert ns/ms first; the answer is usually dominated by p·s.</td></tr>
      <tr><td><b>Page replacement</b></td><td>Simulate the reference string frame by frame; count faults, not hits. FIFO can show Belady's anomaly; LRU cannot.</td></tr>
    </tbody>
  </table>
  <p class="small"><b>One-line check:</b> every OS numerical has a “before you calculate” condition — preemptive or not, offset &lt; limit, Need = Max − Allocation. Write it down first.</p>

  <h3>OS theory traps</h3>
  <table>
    <thead><tr><th>Pair</th><th>Distinction the examiner tests</th></tr></thead>
    <tbody>
      <tr><td><b>Deadlock vs starvation</b></td><td>Deadlock: a set of processes can never proceed. Starvation: a process can proceed in principle but is indefinitely overlooked.</td></tr>
      <tr><td><b>Paging vs segmentation</b></td><td>Paging is fixed-size, invisible to the programmer, internal fragmentation. Segmentation is variable-size, logical, external fragmentation.</td></tr>
      <tr><td><b>Prevention vs avoidance</b></td><td>Prevention breaks one Coffman condition. Avoidance uses future information (Banker's) to stay in a safe state.</td></tr>
      <tr><td><b>Detection vs recovery</b></td><td>Detection finds the cycle (wait-for graph). Recovery breaks it: terminate a process or preempt a resource.</td></tr>
      <tr><td><b>Internal vs external fragmentation</b></td><td>Internal: allocated block is larger than needed. External: free memory is split into non-contiguous holes.</td></tr>
      <tr><td><b>Page fault vs thrashing</b></td><td>A page fault is one miss. Thrashing is a sustained high fault rate that leaves no CPU time for useful work.</td></tr>
    </tbody>
  </table>
""",
    "Low-yield official CS": """
  <h3>The only CN table you need</h3>
  <table>
    <thead><tr><th>TCP/IP layer</th><th>Protocols / devices</th><th>One-line job</th></tr></thead>
    <tbody>
      <tr><td><b>Application</b></td><td>HTTP, DNS, SMTP, POP3, FTP, DHCP</td><td>User services, naming and mail/web transfer.</td></tr>
      <tr><td><b>Transport</b></td><td>TCP, UDP</td><td>End-to-end delivery, ports, reliability (TCP) or speed (UDP).</td></tr>
      <tr><td><b>Internet</b></td><td>IP, ICMP, routing protocols</td><td>Logical addressing, packet forwarding and error reporting.</td></tr>
      <tr><td><b>Network access</b></td><td>Ethernet, Wi-Fi, ARP, hub, switch, bridge</td><td>Frames on the local link; MAC addressing.</td></tr>
    </tbody>
  </table>
  <p class="small"><b>Device line:</b> hub broadcasts, switch forwards by MAC, router forwards by IP, gateway translates between protocols. OSI adds session and presentation layers; TCP/IP folds both into application. If CN appears, expect layer/protocol matching — not subnetting.</p>

  <h3>DBMS insurance in six lines</h3>
  <div class="box accent">
    <ul>
      <li><b>ACID:</b> Atomicity (all or nothing), Consistency (constraints preserved), Isolation (concurrent schedules behave serially), Durability (committed data survives failure).</li>
      <li><b>Conflict serializability:</b> build a precedence graph; the schedule is conflict-serializable iff the graph is acyclic.</li>
      <li><b>Keys:</b> superkey ⊇ candidate key; primary key is the chosen candidate; foreign key references a candidate key.</li>
      <li><b>Normal forms:</b> 1NF atomic values; 2NF no partial dependency on a composite key; 3NF no transitive dependency; BCNF every determinant is a candidate key.</li>
      <li><b>Relational algebra:</b> σ select rows, π project columns, ⋈ join, × product, ∪/∩/− set operations.</li>
      <li><b>SQL order:</b> FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY. Know one aggregate query with GROUP BY and HAVING.</li>
    </ul>
  </div>
  <p class="small"><b>Stop line:</b> this page is the whole DBMS insurance policy. Do not open query optimisation, recovery algorithms or normalization proofs unless the official syllabus forces them.</p>
""",
}

for idx, (s, label, prefix) in enumerate(SUBJECTS, start=1):
    blurb, stats, target, nature = subject_blurbs[s]
    parts.append(f'<div class="section" id="sec-{s.replace(" ", "-").lower()}">')
    parts.append(subject_header(s, f"3.{idx} {label}", blurb, stats, target, nature))
    if s == "Low-yield official CS":
        parts.append("""
        <div class="box warn"><strong>Read this before spending time here.</strong> The current NTA syllabus (December 2025) lists Computer Networks and DBMS. The 2024–2026 papers tested one DBMS question and zero CN questions. Treat these as insurance, not as a main subject. The opportunity cost of a full DBMS/CN block is enormous: those hours are better spent on calculus, TDM or OS numericals.</div>
        """)
    parts.append(card_html[s])
    if s in endcaps:
        parts.append(endcaps[s])
    parts.append("</div>")

# ---------------- SECTION 4: HOW QUESTIONS ARE ASKED ----------------
parts.append("""
<div class="section" id="s4">
  <div class="kicker">Section 4</div>
  <h2>How questions are asked</h2>
  <p class="section-intro">Content knowledge is only half the paper. The other half is recognising the format quickly. Across 225 questions, ten recurring formats account for almost everything. The percentages below are keyword-based approximations; they are useful for training, not for predicting an exact count.</p>

  <table>
    <thead><tr><th>Format</th><th class="c">Approx. count</th><th class="c">Share</th><th>What it looks like</th><th>Time target</th></tr></thead>
    <tbody>
      <tr><td><b>Direct single-concept MCQ</b></td><td class="c">~120</td><td class="c">~53%</td><td>One definition, one formula or one short numerical; four options.</td><td>45–60 s</td></tr>
      <tr><td><b>Match List-I with List-II</b></td><td class="c">28</td><td class="c">12.4%</td><td>Four pairs; one-to-one matching; often 4 small facts in one question.</td><td>75–90 s</td></tr>
      <tr><td><b>Arrange in correct order</b></td><td class="c">21</td><td class="c">9.3%</td><td>Algorithm steps, OS layers, semaphore operations, memory read sequence.</td><td>60–75 s</td></tr>
      <tr><td><b>Multi-statement true/false</b></td><td class="c">14</td><td class="c">6.2%</td><td>Statements A, B, C, D; choose the correct combination.</td><td>75–90 s</td></tr>
      <tr><td><b>Assertion–Reason</b></td><td class="c">9</td><td class="c">4.0%</td><td>A and R; decide truth and whether R explains A. Concentrated in 2026.</td><td>60 s</td></tr>
      <tr><td><b>“Which is NOT” / odd one out</b></td><td class="c">~15</td><td class="c">~7%</td><td>Three correct examples and one exception; or an odd item from a group.</td><td>45–60 s</td></tr>
      <tr><td><b>Diagram / figure based</b></td><td class="c">~15</td><td class="c">~7%</td><td>Figure series, counting, K-map, tree/graph diagram, circuit.</td><td>60–90 s</td></tr>
      <tr><td><b>Cross-topic matching</b></td><td class="c">~10</td><td class="c">~4%</td><td>Algorithm ↔ data structure ↔ application; concept ↔ example.</td><td>75–90 s</td></tr>
    </tbody>
  </table>
  <div class="table-note">Formats overlap: a question can be both “match” and “multi-statement”. Counts come from keyword tagging of the 225 classified questions, then manual review of ambiguous cases.</div>

  <h3>The ten archetypes, with real examples</h3>

  <div class="arche"><div class="top"><div class="name">A1 · Direct definition / recall</div><div class="tag">45–60 s · ~40% of paper</div></div>
  <div class="q">“Which of the following is a universal logic gate?” (2026 Q65) · “Which is NOT an application of stack?” (2024 Q61)</div>
  <div class="do"><b>Approach:</b> Answer from a memorised table, not from first principles. If two options look similar, the examiner is testing a distinction (NAND vs NOR, stack vs queue, RAM vs ROM). <b>Trap:</b> “NOT” questions — mark the word before reading the options.</div></div>

  <div class="arche"><div class="top"><div class="name">A2 · One-formula numerical</div><div class="tag">60–90 s · ~25%</div></div>
  <div class="q">“Page-fault service time 10 ms, memory access 30 ns, one fault per 10⁶ accesses — find EAT.” (2024 Q46) · “1K pages, 512 frames, 2 KB page — how many virtual address bits?” (2024 Q47)</div>
  <div class="do"><b>Approach:</b> Write the formula, substitute in consistent units, estimate the answer before computing. <b>Trap:</b> ns vs ms; bits vs bytes; page size vs number of pages.</div></div>

  <div class="arche"><div class="top"><div class="name">A3 · Match List-I with List-II</div><div class="tag">75–90 s · 28 questions</div></div>
  <div class="q">“Match JK flip-flop inputs 00/01/10/11 with no-change/set/reset/toggle.” (2025 Q69) · “Match algorithms with recurrences.” (2025 Q53)</div>
  <div class="do"><b>Approach:</b> Do the pairs you are sure of first; eliminate options; use the one-to-one constraint. <b>Trap:</b> One wrong pair can make the whole option wrong; do not guess the last pair blindly.</div></div>

  <div class="arche"><div class="top"><div class="name">A4 · Arrange in correct order</div><div class="tag">60–75 s · 21 questions</div></div>
  <div class="q">“Arrange the semaphore operations for the producer.” (2026 Q49) · “Arrange the steps to retrieve data from memory.” (2026 Q75)</div>
  <div class="do"><b>Approach:</b> Find the fixed first and last step, then order the middle. Use the dependency, not the option order. <b>Trap:</b> Two steps can look interchangeable; check what must be true before the next.</div></div>

  <div class="arche"><div class="top"><div class="name">A5 · Multi-statement true/false</div><div class="tag">75–90 s · 14 questions</div></div>
  <div class="q">“RAM is a combinational circuit; PLA is a combinational circuit…” (2024 Q66) · “Which statements about symmetric matrices are true?” (2024 Q22)</div>
  <div class="do"><b>Approach:</b> Evaluate each statement independently and mark T/F; then match the pattern to the options. <b>Trap:</b> One false word (“always”, “only”, “every”) invalidates a statement.</div></div>

  <div class="arche"><div class="top"><div class="name">A6 · Assertion–Reason</div><div class="tag">60 s · 9 questions, all 2026</div></div>
  <div class="q">“A: Leaves are green. R: Plants contain chromoplast.” (2026 Q9)</div>
  <div class="do"><b>Approach:</b> First decide A and R separately; then ask whether R is the correct explanation of A. <b>Trap:</b> A true R that explains a different fact is not the answer. In 2026 this format appeared in science GK and calculus.</div></div>

  <div class="arche"><div class="top"><div class="name">A7 · “Which is NOT” / odd one out</div><div class="tag">45–60 s · ~15 questions</div></div>
  <div class="q">“Which is NOT an application of stack?” (2024 Q61, 2026 Q52) · “Which word is different: arrow, missile, sword, bullet?” (2025 Q13)</div>
  <div class="do"><b>Approach:</b> Test each option against the defining property; the exception usually violates one criterion. <b>Trap:</b> Several options may share a secondary property; use the most essential one.</div></div>

  <div class="arche"><div class="top"><div class="name">A8 · Diagram / figure based</div><div class="tag">60–90 s · ~15 questions</div></div>
  <div class="q">“Find the number of triangles.” (2025 Q5) · “Complete the figure matrix.” (2024 Q7) · “Find the function from the K-map.” (2024 Q71)</div>
  <div class="do"><b>Approach:</b> Label the figure, count systematically by size/orientation, and look for one rule at a time. <b>Trap:</b> Double counting; assuming rotation when the rule is reflection.</div></div>

  <div class="arche"><div class="top"><div class="name">A9 · Multi-statement combination</div><div class="tag">75–90 s · common in math</div></div>
  <div class="q">“Choose the correct answer from the options: (1) A and B only (2) B and C only …”</div>
  <div class="do"><b>Approach:</b> This is A5 with a different wrapper. Evaluate the statements, then eliminate combinations. <b>Trap:</b> Options often repeat one statement; use it as an anchor.</div></div>

  <div class="arche"><div class="top"><div class="name">A10 · Cross-topic matching</div><div class="tag">75–90 s · 2026 increase</div></div>
  <div class="q">“Match: MST, stack, BFS, sparse graph with height-balanced tree, recursion, shortest paths, adjacency list.” (2026 Q57)</div>
  <div class="do"><b>Approach:</b> Build a three-column mental table (concept → structure → application). Start with the pair you know best. <b>Trap:</b> The same term can fit two descriptions; use the unique one.</div></div>

  <h3>Question wording decoder</h3>
  <table>
    <thead><tr><th>Phrase in the paper</th><th>What it usually means</th><th>First action</th></tr></thead>
    <tbody>
      <tr><td>“Which of the following statements is/are true?”</td><td>Multi-statement T/F; one false word can flip the answer.</td><td>Mark each statement T/F before looking at options.</td></tr>
      <tr><td>“Choose the correct answer from the options given below”</td><td>Combination options (A/B/C/D only).</td><td>Eliminate by one confident statement.</td></tr>
      <tr><td>“Arrange … in the correct order/sequence”</td><td>Process or algorithm steps.</td><td>Find first/last, then dependencies.</td></tr>
      <tr><td>“Match List-I with List-II”</td><td>Four one-to-one pairs.</td><td>Fix sure pairs; use elimination.</td></tr>
      <tr><td>“Which is NOT / except”</td><td>Three true, one false.</td><td>Underline NOT; test the defining property.</td></tr>
      <tr><td>“Assertion (A) … Reason (R) …”</td><td>Truth of A, truth of R, and explanation link.</td><td>Decide A, then R, then the link.</td></tr>
      <tr><td>“The minimum number of … required”</td><td>Extremal formula (MUX, resources, bits, states).</td><td>Write the known formula; check units.</td></tr>
      <tr><td>“In the light of the above statements”</td><td>Assertion–reason or data-sufficiency style.</td><td>Do not import outside assumptions.</td></tr>
    </tbody>
  </table>

  <h3>Top traps by subject</h3>
  <table>
    <thead><tr><th>Subject</th><th>Most common trap</th><th>How to avoid it</th></tr></thead>
    <tbody>
      <tr><td><b>Mathematics</b></td><td>Using a formula outside its condition (L'Hôpital without 0/0; area without absolute value; conic orientation).</td><td>Write the condition next to the formula; check the sign/orientation before computing.</td></tr>
      <tr><td><b>TDM</b></td><td>Reversing the relation in analogy; missing “only/at least”; choosing a secondary odd-one-out criterion.</td><td>Say the relation in a full sentence before applying it; underline quantifiers.</td></tr>
      <tr><td><b>Digital</b></td><td>MSB/LSB order; bias 127 vs 1023; grouping K-map cells across the edge; combinational vs sequential.</td><td>Label bit positions; draw the K-map with Gray order; ask “does it have memory?”</td></tr>
      <tr><td><b>DSA</b></td><td>Best vs worst case; 0-index vs 1-index; directed vs undirected edge counts; complete vs full tree.</td><td>Write the case and the convention at the top of the rough work.</td></tr>
      <tr><td><b>OS</b></td><td>Preemptive vs non-preemptive; Need = Max − Allocation; offset ≥ limit; FIFO Belady anomaly.</td><td>Write the algorithm’s precondition; recheck units and table columns.</td></tr>
    </tbody>
  </table>
</div>
""")

# ---------------- SECTION 5: WEIGHTAGE AND TRENDS ----------------
# Top topics table: aggregate by module
module_counts = defaultdict(lambda: Counter())
for r in ROWS:
    if r["subject"] == "Low-yield official CS":
        continue
    module_counts[(r["subject"], r["module"])] += Counter(r["counts"])

top_modules = sorted(module_counts.items(), key=lambda kv: -sum(kv[1].values()))[:20]
top_rows = []
for (s, m), c in top_modules:
    top_rows.append(f"<tr><td>{esc(s)}</td><td><b>{esc(m)}</b></td><td class='c'>{c['2024']}</td><td class='c'>{c['2025']}</td><td class='c'>{c['2026']}</td><td class='c'><b>{sum(c.values())}</b></td></tr>")

parts.append(f"""
<div class="section" id="s5">
  <div class="kicker">Section 5</div>
  <h2>Weightage and trends</h2>
  <p class="section-intro">The subject split tells you what to study; the topic split tells you what to master. The table below aggregates the 225 questions by module. Read it as a priority list, not a fixed prediction: the paper rotates individual subtopics but keeps the same families.</p>

  <h3>The 20 highest-yield modules</h3>
  <table>
    <thead><tr><th>Subject</th><th>Module</th><th class="c">2024</th><th class="c">2025</th><th class="c">2026</th><th class="c">Total</th></tr></thead>
    <tbody>{''.join(top_rows)}</tbody>
  </table>
  <div class="table-note">Modules are groups of closely related subtopics (for example, all calculus subtopics are one module). The full subtopic split is in the master syllabus cards.</div>

  <h3>What is stable, what is volatile</h3>
  <div class="grid2">
    <div class="box"><h4>Stable (plan for these every year)</h4>
      <ul>
        <li>Calculus: 5–10 questions every year.</li>
        <li>Coordinate geometry: 4–6 every year.</li>
        <li>Series, analogy and logical reasoning: 10–14 together.</li>
        <li>Digital Boolean/K-map/circuits: 6–9.</li>
        <li>OS deadlock + memory + virtual memory: 6–9.</li>
        <li>DSA trees + graphs + complexity: 6–9.</li>
      </ul>
    </div>
    <div class="box"><h4>Volatile (do not over-fit to one year)</h4>
      <ul>
        <li>Mathematics: 30 in 2024, then 20 and 20. Do not assume 30.</li>
        <li>OS: 9 → 14 → 11. A lean year can still ask 14.</li>
        <li>TDM: 15 → 15 → 20. The trend is upward, not fixed.</li>
        <li>General awareness: 0 → 0 → 4. Treat 2026 as an anomaly.</li>
        <li>DBMS/CN: 1 → 0 → 0. Insurance only.</li>
      </ul>
    </div>
  </div>

  <h3>Subtopic heat map</h3>
  <table>
    <thead><tr><th>Band</th><th>Subtopics</th><th>What to do</th></tr></thead>
    <tbody>
      <tr><td><b>Hot (5–7 Qs)</b></td><td>Number series, word analogy, limits, matrix algebra, sets/Venn, deadlock</td><td>Master every variant; these alone are ~15% of the paper.</td></tr>
      <tr><td><b>Warm (3–4 Qs)</b></td><td>Asymptotic order, BST, flip-flops, progressions, quadratic, continuity, integration, odd-one-out, figure series, letter series, linked lists, graphs, Boolean, K-map, MUX, memory hierarchy, CPU scheduling, paging, synchronization, virtual memory, circles, parabola, determinants, statistics</td><td>Learn the standard pattern and one numerical variant each.</td></tr>
      <tr><td><b>Cool (1–2 Qs)</b></td><td>The long tail: hashing, heaps, B-trees, sorting, probability, P&amp;C, ellipse, conic properties, file systems, segmentation, banker's algorithm, etc.</td><td>Know the definition and one example; do not chase every variant.</td></tr>
      <tr><td><b>Cold (0 Qs)</b></td><td>CN, deep DBMS, computer arithmetic algorithms, IC logic families, parameter passing</td><td>One-page summary late; no full block.</td></tr>
    </tbody>
  </table>

  <div class="box accent">
    <h4>The 80/20 of this paper</h4>
    <p>If you master only the <b>top 20 modules</b> in the table above, you cover <b>179 of 225 questions (79.6%)</b>. Add the next 10 modules and you are above 90%. The remaining long tail is real, but it is not where ranks are decided.</p>
  </div>
</div>
""")

# ---------------- SECTION 6: HIGH-YIELD VS LOW-YIELD ----------------
parts.append("""
<div class="section" id="s6">
  <div class="kicker">Section 6</div>
  <h2>High-yield vs low-yield</h2>
  <p class="section-intro">A syllabus is also a list of things not to study. This section is deliberately blunt: it separates what the paper rewards from what the syllabus mentions but the paper ignores. Use it to protect your time.</p>

  <h3>Tier 1 — master these first (P0)</h3>
  <div class="cols2">
    <div class="box"><h4>Mathematics</h4><ul class="checklist">
      <li>Limits and continuity (10 Qs)</li><li>Differentiation, tangents and maxima/minima (4 Qs)</li>
      <li>Integration and definite integrals/area (7 Qs)</li><li>Coordinate geometry: circle, parabola, ellipse/hyperbola, lines (15 Qs)</li>
      <li>Matrices and determinants (9 Qs)</li><li>Sets/Venn and quadratic/inequalities (10 Qs)</li>
    </ul></div>
    <div class="box"><h4>TDM</h4><ul class="checklist">
      <li>Number and letter series (11 Qs)</li><li>Word/number analogy and odd one out (13 Qs)</li>
      <li>Coding–decoding, blood relations, direction, seating (9 Qs)</li><li>Syllogism and verbal reasoning (3 Qs)</li>
      <li>Figure series, counting and mirror images (6 Qs)</li>
    </ul></div>
    <div class="box"><h4>Digital</h4><ul class="checklist">
      <li>Number systems, complements, floating point (6 Qs)</li><li>Boolean algebra, gates and K-map (8 Qs)</li>
      <li>Combinational circuits: adders, MUX, decoder (8 Qs)</li><li>Flip-flops, registers, counters (6 Qs)</li>
      <li>Memory hierarchy, RAM/ROM, addressing (7 Qs)</li>
    </ul></div>
    <div class="box"><h4>DSA + OS</h4><ul class="checklist">
      <li>Complexity and recurrences (5 Qs)</li><li>Trees: BST, AVL, B/B+, heaps (8 Qs)</li>
      <li>Graphs: representation, BFS/DFS, shortest paths (7 Qs)</li><li>Linked lists, stacks, queues (8 Qs)</li><li>Sorting, searching, hashing (6 Qs)</li>
      <li>Deadlock and Banker's algorithm (7 Qs)</li><li>Memory, paging, virtual memory (10 Qs)</li>
      <li>CPU scheduling, synchronization, file/disk (12 Qs)</li>
    </ul></div>
  </div>

  <h3>Tier 2 — cover once, late (P2/P3)</h3>
  <table>
    <thead><tr><th>Topic</th><th>Why it is Tier 2</th><th>Minimum coverage</th></tr></thead>
    <tbody>
      <tr><td>Hashing, heaps, B/B+ trees</td><td>2 Qs each; often definitional.</td><td>One page of properties + one complexity table.</td></tr>
      <tr><td>Probability, P&amp;C, statistics</td><td>3 Qs each; formula-driven but lower frequency.</td><td>Standard formulas + one solved example each.</td></tr>
      <tr><td>Ellipse, hyperbola, conic identification</td><td>2 Qs each; overlap with coordinate geometry.</td><td>Standard forms, eccentricity, latus rectum.</td></tr>
      <tr><td>File systems, disk scheduling, segmentation</td><td>1–3 Qs; often one numerical.</td><td>Disk algorithms + segment translation + inode basics.</td></tr>
      <tr><td>Banker's algorithm</td><td>1 Q in 2024; still a classic numerical.</td><td>Need matrix + safety check; one solved table.</td></tr>
      <tr><td>Computer arithmetic, logic families, DBMS transactions</td><td>0–1 Qs each; official but absent or rare.</td><td>One-page flowchart/property summary; conflict serializability + precedence graph.</td></tr>
    </tbody>
  </table>

  <h3>What to drop without guilt</h3>
  <div class="box warn">
    <ul>
      <li><b>English grammar, vocabulary, reading comprehension.</b> These belonged to the pre-2024 Part A. There is no Part A in 2024–2026.</li>
      <li><b>Daily current affairs and general studies.</b> 2026 added four static-science/GK questions; that is an anomaly, not a new section. A 15-minute weekly static-GK review is enough.</li>
      <li><b>Deep DBMS:</b> normalization proofs, SQL query tuning, recovery algorithms, Codd's rules in detail. One question in three years.</li>
      <li><b>Computer networks:</b> subnetting drills, routing protocol internals, cryptography mathematics. Zero questions in three years. Keep only a layer/protocol table as insurance.</li>
      <li><b>Software engineering, TOC, compilers, AI/ML, web development, Python/Java.</b> Not in the current SCQP09 syllabus and not in the papers.</li>
      <li><b>Advanced engineering mathematics:</b> differential equations, complex analysis, 3D geometry, vector calculus, linear programming, real-analysis proofs. Not asked.</li>
      <li><b>Advanced computer architecture:</b> pipelining hazards, cache-mapping numericals, microprogramming, instruction formats. Only memory-hierarchy basics appear.</li>
      <li><b>Hardware electronics:</b> transistor-level analysis, IC fabrication, logic-family electrical characteristics. Only the digital-logic abstraction is asked.</li>
    </ul>
  </div>

  <div class="box accent">
    <h4>Official but untested: the honest position</h4>
    <p>The December 2025 NTA syllabus lists <b>Computer Networks</b> and a full <b>DBMS</b> block. The 2024–2026 papers do not reflect that breadth: 0 CN and 1 DBMS question. If your target year’s syllabus still lists them, do a <b>two-hour orientation</b> (layers/protocols; ER/normalization/transactions) in the final month. Do not let it become a third CS subject. The evidence says the marks are in the five core blocks.</p>
  </div>

  <h3>If CN/DBMS are in your syllabus: the two-hour insurance plan</h3>
  <table>
    <thead><tr><th>Block</th><th>60-minute minimum</th><th>What to skip</th></tr></thead>
    <tbody>
      <tr><td><b>Computer Networks</b></td><td>OSI and TCP/IP layer table; protocol-to-layer matching (HTTP, DNS, SMTP, FTP, TCP, UDP, IP); LAN devices (hub, switch, bridge, router, gateway); transmission media; IPv4 basics; firewall/cryptography definitions.</td><td>Subnetting drills, routing-algorithm calculations, congestion-control maths, protocol-header bit fields.</td></tr>
      <tr><td><b>DBMS</b></td><td>ACID; conflict serializability and precedence graph; ER entities/relationships; keys and constraints; 1NF–3NF/BCNF definitions; relational algebra symbols; one SQL SELECT example.</td><td>Query optimisation, recovery algorithms, security/authorisation, object-relational details, Codd’s rules in depth.</td></tr>
    </tbody>
  </table>
  <div class="box warn"><strong>When to do it:</strong> in the last 10 days, not in the first 10 weeks. Spend 60 minutes on each block, make a one-page sheet, and test yourself with 10 definitional questions. If the paper again ignores these topics, you have lost two hours — not two months.</div>
</div>
""")

# ---------------- SECTION 7: PLAN ----------------
weeks = [
    ("1", "Math toolkit: sets, Venn, counting, probability", "TDM: series + analogy (daily)", "Diagnostic: 2024 paper, untimed"),
    ("2", "Algebra: indices/logs, quadratic, inequalities, functions, AP/GP/HP", "TDM: coding, blood relations, direction", "30 math + 20 TDM questions"),
    ("3", "Statistics + matrices/determinants", "TDM: seating, syllogism, verbal", "Sectional: math toolkit"),
    ("4", "Coordinate geometry: lines, circle", "TDM: figure series + counting", "Sectional: coordinate"),
    ("5", "Coordinate geometry: parabola, ellipse, hyperbola, conics", "TDM: mixed figures + puzzles", "Full math section, timed"),
    ("6", "Calculus: limits, continuity", "TDM: 20-question speed set", "Sectional: calculus I"),
    ("7", "Calculus: differentiation, maxima/minima, integration, area", "TDM: error log review", "Full math paper, 35 min"),
    ("8", "Math revision + weak-topic repair", "TDM: full 20 in 18 min", "Half mock: math + TDM"),
    ("9", "Digital: number systems, complements, floating point, error codes", "TDM daily", "Sectional: digital I"),
    ("10", "Digital: Boolean, K-map, combinational, sequential, memory", "TDM daily", "Sectional: digital II"),
    ("11", "DSA: complexity, arrays, linked lists, stacks, queues", "TDM daily", "Sectional: DSA I"),
    ("12", "DSA: trees, BST, AVL, heaps, B-trees", "TDM daily", "Sectional: DSA II"),
    ("13", "DSA: graphs, sorting, searching, hashing", "TDM daily", "Sectional: DSA III"),
    ("14", "OS: processes, scheduling, synchronization, deadlock", "TDM daily", "Sectional: OS I"),
    ("15", "OS: memory, paging, virtual memory, file/disk + full revision", "TDM daily", "Full mock #1"),
    ("16", "Full revision: formula sheet, error log, 4 full mocks", "TDM: 20 in 15 min", "Full mocks #2–#4 + analysis"),
]
week_rows = "".join(
    f"<tr><td>{w}</td><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for w, a, b, c in weeks
)

parts.append(f"""
<div class="section" id="s7">
  <div class="kicker">Section 7</div>
  <h2>The 16-week plan</h2>
  <p class="section-intro">This plan assumes 4–5 focused hours on weekdays and 6–7 on weekends. If you have less time, use the 6-week crash plan below. The sequence is fixed; the pace is adjustable.</p>

  <h3>Week-by-week</h3>
  <table class="weeks">
    <thead><tr><th>Week</th><th>Core block (2.5–3 h/day)</th><th>Parallel TDM (30–40 min/day)</th><th>Weekly test</th></tr></thead>
    <tbody>{week_rows}</tbody>
  </table>

  <div class="box accent">
    <h4>Plan rules that matter more than the schedule</h4>
    <div class="grid2">
      <div>
        <ul>
          <li><b>Never skip two TDM days in a row.</b> Reasoning is a skill; a four-day gap costs more than a missed chapter.</li>
          <li><b>Every week ends with a timed test.</b> Untimed practice measures knowledge; timed practice measures rank.</li>
        </ul>
      </div>
      <div>
        <ul>
          <li><b>If a week slips, cut practice volume — not the concept block.</b> Finishing the concept once is cheaper than restarting it later.</li>
          <li><b>Protect the last 20 minutes of the day.</b> Retrieval and the error log are where marks actually move.</li>
        </ul>
      </div>
    </div>
  </div>

  <h3>The daily template</h3>
  <div class="grid2">
    <div class="box"><h4>Weekday (4–5 h)</h4>
      <ul>
        <li><b>60 min</b> — new concept + 10 solved examples.</li>
        <li><b>60 min</b> — 25–30 practice questions on that concept.</li>
        <li><b>40 min</b> — TDM sprint (20 questions, timed).</li>
        <li><b>40 min</b> — previous-day retrieval + error log.</li>
        <li><b>30 min</b> — formula sheet / flashcards.</li>
      </ul>
    </div>
    <div class="box"><h4>Weekend (6–7 h)</h4>
      <ul>
        <li><b>2 h</b> — sectional test (75 questions or one subject).</li>
        <li><b>2 h</b> — full analysis: every wrong answer, every guess.</li>
        <li><b>2 h</b> — weak-topic repair from the error log.</li>
        <li><b>1 h</b> — TDM mixed set + formula revision.</li>
      </ul>
    </div>
  </div>

  <h3>6-week crash plan</h3>
  <table>
    <thead><tr><th>Week</th><th>What to do</th><th>Non-negotiable</th></tr></thead>
    <tbody>
      <tr><td><b>1</b></td><td>Math toolkit + limits/continuity + TDM series/analogy</td><td>30 math + 20 TDM questions daily</td></tr>
      <tr><td><b>2</b></td><td>Calculus (differentiation/integration/area) + coordinate geometry</td><td>One full math section, timed</td></tr>
      <tr><td><b>3</b></td><td>Matrices, sets, probability, statistics + Digital number systems/Boolean</td><td>Digital K-map and conversion drills</td></tr>
      <tr><td><b>4</b></td><td>Digital circuits/memory + DSA complexity/lists/trees</td><td>DSA complexity table memorised</td></tr>
      <tr><td><b>5</b></td><td>DSA graphs/sorting/hashing + OS scheduling/deadlock</td><td>Two OS numericals daily</td></tr>
      <tr><td><b>6</b></td><td>OS memory/virtual memory + 4 full mocks + error log</td><td>One full mock every alternate day</td></tr>
    </tbody>
  </table>

  <h3>Revision rhythm: 1–3–7–21</h3>
  <div class="box accent">
    <p>Revise each new module on <b>day 1</b> (same evening), <b>day 3</b> (short retrieval), <b>day 7</b> (mixed questions) and <b>day 21</b> (full-paper context). This is more effective than rereading notes. Use the priority badge: P0 modules get all four touches; P2/P3 get only day 1 and day 21.</p>
  </div>

  <h3>Weekly scoreboard</h3>
  <table>
    <thead><tr><th>Metric</th><th>Target by week 8</th><th>Target by week 16</th></tr></thead>
    <tbody>
      <tr><td>Questions attempted in 90 min</td><td>65</td><td>72–75</td></tr>
      <tr><td>Accuracy on attempted</td><td>75%</td><td>85%+</td></tr>
      <tr><td>TDM time for 20 questions</td><td>22 min</td><td>15–17 min</td></tr>
      <tr><td>Math time for 20 questions</td><td>35 min</td><td>28–30 min</td></tr>
      <tr><td>Full mock score</td><td>180–200</td><td>230–250+</td></tr>
    </tbody>
  </table>
</div>
""")

# ---------------- SECTION 8: EXAM DAY ----------------
parts.append("""
<div class="section" id="s8">
  <div class="kicker">Section 8</div>
  <h2>Exam-day strategy</h2>
  <p class="section-intro">A 90-minute, 75-question paper with +4/−1 is a triage exercise. You cannot solve everything; you must choose what to solve, in what order, and when to leave. The plan below is built for the actual subject mix.</p>

  <h3>The three-pass method</h3>
  <table>
    <thead><tr><th>Pass</th><th>Time</th><th>What to attempt</th><th>Rule</th></tr></thead>
    <tbody>
      <tr><td><b>Pass 1</b></td><td>30–35 min</td><td>TDM, digital, direct DSA/OS facts, easy math.</td><td>If it takes more than 60 seconds, mark and move. Bank the sure shots.</td></tr>
      <tr><td><b>Pass 2</b></td><td>35–40 min</td><td>One/two-step numericals, match/arrange, statement questions.</td><td>Use elimination; write only the essential rough work.</td></tr>
      <tr><td><b>Pass 3</b></td><td>15–20 min</td><td>Flagged questions, educated guesses, review of NOT/units.</td><td>Never leave a question you have eliminated two options on.</td></tr>
    </tbody>
  </table>

  <h3>Recommended attempt order</h3>
  <div class="grid2">
    <div class="box"><h4>If you are strong in math</h4>
      <ol>
        <li>TDM (15–20 Qs, 15 min) — warm-up and confidence.</li>
        <li>Digital (10–13 Qs, 11 min) — high accuracy.</li>
        <li>Math (20–30 Qs, 30 min) — the big block while fresh.</li>
        <li>DSA (10–13 Qs, 13 min).</li>
        <li>OS (9–14 Qs, 12 min).</li>
        <li>Review (9 min).</li>
      </ol>
    </div>
    <div class="box"><h4>If math is your weak area</h4>
      <ol>
        <li>TDM (15–20 Qs, 16 min).</li>
        <li>Digital (10–13 Qs, 11 min).</li>
        <li>DSA (10–13 Qs, 13 min).</li>
        <li>OS (9–14 Qs, 13 min).</li>
        <li>Math (20–30 Qs, 28 min) — attempt the easy 15 first.</li>
        <li>Review (9 min).</li>
      </ol>
    </div>
  </div>

  <h3>The guessing rule (do the maths once)</h3>
  <div class="box dark">
    <p>With four options and +4/−1, a blind guess has expected value <b>0</b>. If you eliminate one option, EV = <b>+0.33</b>; eliminate two, EV = <b>+1.0</b>; eliminate three, mark it. Therefore:</p>
    <ul>
      <li><b>No elimination → leave it.</b> A zero-EV guess adds variance, not marks.</li>
      <li><b>One option eliminated → guess only if you are short on attempts.</b></li>
      <li><b>Two options eliminated → always guess.</b></li>
      <li><b>Three options eliminated → never leave it.</b></li>
    </ul>
  </div>

  <h3>Ten instructions for the hall</h3>
  <ol>
    <li><b>Read the last line first.</b> It tells you whether the question is “which is true”, “which is NOT”, “minimum”, or “arrange”.</li>
    <li><b>Write the subject and formula before solving.</b> Ten seconds of labelling prevents most silly errors.</li>
    <li><b>Use units as a check.</b> ns vs ms, bits vs bytes, degrees vs radians, sq. units.</li>
    <li><b>Do not re-derive standard results.</b> Recall the limit, the derivative, the complexity, the flip-flop table.</li>
    <li><b>For match questions, fix the sure pairs first.</b> The one-to-one constraint usually finishes the rest.</li>
    <li><b>For arrange questions, find first and last.</b> The middle often follows.</li>
    <li><b>For statement questions, mark T/F in the margin.</b> Do not hold four evaluations in your head.</li>
    <li><b>For numericals, estimate before computing.</b> If the options are far apart, approximation is enough.</li>
    <li><b>Never spend more than 2 minutes on one question in Pass 1.</b> The paper is designed to make you do that.</li>
    <li><b>Keep the last 5 minutes for review.</b> Check NOT questions, marking, and that no easy question is blank.</li>
  </ol>

  <div class="box accent">
    <h4>What a top score looks like</h4>
    <p>75 questions, 300 marks. A realistic AIR-1 range is <b>240–270</b>: about 62–68 correct, 3–5 wrong and 4–8 blank. That is not perfection; it is <b>triage plus accuracy</b>. The plan above is designed to get you to 65 attempts with 90% accuracy, not to make you solve every question.</p>
  </div>

  <h3>The final 10-day checklist</h3>
  <table>
    <thead><tr><th>Day</th><th>Focus</th><th>Output</th></tr></thead>
    <tbody>
      <tr><td><b>10</b></td><td>Math mixed set: calculus, coordinate, matrices, algebra</td><td>30 questions + rewrite the formula sheet from memory</td></tr>
      <tr><td><b>9</b></td><td>Digital: number systems, K-map, circuits, memory</td><td>25 questions + one-page error list</td></tr>
      <tr><td><b>8</b></td><td>DSA: complexity, trees, graphs, sorting, hashing</td><td>25 questions + complexity table</td></tr>
      <tr><td><b>7</b></td><td>OS: scheduling, deadlock, paging, EAT, page replacement</td><td>25 questions + all formulas on one page</td></tr>
      <tr><td><b>6</b></td><td>TDM sprint: series, analogy, coding, figures</td><td>40 questions in 35 minutes</td></tr>
      <tr><td><b>5</b></td><td>Full mock #1, strict 90 minutes</td><td>Score + question-level analysis (2 hours)</td></tr>
      <tr><td><b>4</b></td><td>Repair the three weakest topics from the mock</td><td>20 questions per weak topic</td></tr>
      <tr><td><b>3</b></td><td>Full mock #2, strict 90 minutes</td><td>Score + update error log</td></tr>
      <tr><td><b>2</b></td><td>Formula sheet, top traps, 20 TDM questions</td><td>No new topics; only retrieval</td></tr>
      <tr><td><b>1</b></td><td>Light revision, exam logistics, sleep</td><td>No mock; no new material; 7–8 hours sleep</td></tr>
    </tbody>
  </table>
  <p class="small">On exam morning: eat a normal breakfast, carry the admit card and ID, reach the centre early, and do a 5-minute warm-up of easy TDM questions — not a new math chapter.</p>
</div>
""")

# ---------------- APPENDIX A: FORMULAS ----------------
parts.append("""
<div class="section formula" id="sA">
  <div class="kicker">Appendix A</div>
  <h2>Formula and fact sheet</h2>
  <p class="section-intro">The minimum set to revise in the last 48 hours. If a formula is not here, it was not worth memorising for this paper.</p>

  <h3>Mathematics</h3>
  <table>
    <thead><tr><th>Concept</th><th>Formula / fact</th></tr></thead>
    <tbody>
      <tr><td>Quadratic</td><td>Roots of ax²+bx+c=0: x = [−b ± √(b²−4ac)] / 2a; sum = −b/a; product = c/a; real roots ⇔ b²−4ac ≥ 0.</td></tr>
      <tr><td>AP / GP / HP</td><td>AP: aₙ=a+(n−1)d, Sₙ=n/2[2a+(n−1)d]. GP: aₙ=arⁿ⁻¹, Sₙ=a(1−rⁿ)/(1−r), S∞=a/(1−r) for |r|<1. HM: reciprocals are in AP.</td></tr>
      <tr><td>Counting</td><td>nPr = n!/(n−r)!; nCr = n!/[r!(n−r)!]; nC₀=nCn=1; nCr=nC(n−r).</td></tr>
      <tr><td>Probability</td><td>P(A∪B)=P(A)+P(B)−P(A∩B); P(A|B)=P(A∩B)/P(B); Bayes: P(Bᵢ|A)=P(Bᵢ)P(A|Bᵢ)/ΣP(Bⱼ)P(A|Bⱼ).</td></tr>
      <tr><td>Statistics</td><td>Mean = Σx/n; variance = Σ(x−x̄)²/n; SD = √variance; combined mean = (n₁x̄₁+n₂x̄₂)/(n₁+n₂).</td></tr>
      <tr><td>Lines</td><td>Distance = √[(x₂−x₁)²+(y₂−y₁)²]; area = ½|x₁(y₂−y₃)+x₂(y₃−y₁)+x₃(y₁−y₂)|; point-line distance = |ax₀+by₀+c|/√(a²+b²).</td></tr>
      <tr><td>Circle</td><td>x²+y²+2gx+2fy+c=0: centre (−g,−f), radius √(g²+f²−c).</td></tr>
      <tr><td>Parabola</td><td>y²=4ax: focus (a,0), directrix x=−a, latus rectum 4a. x²=4ay: focus (0,a), directrix y=−a.</td></tr>
      <tr><td>Ellipse</td><td>x²/a²+y²/b²=1 (a>b): c²=a²−b², e=c/a, latus rectum 2b²/a; major axis 2a.</td></tr>
      <tr><td>Hyperbola</td><td>x²/a²−y²/b²=1: c²=a²+b², e=c/a, asymptotes y=±(b/a)x; latus rectum 2b²/a.</td></tr>
      <tr><td>Limits</td><td>lim(sinx/x)=1; lim((1−cosx)/x²)=½; lim((eˣ−1)/x)=1; lim(log(1+x)/x)=1; L'Hôpital only for 0/0 or ∞/∞.</td></tr>
      <tr><td>Derivatives</td><td>(sinx)′=cosx; (cosx)′=−sinx; (tanx)′=sec²x; (eˣ)′=eˣ; (lnx)′=1/x; (xⁿ)′=nxⁿ⁻¹.</td></tr>
      <tr><td>Tangents</td><td>Slope at a point = dy/dx; normal slope = −1/(dy/dx); parametric dy/dx=(dy/dt)/(dx/dt).</td></tr>
      <tr><td>Integrals</td><td>∫xⁿdx=xⁿ⁺¹/(n+1)+C; ∫eˣdx=eˣ+C; ∫sinx dx=−cosx+C; ∫cosx dx=sinx+C; ∫1/x dx=ln|x|+C.</td></tr>
      <tr><td>Definite integrals</td><td>∫ₐᵇf(x)dx=∫ₐᵇf(a+b−x)dx; ∫₋ₐᵃf(x)dx=0 if f is odd, 2∫₀ᵃf(x)dx if f is even.</td></tr>
      <tr><td>Matrices</td><td>|kA|=kⁿ|A|; |AB|=|A||B|; A⁻¹=adj(A)/|A|; (AB)ᵀ=BᵀAᵀ; (AB)⁻¹=B⁻¹A⁻¹; trace = Σ eigenvalues; |A| = Π eigenvalues.</td></tr>
    </tbody>
  </table>

  <h3>Digital Fundamentals</h3>
  <table>
    <thead><tr><th>Concept</th><th>Formula / fact</th></tr></thead>
    <tbody>
      <tr><td>2's complement range</td><td>n bits: −2ⁿ⁻¹ to 2ⁿ⁻¹−1.</td></tr>
      <tr><td>Number of states</td><td>n flip-flops → 2ⁿ states; mod-N counter needs ⌈log₂N⌉ flip-flops.</td></tr>
      <tr><td>Hamming distance</td><td>Detect d errors: dmin ≥ d+1. Correct p errors: dmin ≥ 2p+1.</td></tr>
      <tr><td>Multiplexer</td><td>2ⁿ:1 MUX has n select lines; a 2:1 MUX tree for 2ⁿ:1 needs 2ⁿ−1 MUXes.</td></tr>
      <tr><td>Memory capacity</td><td>Capacity = 2^(address lines) × word size; address lines = log₂(number of words).</td></tr>
      <tr><td>K-map</td><td>Groups of 1, 2, 4, 8; Gray-code adjacency; wrap-around allowed; don't-cares can be 0 or 1.</td></tr>
      <tr><td>Flip-flops</td><td>JK: 00 no change, 01 reset, 10 set, 11 toggle. D: next state = D. T: toggle when T=1.</td></tr>
      <tr><td>IEEE 754 single</td><td>1 sign + 8 exponent (bias 127) + 23 mantissa; value = (−1)ˢ × 1.M × 2^(E−127) for normals.</td></tr>
    </tbody>
  </table>

  <h3>Operating Systems</h3>
  <table>
    <thead><tr><th>Concept</th><th>Formula / fact</th></tr></thead>
    <tbody>
      <tr><td>Scheduling</td><td>TAT = CT − AT; WT = TAT − BT; response time = first CPU − AT.</td></tr>
      <tr><td>Deadlock bound</td><td>n processes, each needs at most m units: minimum units to guarantee no deadlock = n(m−1)+1.</td></tr>
      <tr><td>Banker's</td><td>Need = Max − Allocation; a state is safe if a sequence exists that finishes all processes with Available.</td></tr>
      <tr><td>Paging bits</td><td>Offset bits = log₂(page size); page-number bits = log₂(number of pages); virtual bits = page bits + offset; frame bits = log₂(number of frames).</td></tr>
      <tr><td>EAT (page fault)</td><td>EAT = (1−p)·m + p·s, where p = page-fault rate, m = memory access time, s = page-fault service time.</td></tr>
      <tr><td>EAT (TLB)</td><td>EAT = h(t+m) + (1−h)(t+2m), where h = TLB hit ratio, t = TLB lookup time, m = memory access.</td></tr>
      <tr><td>Segmentation</td><td>Physical address = base + offset, provided offset < limit; otherwise trap.</td></tr>
      <tr><td>Disk</td><td>Access time = seek + rotational latency + transfer; rotational latency = ½ rotation for average.</td></tr>
    </tbody>
  </table>

  <h3>Data Structures & Algorithms</h3>
  <table>
    <thead><tr><th>Concept</th><th>Formula / fact</th></tr></thead>
    <tbody>
      <tr><td>Tree invariant</td><td>Any non-empty binary tree: n₀ = n₂ + 1 (leaves = degree-2 nodes + 1).</td></tr>
      <tr><td>Full binary tree</td><td>Height h (root at 0): max nodes = 2^(h+1)−1; max leaves = 2ʰ.</td></tr>
      <tr><td>Heap indices</td><td>1-indexed: parent = ⌊i/2⌋, left = 2i, right = 2i+1. 0-indexed: parent = ⌊(i−1)/2⌋, left = 2i+1, right = 2i+2.</td></tr>
      <tr><td>Graph counts</td><td>Directed adjacency list total length = |E|; undirected = 2|E|; adjacency matrix space = O(V²).</td></tr>
      <tr><td>Master theorem</td><td>T(n)=aT(n/b)+f(n); compare f(n) with n^(log_b a): Case 1/2/3.</td></tr>
      <tr><td>Sorting</td><td>Bubble/selection/insertion O(n²); merge O(n log n); quick avg O(n log n), worst O(n²); heap O(n log n).</td></tr>
      <tr><td>Graph algorithms</td><td>BFS/DFS O(V+E); Dijkstra O((V+E)log V) with heap; Bellman–Ford O(VE); Floyd–Warshall O(V³); Prim O(E log V); Kruskal O(E log E).</td></tr>
      <tr><td>Searching</td><td>Linear O(n); binary O(log n), requires sorted input; hashing average O(1), worst O(n).</td></tr>
    </tbody>
  </table>

  <h3>Thinking & Decision Making: quick rules</h3>
  <table>
    <thead><tr><th>Type</th><th>Rule</th></tr></thead>
    <tbody>
      <tr><td>Number series</td><td>Check differences → ratios → squares/cubes → alternating → operations on previous terms. Verify the rule on every term.</td></tr>
      <tr><td>Letter series</td><td>Write A=1 … Z=26; check gaps; check reverse alphabet; check two interleaved series.</td></tr>
      <tr><td>Analogy</td><td>Say the relation as a sentence (“X is used for Y”); apply the same direction to the second pair.</td></tr>
      <tr><td>Syllogism</td><td>Draw Venn diagrams; “some A are B” does not give “all A are B”; test the conclusion in the most unfavourable diagram.</td></tr>
      <tr><td>Blood relations</td><td>Draw a tree; mark gender; use “only son of my grandfather” to fix the father.</td></tr>
      <tr><td>Direction</td><td>Fix N/E/S/W; right turn = clockwise; use Pythagoras for net displacement.</td></tr>
      <tr><td>Seating</td><td>Start with the most constrained position; use elimination; for circular, fix one person and orient left/right.</td></tr>
      <tr><td>Figure series</td><td>Check rotation, reflection, number of elements, shading, and position separately.</td></tr>
    </tbody>
  </table>

  <h3>Numbers worth memorising</h3>
  <table>
    <thead><tr><th>Set</th><th>Values</th></tr></thead>
    <tbody>
      <tr><td>Powers of 2</td><td>2⁰=1, 2¹=2, 2²=4, 2³=8, 2⁴=16, 2⁵=32, 2⁶=64, 2⁷=128, 2⁸=256, 2⁹=512, 2¹⁰=1024, 2¹¹=2048, 2¹²=4096, 2¹⁶=65,536, 2²⁰≈10⁶, 2³⁰≈10⁹.</td></tr>
      <tr><td>Factorials</td><td>0!=1, 1!=1, 2!=2, 3!=6, 4!=24, 5!=120, 6!=720, 7!=5040, 8!=40,320.</td></tr>
      <tr><td>Squares (11–30)</td><td>121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841, 900.</td></tr>
      <tr><td>Cubes (1–12)</td><td>1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728.</td></tr>
      <tr><td>Logarithms</td><td>log₁₀2=0.3010, log₁₀3=0.4771, log₁₀5=0.6990, log₁₀7=0.8451; ln2=0.6931, ln10=2.3026.</td></tr>
      <tr><td>Primes up to 50</td><td>2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47.</td></tr>
      <tr><td>2's-complement ranges</td><td>4-bit: −8 to +7; 8-bit: −128 to +127; 16-bit: −32,768 to +32,767; 32-bit: −2,147,483,648 to +2,147,483,647.</td></tr>
      <tr><td>Memory units</td><td>1 KB=2¹⁰ B; 1 MB=2²⁰ B; 1 GB=2³⁰ B; 1 ms=10⁶ ns; 1 μs=10³ ns.</td></tr>
    </tbody>
  </table>
  <p class="small">These are the numbers that turn a 90-second calculation into a 20-second recognition. Drill them as flashcards, not as a list to read.</p>
</div>
""")

# ---------------- APPENDIX B: METHOD ----------------
parts.append("""
<div class="section" id="sB">
  <div class="kicker">Appendix B</div>
  <h2>Method and sources</h2>
  <p class="section-intro">This document is evidence-based, not copied from a coaching syllabus. Here is exactly what was used and how the numbers were produced.</p>

  <h3>Primary evidence</h3>
  <table>
    <thead><tr><th>Paper</th><th>File</th><th class="c">Pages</th><th class="c">Questions</th><th>Role</th></tr></thead>
    <tbody>
      <tr><td>2024, 19 March, Shift 3</td><td>SCQP09_2024_March19_Shift3.pdf</td><td class="c">85</td><td class="c">75</td><td>Full classification</td></tr>
      <tr><td>2025, 27 March, Shift 2</td><td>SCQP09_2025_March27_Shift2.pdf</td><td class="c">65</td><td class="c">75</td><td>Full classification</td></tr>
      <tr><td>2026, 11 March, Shift 2</td><td>SCQP09_2026_March11_Shift2.pdf</td><td class="c">64</td><td class="c">75</td><td>Full classification</td></tr>
    </tbody>
  </table>
  <p class="table-note">All three are official NTA papers. The 2022 and 2023 papers were excluded because the pattern changed (100 questions with a Part A general section, then 75 all-domain questions from 2024) and the evidence base for this edition is deliberately 2024–2026.</p>

  <h3>Official syllabus</h3>
  <p>The current NTA SCQP09 syllabus (December 2025) was used for the official-scope check: Thinking &amp; Decision Making, Mathematics, Operating Systems, Data Structures, Digital Fundamentals — plus Computer Networks and DBMS. The 2024–2026 papers measure which of these are actually tested. Source: <span class="small">NTA CUET-PG syllabus, Computer Science and Information Technology (SCQP09).</span></p>

  <h3>How the 225 questions were classified</h3>
  <ol>
    <li><b>Page rendering and OCR.</b> Each page was rendered at 120 dpi; RapidOCR (ONNX Runtime) extracted the question and option text from the embedded images.</li>
    <li><b>Question segmentation.</b> PDF text-layer anchors (“Question Number”) and OCR geometry were combined to split each paper into 75 questions.</li>
    <li><b>Manual classification.</b> Every question was read and assigned to one subject → topic → subtopic. The classification file is kept alongside this document.</li>
    <li><b>Aggregation.</b> Counts were computed directly from the classification, not estimated. The three-year totals sum to 225.</li>
  </ol>

  <h3>Known limitations</h3>
  <ul>
    <li>OCR is reliable for question stems but can garble mathematical notation and Hindi transliteration. Classification was done by reading the question, not by keyword matching alone.</li>
    <li>Some questions are cross-topic (for example, a DSA question using OS scheduling). They were assigned to the dominant concept.</li>
    <li>Format percentages are approximate (keyword tagging plus manual review), and weightage is a three-paper average, not a guarantee.</li>
    <li>The 2026 general-awareness questions are treated as an anomaly because they are absent in 2024 and 2025.</li>
  </ul>

  <h3>How to use this document with the question bank</h3>
  <p>The companion file <b>SCQP09_Question_Bank_2024-2026.csv</b> (and <b>DATA/question_bank_v2.json</b>) contains all 225 questions with year, question number, subject, topic and subtopic. Use it to drill one module at a time: filter by subtopic, attempt the questions, then return to the card and check whether you can explain every bullet under “What to learn”.</p>

  <div class="box dark" style="padding:2.4mm 4mm;margin-bottom:2mm;">
    <h4>The one-sentence summary</h4>
    <p style="margin:0;font-size:8pt;">Master the top 20 modules, keep TDM on a daily drip, train the match/arrange/assertion formats, and protect your time from CN/DBMS and general awareness. That is the whole paper.</p>
  </div>

  <p class="small" style="margin-top:0;font-size:7pt;">Prepared 1 Nov 2026 · Independent analysis of public NTA papers · Not affiliated with NTA · Verify the current syllabus.</p>
</div>
""")

parts.append("</body></html>")

html_doc = "\n".join(parts)
html_path = os.path.join(OUT, "SCQP09_Master_Syllabus.html")
pdf_path = os.path.join(OUT, "SCQP09_Master_Syllabus_2024-2026.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_doc)

if HAS_WEASYPRINT:
    HTML(string=html_doc, base_url=BASE).write_pdf(pdf_path)
    print("Wrote HTML and PDF successfully.")
else:
    print("Wrote HTML successfully. (Note: WeasyPrint is not available; PDF generation skipped.)")

# CSV export
with open(os.path.join(OUT, "SCQP09_Master_Taxonomy.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "subject", "module", "subtopic", "what_to_learn", "how_it_is_asked", "pyq_signal",
                "count_2024", "count_2025", "count_2026", "total", "priority", "official_scope"])
    for r in ROWS:
        w.writerow([r["id"], r["subject"], r["module"], r["title"], r["learn"].replace("|", "; "),
                    r["asked"].replace("|", "; "), r.get("example", ""),
                    r["counts"]["2024"], r["counts"]["2025"], r["counts"]["2026"], r["total"],
                    r["priority"], "Yes"])
print("Wrote CSV")
