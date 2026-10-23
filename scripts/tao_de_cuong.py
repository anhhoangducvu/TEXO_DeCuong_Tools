# -*- coding: utf-8 -*-
"""Tạo đề cương TVGS từ file thông tin dự án (JSON).
Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật, Công ty CP TEXO Tư vấn và Đầu tư.
python scripts/tao_de_cuong.py thong_tin.json out.docx [--mau "Cơ bản|Nâng cao"]
JSON mẫu: xem scripts/thong_tin_mau.json. Bỏ trống "hang_muc"/"nhan_su" để dùng gợi ý theo quy mô.
"""
import argparse, datetime as dt, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import generator as G, checker

ap = argparse.ArgumentParser()
ap.add_argument("info"); ap.add_argument("out"); ap.add_argument("--mau")
a = ap.parse_args()
info = json.load(open(a.info, encoding="utf-8"))
if isinstance(info.get("ngay"), str) and info["ngay"]:
    info["ngay"] = dt.date.fromisoformat(info["ngay"])
level = a.mau or info.get("mau") or G.de_xuat_muc_mau(info)[0]
mods = info.get("hang_muc") or G.de_xuat_hang_muc(info)
staff = info.get("nhan_su") or G.de_xuat_nhan_su(info, mods, level)
G.generate(info, level, mods, staff, a.out)
r = checker.check_files([(os.path.basename(a.out), a.out)], {"muc_mau": level, "hang_muc": mods})
print(f"Đã tạo {a.out} · mẫu {level} · {len(mods)} hạng mục · tự kiểm {r['diem']}/100 · {r['ket_luan']}")
print("Lý do chọn mẫu:", G.de_xuat_muc_mau(info)[1])

from core import version as _V
print("⚖️ ", _V.LEGAL_NOTE)
