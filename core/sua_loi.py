# -*- coding: utf-8 -*-
"""Sửa lỗi chính tả, gõ phím, trình bày và văn bản pháp lý cũ trong nội dung đề cương.
Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật, Công ty CP TEXO Tư vấn và Đầu tư.

- ap_dung(obj): làm sạch dữ liệu thư viện (dict/list/str) theo data/sua_loi_noi_dung.json.
- soi_loi(text): liệt kê lỗi đã biết có trong một văn bản (dùng cho app/skill Kiểm tra đề cương).
Thêm lỗi mới: bổ sung một dòng vào 'thay_cum' trong data/sua_loi_noi_dung.json – không cần sửa code."""
import json
import os
import re
import unicodedata

_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sua_loi_noi_dung.json")
_CHU = "A-Za-zÀ-ỹĐđ"
_CACHE = {}


def _nfc(s):
    return unicodedata.normalize("NFC", s)


def quy_tac():
    if "qt" not in _CACHE:
        d = json.load(open(_F, encoding="utf-8"))
        rules = []
        for r in d.get("thay_cum", []):
            sai, dung = _nfc(r["sai"]), _nfc(r["dung"])
            # luôn khớp trọn từ ở hai đầu để không sửa nhầm vào giữa một từ đúng
            rx = re.compile(rf"(?<![{_CHU}]){re.escape(sai)}(?![{_CHU}])")
            rules.append((rx, dung, r.get("loai", "chinh_ta"), sai))
        d["_rules"] = rules
        d["_xoa"] = {_nfc(x).rstrip(" .;,") for x in d.get("xoa_phan_tu", [])}
        _CACHE["qt"] = d
    return _CACHE["qt"]


def _trinh_bay(s):
    s = re.sub(rf"([,;])(?=[{_CHU}])", r"\1 ", s)                 # thiếu dấu cách sau , ;
    s = re.sub(r"(\d)\s+:\s*(\d{4})\b", r"\1:\2", s)            # TCVN 4453 : 1995 -> TCVN 4453:1995
    s = re.sub(r"(?<=[^\s.:])[ \t]+([,;:])(?=\s|$)", r"\1", s)    # chữ , / chữ ; / chữ :
    s = re.sub(r"(?<=[^\s.])[ \t]+\.(?=\s|$)", ".", s)            # chữ .   (giữ nguyên "...")
    s = re.sub(r"\([ \t]+", "(", s)
    s = re.sub(r"[ \t]+\)", ")", s)
    s = re.sub(r"(?<=\S)[ \t]{2,}(?=\S)", " ", s)
    return s


def sua_chuoi(s, trinh_bay=True):
    if not isinstance(s, str) or not s:
        return s
    s = _nfc(s)
    for rx, dung, _, _ in quy_tac()["_rules"]:
        s = rx.sub(dung, s)
    return _trinh_bay(s) if trinh_bay else s


def ap_dung(obj, _key=None):
    """Làm sạch toàn bộ chuỗi trong obj (trả về bản mới)."""
    qt = quy_tac()
    if isinstance(obj, str):
        return obj if _key in qt.get("khong_sua_khoa", []) else sua_chuoi(obj)
    if isinstance(obj, dict):
        return {k: (v if k in qt.get("khong_sua_khoa", []) else ap_dung(v, k)) for k, v in obj.items()}
    if isinstance(obj, list):
        out = []
        for v in obj:
            if isinstance(v, str) and _nfc(v).rstrip(" .;,") in qt["_xoa"]:
                continue
            v = ap_dung(v, _key)
            if _key in qt.get("bo_phan_tu_trung", []) and isinstance(v, str) and v in out:
                continue
            out.append(v)
        return out
    return obj


def soi_loi(text, toi_da=40):
    """Trả về danh sách lỗi đã biết trong văn bản: [{sai, dung, loai, so_lan}]."""
    text = _nfc(text or "")
    kq = []
    for rx, dung, loai, sai in quy_tac()["_rules"]:
        n = len(rx.findall(text))
        if n:
            kq.append(dict(sai=sai, dung=dung, loai=loai, so_lan=n))
    for m in re.finditer(rf"(?<![{_CHU}])([A-ZĐ])\1(?=[a-zà-ỹđ])", text):          # XXác
        kq.append(dict(sai=text[m.start():m.start() + 6], dung="(thừa chữ hoa đầu từ)", loai="chinh_ta", so_lan=1))
    for m in re.finditer(r"(?<![A-Za-zÀ-ỹĐđ])[a-zđ]([A-ZĐ][a-zà-ỹđ]{2,})", text):   # pChủ
        if m.group() not in ("kWh", "mAh", "eKYC", "iPad", "iPhone", "eBook", "pHmeter"):
            kq.append(dict(sai=m.group(), dung=m.group(1) + " (thừa ký tự đầu)", loai="chinh_ta", so_lan=1))
    return kq[:toi_da]
