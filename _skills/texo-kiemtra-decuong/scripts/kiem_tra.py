# -*- coding: utf-8 -*-
"""Kiểm tra đề cương TVGS từ dòng lệnh.
Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật, Công ty CP TEXO Tư vấn và Đầu tư.
python scripts/kiem_tra.py <file1.docx|pdf> [file2 ...] [--mau "Cơ bản|Nâng cao"] [--ten "Tên dự án"] [--cdt "Chủ đầu tư"]
        [--hang-muc EPCOC,BTCT] [--out phieu.docx] [--json ketqua.json] [--nguoi "Người kiểm tra"]
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import checker, report

ap = argparse.ArgumentParser()
ap.add_argument("files", nargs="+")
ap.add_argument("--mau"); ap.add_argument("--ten", default=""); ap.add_argument("--cdt", default="")
ap.add_argument("--hang-muc", default=""); ap.add_argument("--out"); ap.add_argument("--json"); ap.add_argument("--nguoi", default="")
ap.add_argument("--don-vi", default="")
a = ap.parse_args()
opts = {"ten_du_an": a.ten, "chu_dau_tu": a.cdt, "hang_muc": [x for x in a.hang_muc.split(",") if x]}
if a.mau:
    opts["muc_mau"] = a.mau
res = checker.check_files([(os.path.basename(f), f) for f in a.files], opts)
todo = report.viec_phai_lam(res)
print(f"Mẫu: {res['muc_mau']} (tự nhận {res['muc_mau_tu_nhan']}) · Điểm khung: {res['diem']}/100 · {res['ket_luan']}")
for m, nd, ht, yc in todo:
    print(f"  [{report.MD[m]}] {nd} | {ht} | {yc}")
if a.json:
    json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
if a.out:
    report.make_report(res, {"ten": a.ten or os.path.splitext(os.path.basename(a.files[0]))[0], "don_vi": a.don_vi}, a.out, a.nguoi)
    print("Phiếu:", a.out)

from core import version as _V
print("⚖️ ", _V.LEGAL_NOTE)
