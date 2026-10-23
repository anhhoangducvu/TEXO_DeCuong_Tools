# -*- coding: utf-8 -*-
"""Thông tin phiên bản bộ công cụ đề cương TVGS – Người xây dựng: Hoàng Đức Vũ (Trưởng phòng Kỹ thuật TEXO)."""
import json
import os

_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def info():
    v = json.load(open(os.path.join(_D, "VERSION.json"), encoding="utf-8"))
    pl = json.load(open(os.path.join(_D, "phap_ly.json"), encoding="utf-8"))
    v["phap_ly_ngay"] = pl.get("ngay_cap_nhat", "")
    return v


AUTHOR = "Hoàng Đức Vũ – Trưởng phòng Kỹ thuật"
LEGAL_NOTE = ("Bắt buộc rà soát văn bản pháp luật, tiêu chuẩn viện dẫn bằng công cụ TEXO Legal Reviewer "
              "để bảo đảm dùng phiên bản mới nhất trước khi trình ký, phát hành.")
