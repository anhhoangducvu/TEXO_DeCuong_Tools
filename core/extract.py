# -*- coding: utf-8 -*-
"""Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật, Công ty CP TEXO Tư vấn và Đầu tư.
Đọc đề cương TVGS (.docx / .pdf / nhiều file .docx của một bộ) thành danh sách khối thống nhất.

Khối: {"k": "p", "lvl": 0..9, "t": "...", "img": bool, "num": bool}  hoặc  {"k": "t", "rows": [[[dòng,...], ...], ...]}
lvl > 0 khi đoạn là tiêu đề (Heading n / outline level / mục lục đánh số dạng PHẦN, CHƯƠNG, I., 1., 1.1.)
"""
import io
import os
import re
import subprocess
import tempfile

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROMAN = r"(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV)"
HEAD_RE = [
    (1, re.compile(r"^(PHẦN|Phần)\s+(THỨ\s+\w+|[A-Z0-9IVX]+)\b", re.U)),
    (1, re.compile(r"^(CHƯƠNG|Chương)\s+[0-9IVX]+", re.U)),
    (2, re.compile(r"^" + ROMAN + r"[\.\)]\s+\S", re.U)),
    (2, re.compile(r"^[A-K][\.\)]\s+[A-ZĐÂĂÊÔƠƯÁÀẢÃẠ]", re.U)),
    (3, re.compile(r"^\d{1,2}[\.\)]\s+\S", re.U)),
    (4, re.compile(r"^\d{1,2}\.\d{1,2}\.?\s+\S", re.U)),
    (5, re.compile(r"^\d{1,2}\.\d{1,2}\.\d{1,2}\.?\s+\S", re.U)),
]


def guess_level(text):
    t = text.strip()
    if len(t) > 180 or len(t) < 3:
        return 0
    for lv, rx in HEAD_RE:
        if rx.match(t):
            return lv
    letters = re.sub(r"[^A-Za-zÀ-ỹĐđ]", "", t)
    if len(letters) >= 6 and t.upper() == t and len(t) < 140:
        return 2
    return 0


def _style_level(p):
    st = p.style.name if p.style is not None else ""
    m = re.search(r"[Hh]eading ?(\d)", st) or re.search(r"Tiêu đề ?(\d)", st)
    if m:
        return int(m.group(1))
    ol = p._p.find(".//" + qn("w:outlineLvl"))
    if ol is not None:
        v = int(ol.get(qn("w:val")))
        if v < 9:
            return v + 1
    if st.lower().startswith("toc") or st.lower().startswith("mục lục"):
        return -1                       # dòng mục lục
    return 0


def _cell_lines(c):
    return [p.text.strip() for p in c.paragraphs if p.text.strip()]


def _table_rows(tb):
    rows = []
    for r in tb.rows:
        cells, prev = [], None
        for c in r.cells:
            if c._tc is prev:
                continue
            prev = c._tc
            cells.append(_cell_lines(c))
        rows.append(cells)
    return rows


def read_docx(src):
    d = Document(src)
    blocks = []
    for ch in d.element.body.iterchildren():
        if ch.tag == qn("w:p"):
            p = Paragraph(ch, d)
            t = p.text.strip()
            img = bool(ch.findall(".//" + qn("w:drawing")) or ch.findall(".//" + qn("w:pict")))
            if not t and not img:
                continue
            lv = _style_level(p)
            if lv == -1:
                blocks.append(dict(k="p", lvl=0, t=t, img=img, toc=True))
                continue
            if lv == 0:
                lv = guess_level(t) if not img else 0
                soft = True
            else:
                soft = False
            blocks.append(dict(k="p", lvl=lv, t=t, img=img, soft=soft,
                               num=ch.find(".//" + qn("w:numPr")) is not None))
        elif ch.tag == qn("w:tbl"):
            try:
                rows = _table_rows(Table(ch, d))
            except Exception:
                rows = []
            img = bool(ch.findall(".//" + qn("w:drawing")) or ch.findall(".//" + qn("w:pict")))
            blocks.append(dict(k="t", rows=rows, img=img))
    meta = dict(sections=len(d.sections), images=sum(1 for b in blocks if b.get("img")),
                tables=sum(1 for b in blocks if b["k"] == "t"))
    try:
        s0 = d.sections[0]
        meta["page"] = (round(s0.page_width.cm, 1), round(s0.page_height.cm, 1))
    except Exception:
        pass
    return blocks, meta


def read_pdf(src):
    """PDF: dùng pdftotext (giữ dòng), nhận tiêu đề bằng mẫu đánh số."""
    with tempfile.TemporaryDirectory() as td:
        p = src
        if not isinstance(src, str):
            p = os.path.join(td, "in.pdf")
            open(p, "wb").write(src.read())
        out = os.path.join(td, "o.txt")
        subprocess.run(["pdftotext", p, out], check=False)
        txt = open(out, encoding="utf-8", errors="ignore").read() if os.path.exists(out) else ""
        try:
            info = subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout
            pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
        except Exception:
            pages = 0
    blocks = []
    for line in txt.splitlines():
        t = re.sub(r"\s+", " ", line).strip()
        if not t or re.fullmatch(r"\d{1,3}", t):
            continue
        blocks.append(dict(k="p", lvl=guess_level(t), t=t, img=False, soft=True))
    return blocks, dict(pages=pages, images=0, tables=0)


def read_any(files):
    """files: list[(name, bytes|path)] — nhiều file của cùng một bộ được nối theo thứ tự tên."""
    allb, meta = [], dict(files=[], images=0, tables=0, pages=0)
    for name, data in sorted(files, key=lambda x: x[0]):
        ext = os.path.splitext(name)[1].lower()
        if ext not in (".pdf", ".docx", ".docm"):
            head = (open(data, "rb").read(5) if isinstance(data, str) else bytes(data[:5]))
            ext = ".pdf" if head.startswith(b"%PDF") else (".docx" if head.startswith(b"PK") else ext)
        src = data if isinstance(data, str) else io.BytesIO(data)
        if ext == ".pdf":
            b, m = read_pdf(src)
        elif ext in (".docx", ".docm"):
            b, m = read_docx(src)
        else:
            continue
        allb.extend(b)
        meta["files"].append(name)
        for k in ("images", "tables", "pages"):
            meta[k] += m.get(k, 0) or 0
        meta.setdefault("page", m.get("page"))
    return allb, meta


def full_text(blocks):
    out = []
    for b in blocks:
        if b["k"] == "p":
            out.append(b["t"])
        else:
            for r in b["rows"]:
                out.append(" | ".join(" ".join(c) for c in r))
    return "\n".join(out)


def headings(blocks):
    return [b["t"] for b in blocks if b["k"] == "p" and b.get("lvl", 0) > 0]


def word_count(blocks):
    return len(full_text(blocks).split())
