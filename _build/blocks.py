# -*- coding: utf-8 -*-
"""Bước 1 dựng thư viện: đọc mọi đề cương .docx trong thư mục nguồn thành khối JSON (_build/_blocks).
Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật TEXO."""
import os, re, json, glob, sys
from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.table import Table
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
ROOT = _os.path.dirname(HERE)
SRC_DIR = _os.environ.get("DC_SRC") or _os.path.dirname(ROOT)   # thư mục chứa các đề cương nguồn (mặc định: thư mục cha của bộ công cụ)
BLOCKS = _os.path.join(HERE, "_blocks")
DATA = _os.path.join(ROOT, "core", "data")
SRC=SRC_DIR; OUT=BLOCKS; _os.makedirs(OUT, exist_ok=True)
def cell_lines(c):
    out=[]
    for p in c.paragraphs:
        t=p.text.strip()
        if t: out.append(t)
    return out
def table_rows(tb):
    rows=[]
    for r in tb.rows:
        cells=[]; prev=None
        for c in r.cells:
            if c._tc is prev: continue
            prev=c._tc; cells.append(cell_lines(c))
        rows.append(cells)
    return rows
def level(p):
    st=p.style.name if p.style is not None else ''
    m=re.search(r'[Hh]eading ?(\d)',st)
    if m: return int(m.group(1))
    ol=p._p.find('.//'+qn('w:outlineLvl'))
    if ol is not None:
        v=int(ol.get(qn('w:val')))
        if v<9: return v+1
    return 0
for f in sorted(x for x in glob.glob(SRC+"/**/*.docx", recursive=True) if "TEXO_DeCuong_Tools" not in x and not _os.path.basename(x).startswith("~$")):
    d=Document(f); rel=os.path.relpath(f,SRC); blocks=[]
    for ch in d.element.body.iterchildren():
        if ch.tag==qn('w:p'):
            p=Paragraph(ch,d); t=p.text.strip()
            img=bool(ch.findall('.//'+qn('w:drawing')) or ch.findall('.//'+qn('w:pict')))
            if not t and not img: continue
            blocks.append(dict(k='p',lvl=level(p),st=(p.style.name if p.style is not None else ''),
                               num=ch.find('.//'+qn('w:numPr')) is not None,t=t,img=img))
        elif ch.tag==qn('w:tbl'):
            try: blocks.append(dict(k='t',rows=table_rows(Table(ch,d))))
            except Exception as e: blocks.append(dict(k='t',rows=[],err=str(e)))
    name=rel.replace('\\','/').replace('/','__').replace('.docx','')
    json.dump(blocks,open(f"{OUT}/{name}.json","w"),ensure_ascii=False)
    print(rel,len(blocks))
