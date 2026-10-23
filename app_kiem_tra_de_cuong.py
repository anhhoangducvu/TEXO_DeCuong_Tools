# -*- coding: utf-8 -*-
"""App 2 – KIỂM TRA ĐỀ CƯƠNG TVGS của các đoàn theo khung chuẩn TEXO.
Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật, Công ty CP TEXO Tư vấn và Đầu tư.
Chạy: streamlit run app_kiem_tra_de_cuong.py
"""
import datetime as dt
import io
import os
import tempfile

import pandas as pd
import streamlit as st

from core import ai as AI, checker, extract as ex, report, ui

TITLE = "Kiểm tra đề cương Tư vấn giám sát"
ui.setup(TITLE, "🔎")
ui.gate(TITLE)
ui.header(TITLE, "Phòng Kỹ thuật · Đối chiếu khung chuẩn, hạng mục, căn cứ pháp lý 2026")
CFG = ui.sidebar(kiem_tra=True)

LIB = checker.load("thu_vien_hang_muc.json")["hang_muc"]
LIBD = {m["id"]: m for m in LIB}
MD = {"high": "🔴 Phải xử lý", "mid": "🟠 Nên xử lý", "ok": "🟢 Đạt", "info": "🔵 Lưu ý"}

tab_ck, tab_khung = st.tabs(["Kiểm tra đề cương", "Khung chuẩn tham chiếu"])

with tab_ck:
    files = st.file_uploader("Tải đề cương (.docx hoặc .pdf). Đề cương chia nhiều file thì chọn tất cả – công cụ ghép theo thứ tự tên file.",
                             type=["docx", "pdf"], accept_multiple_files=True)
    c1, c2, c3, c4 = st.columns([1, 1.6, 1.6, 1])
    mau = c1.selectbox("Mẫu đăng ký", ["Tự nhận", "Cơ bản", "Nâng cao"])
    ten = c2.text_input("Tên dự án (để soát lẫn tên)", "")
    cdt = c3.text_input("Chủ đầu tư (để soát lẫn tên)", "")
    don_vi = c4.selectbox("Đơn vị lập (nội bộ)", [""] + [f"Trung tâm Tư vấn {i:02d}" for i in (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 18)] + ["Phòng/đơn vị khác"])
    hm = st.multiselect("Hạng mục công trình bắt buộc phải có đề cương chi tiết (để trống: công cụ tự suy từ phần quy mô)",
                        [m["id"] for m in LIB], format_func=lambda i: f"{LIBD[i]['nhom']} · {LIBD[i]['ten']}")
    if st.button("🔎 Kiểm tra", type="primary", disabled=not files):
        with st.spinner("Đang đọc và đối chiếu…"):
            opts = {"ten_du_an": ten, "chu_dau_tu": cdt, "hang_muc": hm}
            if mau != "Tự nhận":
                opts["muc_mau"] = mau
            blocks, meta = ex.read_any([(f.name, f.getvalue()) for f in files])
            res = checker.check(blocks, meta, opts)
            res["files"] = meta.get("files", [])
            ai_data = None
            if CFG.get("ai"):
                with st.spinner("AI đang đọc thẩm định nội dung (20–90 giây)…"):
                    r = AI.kiem_tra(blocks, res, CFG["ai"])
                if r.get("ok"):
                    ai_data = r["data"]
                    if r.get("truncated"):
                        st.warning("Phản hồi AI có thể bị cắt phần cuối.")
                else:
                    st.error("AI lỗi – phiếu vẫn xuất theo bộ quy tắc. " + r.get("error", ""))
            tmp = tempfile.mkdtemp()
            base = os.path.splitext(files[0].name)[0][:50]
            out = os.path.join(tmp, f"Phieu_kiem_tra_de_cuong_{base}.docx")
            report.make_report(res, {"ten": ten or base, "don_vi": don_vi}, out, CFG.get("nguoi_kiem_tra", ""),
                               (CFG.get("chuc_danh_duyet") or "Trưởng phòng Kỹ thuật", CFG.get("nguoi_duyet", "")), ai_data)
            st.session_state["res"] = (res, open(out, "rb").read(), os.path.basename(out), ai_data)

    if "res" in st.session_state:
        res, data, fn, ai_data = st.session_state["res"]
        todo = report.viec_phai_lam(res)
        n_high = sum(1 for x in todo if x[0] == "high")
        c1, c2, c3, c4 = st.columns(4)
        ui.kpi(c1, res["diem"], "Điểm khung", f"/100 · mẫu {res['muc_mau']}", res["mau"])
        ui.kpi(c2, n_high, "Phải xử lý", "trước khi trình ký", "red" if n_high else "green")
        ui.kpi(c3, sum(1 for h in res["hang_muc"] if h["trang_thai"].startswith("Có mục")), "Hạng mục chi tiết", "có mục riêng")
        ui.kpi(c4, len(res["phap_ly"]["het"]), "Căn cứ hết hiệu lực", "loại văn bản", "red" if res["phap_ly"]["het"] else "green")
        ui.callout(f"<b>Kết luận: {res['ket_luan']}.</b> Mẫu tự nhận: {res['muc_mau_tu_nhan']} · "
                   f"thời điểm lập: {res.get('ngay') or 'không xác định'}", res["mau"])
        st.download_button("⬇️ Tải phiếu kiểm tra (.docx)", data, file_name=fn, type="primary",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        if ai_data:
            with st.expander("🤖 Nhận xét chuyên môn (AI hỗ trợ)", expanded=True):
                if ai_data.get("nhan_xet_chung"):
                    st.write(ai_data["nhan_xet_chung"])
                st.dataframe(pd.DataFrame([{"Mức độ": MD.get(x.get("muc_do"), MD["info"]), "Phát hiện": x.get("noi_dung", ""),
                                            "Vị trí": x.get("vi_tri", ""), "Đề xuất": x.get("de_xuat", "")}
                                           for x in ai_data.get("phat_hien", []) if isinstance(x, dict)]), width="stretch", hide_index=True)
        t1, t2, t3, t4, t5 = st.tabs(["Việc cần xử lý", "Khung chuẩn", "Hạng mục", "Pháp lý", "Trình bày"])
        with t1:
            st.dataframe(pd.DataFrame([{"Mức độ": MD[x[0]], "Nội dung": x[1], "Hiện trạng": x[2], "Yêu cầu sửa": x[3]} for x in todo]),
                         width="stretch", hide_index=True)
        with t2:
            nh = {n["id"]: n["ten"] for n in res["nhom"]}
            df = pd.DataFrame([{"Nhóm": nh[r["nhom"]], "Mã": r["id"], "Tiêu chí": r["ten"], "Cấp": "Bắt buộc" if r["cap"] == "B" else "Nâng cao",
                                "Kết quả": r["trang_thai"], "Bằng chứng": r["bang_chung"], "Mức độ": MD[r["muc_do"]]} for r in res["tieu_chi"]])
            loc = st.radio("Lọc", ["Tất cả", "Chưa đạt"], horizontal=True)
            if loc == "Chưa đạt":
                df = df[df["Kết quả"] != "Đạt"]
            st.dataframe(df, width="stretch", hide_index=True, height=520)
        with t3:
            st.dataframe(pd.DataFrame([{"Nhóm": h["nhom"], "Hạng mục": h["ten"], "Hiện trạng": h["trang_thai"], "Mục tìm thấy": h["bang_chung"],
                                        "Cần có": "Có" if h["can_co"] else "", "Mức độ": MD[h["muc_do"]]} for h in res["hang_muc"]]),
                         width="stretch", hide_index=True)
        with t4:
            pl = res["phap_ly"]
            st.write("Văn bản mới đã viện dẫn: " + " · ".join(f"{k} {'✅' if v else '❌'}" for k, v in pl["co_moi"].items()))
            rows = [{"Văn bản": x["ten"], "Số lần": x["so_lan"], "Đề xuất": "Thay bằng " + x["thay_the"], "Mức độ": MD[x["muc_do"]]} for x in pl["het"]] + \
                   [{"Văn bản": x["ten"], "Số lần": x["so_lan"], "Đề xuất": x["ly_do"], "Mức độ": MD["info"]} for x in pl["ra_soat"]]
            st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        with t5:
            cl = res["chat_luong"]
            st.write(f"{cl['so_tu']:,} từ · {cl['so_tieu_de']} tiêu đề · {cl['so_bang']} bảng · {cl['so_hinh']} hình".replace(",", "."))
            st.write("**Tên dự án tìm thấy:** " + ("; ".join(cl["ten_du_an"]) or "—"))
            st.write("**Chủ đầu tư tìm thấy:** " + ("; ".join(cl["chu_dau_tu"]) or "—"))
            if cl["nghi_lan_ten"]:
                st.error("Nghi lẫn tên dự án/CĐT khác: " + "; ".join(cl["nghi_lan_ten"]))
            if cl["cho_trong"]:
                st.warning(f"{cl['so_cho_trong']} chỗ trống chờ điền")
                for x in cl["cho_trong"][:15]:
                    st.code(x)

with tab_khung:
    K = checker.load("khung_tieuchi.json")
    nh = {n["id"]: n["ten"] for n in K["nhom"]}
    st.markdown("Khung chuẩn rút từ 16 bộ đề cương của các Trung tâm (TT02, 03, 05, 06, 08, 09, 10, 12). **Bắt buộc** áp dụng mọi đề cương; "
                "**Nâng cao** áp dụng cho công trình cấp I trở lên, có tầng hầm, cao tầng hoặc theo yêu cầu Chủ đầu tư.")
    st.dataframe(pd.DataFrame([{"Nhóm": nh[c["nhom"]], "Mã": c["id"], "Tiêu chí": c["ten"], "Cấp": "Bắt buộc" if c["cap"] == "B" else "Nâng cao"}
                               for c in K["tieu_chi"]]), width="stretch", hide_index=True, height=600)
    st.markdown("**Thư viện hạng mục giám sát chi tiết**")
    st.dataframe(pd.DataFrame([{"Nhóm": m["nhom"], "Hạng mục": m["ten"], "Nguồn": ", ".join(m["nguon"]), "Số dòng nội dung": len(m["hang"]),
                                "Phiếu kiểm tra": len(m["checklist"])} for m in LIB]), width="stretch", hide_index=True)
