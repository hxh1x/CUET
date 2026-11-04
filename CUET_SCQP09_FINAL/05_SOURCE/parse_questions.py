#!/usr/bin/env python3
"""Parse OCR output + PDF text anchors of CUET-PG SCQP09 papers into a question bank."""
import json
import os
import re
import sys

import pymupdf as fitz

OCR_DIR = "ocr"
OUT = "questions.json"
DPI = {"2022": 150, "2023": 150, "2023b": 150, "2024": 120, "2025": 120, "2026": 120}
PDF = {
    "2022": "raw/SCQP09_2022_PGQP26.pdf",
    "2023": "raw/SCQP09_2023_June07_Shift2.pdf",
    "2023b": "raw/SCQP09_2023_June16_Shift3.pdf",
    "2024": "raw/SCQP09_2024_March19_Shift3.pdf",
    "2025": "raw/SCQP09_2025_March27_Shift2.pdf",
    "2026": "raw/SCQP09_2026_March11_Shift2.pdf",
}

META = re.compile(
    r"^(Question Number|Question Id|Question Type|Question Mandatory|Correct Marks|Wrong Marks|"
    r"Instruction Time|Options\s*:|Section|Group|Duration|Total Marks|Display Marks|"
    r"National Testing|Question Paper Name|Subject Name|Creation Date|Sub-Section|"
    r"Maximum Instruction|Mandatory or Optional|Number of Questions|Section Marks|"
    r"Enable Mark|Clear Response|Question Shuffling|Is Section|Is this Group|Examiner|"
    r"Show Attended|Show Progress|Break time|Group Maximum|Group Minimum|Group Marks)",
    re.I,
)
OPTID = re.compile(r"^\d{5,}\s*\.\s*\d\s*$")
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
HEAD_Q = re.compile(r"Question\s*Number\s*[:\-]?\s*(\d+)", re.I)
HEAD_SL = re.compile(r"Sl\.?\s*No\.?\s*[:\-]?\s*(\d+)", re.I)


def latin_ratio(s):
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if "a" <= c.lower() <= "z") / len(letters)


def garbage(s):
    toks = s.split()
    if len(toks) >= 4 and sum(1 for t in toks if len(t) == 1) / len(toks) > 0.3:
        return True
    letters = [c.lower() for c in s if c.isalpha()]
    if len(letters) > 8:
        vowels = sum(1 for c in letters if c in "aeiou")
        if vowels / len(letters) < 0.18:
            return True
    return False


def load_pages(year):
    rows = []
    path = os.path.join(OCR_DIR, f"{year}.jsonl")
    if not os.path.exists(path):
        return rows
    for line in open(path):
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    rows.sort(key=lambda r: r["page"])
    return rows


def lines_of(page):
    items = sorted(page["items"], key=lambda d: (d["y"], d["x"]))
    lines, cur = [], []
    for it in items:
        if not cur:
            cur = [it]
            continue
        prev = cur[-1]
        if abs(it["y"] - prev["y"]) <= 8 and it["x"] - prev["x1"] < 40:
            cur.append(it)
        else:
            lines.append(cur)
            cur = [it]
    if cur:
        lines.append(cur)
    return [" ".join(i["t"] for i in sorted(ln, key=lambda d: d["x"])) for ln in lines]


def clean_line(s):
    s = s.replace("\u00a0", " ").strip()
    s = re.sub(r"\s+", " ", s)
    if not s or len(s) < 2:
        return ""
    if OPTID.match(s) or META.match(s):
        return ""
    if DEVANAGARI.search(s) and latin_ratio(s) < 0.55:
        return ""
    if garbage(s):
        return ""
    return s


def anchors(year):
    """Return {page_number: [(y_px, qno), ...]} from PDF text layer, fallback OCR headers."""
    doc = fitz.open(PDF[year])
    dpi = DPI[year]
    scale = dpi / 72.0
    out = {}
    for i, page in enumerate(doc):
        found = []
        text = page.get_text("blocks")
        for b in text:
            t = b[4].replace("\n", " ")
            m = HEAD_Q.search(t) or HEAD_SL.search(t)
            if m:
                found.append((b[1] * scale, int(m.group(1))))
        if not found:
            # fallback: OCR lines with headers
            path = os.path.join(OCR_DIR, f"{year}.jsonl")
            if os.path.exists(path):
                for line in open(path):
                    row = json.loads(line)
                    if row["page"] == i + 1:
                        for it in row["items"]:
                            m = HEAD_Q.search(it["t"]) or HEAD_SL.search(it["t"])
                            if m:
                                found.append((it["y"], int(m.group(1))))
        # unique by qno, keep smallest y
        best = {}
        for y, n in found:
            if n not in best or y < best[n]:
                best[n] = y
        out[i + 1] = sorted((y, n) for n, y in best.items())
    return out


def parse(year):
    pages = load_pages(year)
    anc = anchors(year)
    groups, order = {}, []
    cur = None

    def add(n, line):
        nonlocal cur
        if n not in groups:
            groups[n] = []
            order.append(n)
        cur = n
        groups[n].append(line)

    for p in pages:
        pno = p["page"]
        page_anchors = anc.get(pno, [])
        items = sorted(p["items"], key=lambda d: (d["y"], d["x"]))
        line_groups, curline = [], []
        for it in items:
            if not curline:
                curline = [it]
                continue
            prev = curline[-1]
            if abs(it["y"] - prev["y"]) <= 8 and it["x"] - prev["x1"] < 40:
                curline.append(it)
            else:
                line_groups.append(curline)
                curline = [it]
        if curline:
            line_groups.append(curline)
        for ln in line_groups:
            ly = min(i["y"] for i in ln)
            text = " ".join(i["t"] for i in sorted(ln, key=lambda d: d["x"]))
            qn = None
            for ay, an in page_anchors:
                if ay <= ly + 6:
                    qn = an
            if qn is not None:
                cur = qn
            c = clean_line(text)
            if c and cur is not None:
                add(cur, c)
    # dedupe
    qs = []
    for n in sorted(groups):
        seen, lines = set(), []
        for ln in groups[n]:
            key = re.sub(r"\W+", "", ln.lower())
            if not key or key in seen:
                continue
            if any(key in re.sub(r"\W+", "", x.lower()) for x in lines):
                continue
            seen.add(key)
            lines.append(ln)
        text = re.sub(r"\s+", " ", " ".join(lines)).strip()
        qs.append({"year": year, "qno": n, "text": text, "lines": lines})
    return qs


if __name__ == "__main__":
    years = sys.argv[1].split(",") if len(sys.argv) > 1 else ["2022", "2023", "2023b", "2024", "2025", "2026"]
    allq = []
    for y in years:
        qs = parse(y)
        print(f"{y}: {len(qs)} questions", flush=True)
        allq += qs
    json.dump(allq, open(OUT, "w"), indent=1)
    print("wrote", OUT, len(allq))
