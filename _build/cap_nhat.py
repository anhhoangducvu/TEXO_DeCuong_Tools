# -*- coding: utf-8 -*-
"""CƠ CHẾ CẬP NHẬT bộ công cụ Đề cương TVGS – Người xây dựng: Hoàng Đức Vũ (Trưởng phòng Kỹ thuật TEXO).

Lệnh:
  python _build/cap_nhat.py quet                 # dò đề cương mới trong thư mục nguồn, chấm theo khung, ghi sổ nguồn + báo cáo
  python _build/cap_nhat.py dung-lai             # dựng lại thư viện hạng mục + mục nâng cao từ đề cương nguồn
  python _build/cap_nhat.py dong-bo "nội dung"   # tăng phiên bản, ghi CHANGELOG, chép lõi sang 2 skill, đóng gói .skill
Biến môi trường DC_SRC: thư mục đề cương nguồn (mặc định: thư mục cha của bộ công cụ).
"""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.environ.get("DC_SRC") or os.path.dirname(ROOT)
DATA = os.path.join(ROOT, "core", "data")
SO_NGUON = os.path.join(HERE, "so_de_cuong_nguon.json")
SKILLS = os.path.join(ROOT, "_skills")
sys.path.insert(0, ROOT)


def _files():
    out = []
    for r, ds, fs in os.walk(SRC):
        if "TEXO_DeCuong_Tools" in r:
            continue
        docx = [f for f in fs if f.lower().endswith(".docx") and not f.startswith("~$")]
        # thư mục con chứa nhiều file của 1 bộ đề cương → gộp 1 bộ
        if r != SRC and docx:
            out.append((os.path.relpath(r, SRC), [os.path.join(r, f) for f in sorted(docx)]))
            continue
        for f in fs:
            p = os.path.join(r, f)
            if f.startswith("~$") or os.path.isdir(p):
                continue
            head = open(p, "rb").read(5)
            if f.lower().endswith((".docx", ".pdf")) or head.startswith((b"%PDF", b"PK")):
                out.append((f, [p]))
    return out


def quet():
    from core import checker
    so = json.load(open(SO_NGUON, encoding="utf-8")) if os.path.exists(SO_NGUON) else {}
    moi = []
    for ten, fs in _files():
        key = ten
        mt = max(os.path.getmtime(f) for f in fs)
        if key in so and so[key].get("mtime") == mt:
            continue
        r = checker.check_files([(os.path.basename(f) if os.path.splitext(f)[1] else os.path.basename(f) + ".pdf", f) for f in fs], {})
        tt = re.match(r"^(TT\s?\d{1,2})", ten)
        so[key] = dict(trung_tam=tt.group(1).replace(" ", "") if tt else "", mtime=mt, ngay_quet=dt.date.today().isoformat(),
                       mau=r["muc_mau"], diem=r["diem"], van_ban_2026=sum(r["phap_ly"]["co_moi"].values()),
                       het_hieu_luc=[h["ten"] for h in r["phap_ly"]["het"]],
                       hang_muc=[h["id"] for h in r["hang_muc"] if h["trang_thai"].startswith("Có mục")],
                       da_dua_vao_thu_vien=so.get(key, {}).get("da_dua_vao_thu_vien", False))
        moi.append(key)
    json.dump(so, open(SO_NGUON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    lines = [f"# Sổ đề cương nguồn – quét ngày {dt.date.today():%d/%m/%Y}", "",
             "| Bộ đề cương | Đơn vị | Mẫu | Điểm | VB 2026 | Còn VB hết hiệu lực | Đã vào thư viện | Mới |", "|---|---|---|---|---|---|---|---|"]
    for k, v in sorted(so.items()):
        lines.append(f"| {k} | {v['trung_tam']} | {v['mau']} | {v['diem']} | {v['van_ban_2026']} | {len(v['het_hieu_luc'])} | "
                     f"{'✓' if v['da_dua_vao_thu_vien'] else ''} | {'MỚI' if k in moi else ''} |")
    open(os.path.join(HERE, "BAO_CAO_NGUON.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"Đã quét {len(so)} bộ, mới/đổi: {len(moi)}")
    for k in moi:
        print("  +", k, so[k]["diem"], so[k]["mau"])


def dung_lai():
    for s in ("blocks.py", "build_library.py", "build_snippets.py"):
        print(">>", s)
        subprocess.run([sys.executable, os.path.join(HERE, s)], check=True)


def dong_bo(noi_dung, muc="patch"):
    vf = os.path.join(DATA, "VERSION.json")
    v = json.load(open(vf, encoding="utf-8"))
    a, b, c = [int(x) for x in v["phien_ban"].split(".")]
    a, b, c = (a + 1, 0, 0) if muc == "major" else (a, b + 1, 0) if muc == "minor" else (a, b, c + 1)
    v["phien_ban"], v["ngay"] = f"{a}.{b}.{c}", dt.date.today().isoformat()
    if os.path.exists(SO_NGUON):
        v["so_de_cuong_nguon"] = len(json.load(open(SO_NGUON, encoding="utf-8")))
    json.dump(v, open(vf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cl = os.path.join(ROOT, "CHANGELOG.md")
    old = open(cl, encoding="utf-8").read() if os.path.exists(cl) else "# Nhật ký phiên bản – Bộ công cụ Đề cương TVGS\n"
    head, _, rest = old.partition("\n## ")
    entry = f"\n## {v['phien_ban']} – {dt.date.today():%d/%m/%Y}\n- {noi_dung}\n"
    open(cl, "w", encoding="utf-8").write(head.rstrip() + "\n" + entry + (("\n## " + rest) if rest else ""))
    # chép lõi sang các skill và đóng gói
    for sk in sorted(os.listdir(SKILLS)) if os.path.isdir(SKILLS) else []:
        sd = os.path.join(SKILLS, sk)
        dst = os.path.join(sd, "scripts", "core")
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(ROOT, "core"), dst, ignore=shutil.ignore_patterns("__pycache__", "ui.py"))
        open(os.path.join(sd, "VERSION"), "w").write(v["phien_ban"] + "\n")
        out = os.path.join(ROOT, sk + ".skill")
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for r, ds, fs in os.walk(sd):
                ds[:] = [d for d in ds if d != "__pycache__"]
                for f in fs:
                    p = os.path.join(r, f)
                    z.write(p, os.path.relpath(p, SKILLS))
        print("Đóng gói", out)
    print("Phiên bản mới:", v["phien_ban"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "quet":
        quet()
    elif cmd == "dung-lai":
        dung_lai()
    elif cmd == "dong-bo":
        dong_bo(sys.argv[2] if len(sys.argv) > 2 else "Cập nhật dữ liệu", sys.argv[3] if len(sys.argv) > 3 else "patch")
    else:
        print(__doc__)
