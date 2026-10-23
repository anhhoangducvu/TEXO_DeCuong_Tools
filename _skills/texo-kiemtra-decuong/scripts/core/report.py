# -*- coding: utf-8 -*-
"""Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật, Công ty CP TEXO Tư vấn và Đầu tư.
Xuất phiếu kiểm tra đề cương TVGS (Word, mẫu trình bày TEXO – Phòng Kỹ thuật)."""
import datetime as dt

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from . import texo_docx_kit as K

K.SEV.update({"Phải xử lý": ("🔴", K.C["red"], K.C["redBg"]), "Nên xử lý": ("🟠", K.C["orange"], K.C["orangeBg"]),
              "Đạt": ("🟢", K.C["green"], K.C["greenBg"]), "Lưu ý": ("🔵", K.C["blue"], K.C["label"])})
MD = {"high": "Phải xử lý", "mid": "Nên xử lý", "ok": "Đạt", "info": "Lưu ý"}


def _fix(r):
    return {"Thiếu": "Bổ sung mục riêng theo khung chuẩn", "Có, chưa thành mục": "Tách thành tiêu đề riêng, viết đầy đủ nội dung",
            "Có, chưa đủ": "Bổ sung phần còn thiếu"}.get(r["trang_thai"], "")


def viec_phai_lam(res):
    out = []
    for r in res["tieu_chi"]:
        if r["muc_do"] in ("high", "mid"):
            out.append((r["muc_do"], f"{r['id']} – {r['ten']}", (r.get("bang_chung") or r["trang_thai"]), _fix(r)))
    for h in res["hang_muc"]:
        if h["muc_do"] in ("high", "mid"):
            out.append((h["muc_do"], f"Hạng mục: {h['ten']}", h["trang_thai"], "Bổ sung mục giám sát chi tiết (bảng nội dung – phương pháp – tiêu chuẩn – hồ sơ)"))
    for x in res["phap_ly"]["het"]:
        out.append((x["muc_do"], f"Căn cứ hết hiệu lực: {x['ten']}", f"Viện dẫn {x['so_lan']} lần", "Thay bằng " + x["thay_the"]))
    cl = res["chat_luong"]
    if cl["nghi_lan_ten"]:
        out.append(("high", "Thông tin dự án/Chủ đầu tư không thống nhất", "; ".join(cl["nghi_lan_ten"][:3]), "Rà soát, sửa đúng tên dự án/CĐT của gói thầu (nghi chép từ đề cương khác)"))
    if cl["so_cho_trong"]:
        out.append(("mid", "Còn chỗ trống, ký hiệu chờ điền", f"{cl['so_cho_trong']} vị trí", "Điền đầy đủ thông tin hoặc xóa"))
    out.sort(key=lambda x: {"high": 0, "mid": 1}.get(x[0], 2))
    return out


def make_report(res, meta_info, out_path, nguoi_kiem_tra="", nguoi_duyet=None, ai=None):
    """nguoi_duyet: (chức danh, họ tên) – mặc định Trưởng phòng Kỹ thuật. ai: kết quả core.ai.kiem_tra (data) nếu có."""
    d = Document()
    s0 = d.sections[0]
    ten = (meta_info.get("ten") or "Đề cương TVGS")[:40]
    content = K.setup_section(s0, "A4P", "PHIẾU KIỂM TRA ĐỀ CƯƠNG TVGS", ten,
                              "Tài liệu nội bộ · Phiếu kiểm tra đề cương TVGS")
    K.para(d, "PHIẾU KIỂM TRA ĐỀ CƯƠNG TƯ VẤN GIÁM SÁT", 16, b=True, c=K.C["navy"], align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    K.para(d, meta_info.get("ten") or "", 12, i=True, c=K.C["grey"], align=WD_ALIGN_PARAGRAPH.CENTER, after=8)
    K.meta_table(d, [("Đề cương / dự án", meta_info.get("ten") or ""), ("Đơn vị lập", meta_info.get("don_vi") or ""),
                     ("File kiểm tra", ", ".join(res.get("files", []))[:300]),
                     ("Mẫu áp dụng", f"{res['muc_mau']} (công cụ tự nhận: {res['muc_mau_tu_nhan']})"),
                     ("Thời điểm lập đề cương", res.get("ngay") or "Không xác định trên bìa"),
                     ("Ngày kiểm tra", dt.date.today().strftime("%d/%m/%Y"))], content, 0.3)
    K.spacer(d, 6)
    todo = viec_phai_lam(res)
    n_high = sum(1 for x in todo if x[0] == "high")
    hm_ok = sum(1 for h in res["hang_muc"] if h["trang_thai"].startswith("Có mục"))
    col = {"green": "green", "orange": "orange", "red": "red"}[res["mau"]]
    K.kpi_row(d, [(f"{res['diem']}", "Điểm khung", "/100 theo mẫu " + res["muc_mau"], col),
                  (str(n_high), "Phải xử lý", "trước khi trình ký", "red" if n_high else "green"),
                  (str(hm_ok), "Hạng mục chi tiết", f"có mục giám sát riêng", "blue"),
                  (str(len(res["phap_ly"]["het"])), "Căn cứ hết hiệu lực", "loại văn bản", "red" if res["phap_ly"]["het"] else "green")], content)
    K.spacer(d, 6)
    lines = [f"Kết luận: {res['ket_luan']}."]
    if todo:
        lines.append("Các việc cần xử lý chính: " + "; ".join(x[1] for x in todo[:5]) + ".")
    lines.append("Lưu ý bắt buộc: trước khi trình ký, rà soát văn bản pháp luật, tiêu chuẩn viện dẫn bằng công cụ TEXO Legal Reviewer để bảo đảm dùng phiên bản mới nhất.")
    K.callout(d, "KẾT LUẬN", lines, content, color=col if col != "green" else "green")
    K.spacer(d, 8)

    K.h1(d, "1. Việc cần xử lý trước khi trình ký")
    if todo:
        K.data_table(d, [450, 2900, 2200, 2226, 1250], ["#", "Nội dung", "Hiện trạng", "Yêu cầu sửa", "Mức độ"],
                     [[str(k + 1), x[1], x[2], x[3], MD[x[0]]] for k, x in enumerate(todo)], size=9.5, sev_col=4, center_cols=(0,))
    else:
        K.para(d, "Không có việc phải xử lý.", 11.5)

    if ai:
        K.h1(d, "1b. Nhận xét chuyên môn (AI hỗ trợ)")
        if ai.get("nhan_xet_chung"):
            K.para(d, ai["nhan_xet_chung"], 11)
        ph = [x for x in ai.get("phat_hien", []) if isinstance(x, dict)]
        if ph:
            K.data_table(d, [450, 3300, 4026, 1250], ["#", "Phát hiện / vị trí", "Đề xuất sửa", "Mức độ"],
                         [[str(k + 1), [x.get("noi_dung", ""), {"text": x.get("vi_tri", ""), "i": True, "size": 9, "c": K.C["grey"]}],
                           x.get("de_xuat", ""), MD.get(x.get("muc_do"), "Lưu ý")] for k, x in enumerate(ph)], size=9.5, sev_col=3, center_cols=(0,))
        tot = [x for x in ai.get("diem_tot", []) if isinstance(x, str)]
        if tot:
            K.para(d, "Điểm làm tốt: " + "; ".join(tot), 10.5, i=True)
        K.para(d, "Nhận xét do AI gợi ý trên nền kết quả đối chiếu; người kiểm tra thẩm định lại trước khi dùng.", 9, i=True, c=K.C["grey"])
    K.h1(d, "2. Đối chiếu khung chuẩn đề cương TVGS")
    nhom = {n["id"]: n["ten"] for n in res["nhom"]}
    rows = []
    cur = None
    for r in res["tieu_chi"]:
        if r["nhom"] != cur:
            cur = r["nhom"]
            rows.append([{"text": nhom[cur], "b": True}, "", "", "", ""])
        rows.append([r["id"], r["ten"], "Bắt buộc" if r["cap"] == "B" else "Nâng cao",
                     r["trang_thai"] + (f" – {r['bang_chung']}" if r.get("bang_chung") else ""), MD[r["muc_do"]]])
    t = K.data_table(d, [650, 3200, 900, 3026, 1250], ["Mã", "Tiêu chí", "Cấp", "Kết quả / bằng chứng", "Mức độ"],
                     rows, size=9, sev_col=4)
    # tô hàng nhóm
    for i, r in enumerate(rows, 1):
        if not r[4]:
            row = t.rows[i]
            c = row.cells[0].merge(row.cells[4])
            K.shade(c, K.C["label"])
            for p in c.paragraphs[1:]:
                p._p.getparent().remove(p._p)

    K.h1(d, "3. Hạng mục công tác – đề cương chi tiết")
    if res["hang_muc"]:
        K.data_table(d, [2800, 1250, 2700, 1026, 1250], ["Hạng mục", "Nhóm", "Hiện trạng / mục tìm thấy", "Cần có", "Mức độ"],
                     [[h["ten"], h["nhom"], h["trang_thai"] + (f": {h['bang_chung']}" if h["bang_chung"] else ""),
                       "Có" if h["can_co"] else "—", MD[h["muc_do"]]] for h in res["hang_muc"]], size=9, sev_col=4)
    K.h1(d, "4. Căn cứ pháp lý")
    pl = res["phap_ly"]
    K.para(d, "Văn bản mới đã viện dẫn: " + ", ".join(f"{k} {'✓' if v else '✗'}" for k, v in pl["co_moi"].items()), 11)
    rows = [[x["ten"], str(x["so_lan"]), "Thay bằng " + x["thay_the"], MD[x["muc_do"]]] for x in pl["het"]] + \
           [[x["ten"], str(x["so_lan"]), x["ly_do"], "Lưu ý"] for x in pl["ra_soat"]]
    if rows:
        K.data_table(d, [2600, 650, 4526, 1250], ["Văn bản", "Số lần", "Đề xuất", "Mức độ"], rows, size=9.5, sev_col=3, center_cols=(1,))
    else:
        K.para(d, "Không phát hiện văn bản hết hiệu lực trong danh mục theo dõi.", 11)
    K.para(d, "Công cụ này chỉ dò theo danh mục văn bản theo dõi (cập nhật " + res.get("pl_ngay", "") + "). Bắt buộc rà soát toàn bộ văn bản pháp luật, "
           "tiêu chuẩn viện dẫn bằng công cụ TEXO Legal Reviewer trước khi trình ký để bảo đảm dùng phiên bản mới nhất.", 10, b=True, c=K.C["red"])

    K.h1(d, "5. Trình bày, thông tin dự án")
    cl = res["chat_luong"]
    K.data_table(d, [3000, 6026], ["Nội dung", "Kết quả"], [
        ["Quy mô tài liệu", f"{cl['so_tu']:,} từ · {cl['so_tieu_de']} tiêu đề · {cl['so_bang']} bảng · {cl['so_hinh']} hình/sơ đồ".replace(",", ".")],
        ["Tên dự án tìm thấy", "; ".join(cl["ten_du_an"]) or "—"], ["Chủ đầu tư tìm thấy", "; ".join(cl["chu_dau_tu"]) or "—"],
        ["Nghi lẫn tên dự án/CĐT khác", "; ".join(cl["nghi_lan_ten"]) or "Không"],
        ["Chỗ trống chờ điền", (f"{cl['so_cho_trong']} vị trí: " + " | ".join(cl["cho_trong"][:6])) if cl["so_cho_trong"] else "Không"]], size=9.5)
    K.spacer(d, 10)
    nd = nguoi_duyet or ("TRƯỞNG PHÒNG KỸ THUẬT", K.ORG["signer"])
    signers = ([("NGƯỜI KIỂM TRA", nguoi_kiem_tra)] if nguoi_kiem_tra else []) + [(nd[0].upper(), nd[1])]
    K.signature_block(d, content, dt.date.today(), signers, ["Trung tâm lập đề cương", "Lưu P.KT"])
    d.save(out_path)
    return out_path
