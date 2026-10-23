# -*- coding: utf-8 -*-
"""App 1 – TẠO ĐỀ CƯƠNG TVGS theo khung chuẩn TEXO, phù hợp quy mô công trình.
Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật, Công ty CP TEXO Tư vấn và Đầu tư.
Chạy: streamlit run app_tao_de_cuong.py
"""
import datetime as dt
import io
import json
import os
import tempfile

import pandas as pd
import streamlit as st

from core import ai as AI, checker, generator as G, ui

TITLE = "Tạo đề cương Tư vấn giám sát"
ui.setup(TITLE, "📝")
ui.gate(TITLE)
ui.header(TITLE, "Phòng Kỹ thuật · Khung chuẩn từ đề cương các Trung tâm · Căn cứ pháp lý 2026")
CFG = ui.sidebar(kiem_tra=False)

LIB = G.load("thu_vien_hang_muc.json")["hang_muc"]
LIBD = {m["id"]: m for m in LIB}
NHOM = ["Chung", "Nền móng", "Kết cấu", "Hoàn thiện", "Cơ điện (MEP)", "Hạ tầng", "Công trình xử lý nước thải", "Chuyên đề"]
# Danh sách Trung tâm (không có Trung tâm 04, có Trung tâm 18) – chỉ dùng nội bộ, KHÔNG in ra đề cương
TRUNG_TAM = [f"Trung tâm Tư vấn {i:02d}" for i in (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 18)] + ["Phòng/đơn vị khác"]

st.markdown("**Bước 1 – Thông tin dự án, gói thầu**")
c1, c2 = st.columns(2)
du_an = c1.text_input("Tên dự án *")
cong_trinh = c2.text_input("Công trình")
goi_thau = c1.text_input("Gói thầu", "Tư vấn giám sát thi công xây dựng và lắp đặt thiết bị")
dia_diem = c2.text_input("Địa điểm xây dựng")
cdt = c1.text_input("Chủ đầu tư *")
dd_cdt = c2.text_input("Đại diện Chủ đầu tư / BQLDA (nếu có)")
hop_dong = c1.text_input("Hợp đồng TVGS (số, ngày)", placeholder="Số …/2026/HĐTV ngày …")
nguon_von = c2.text_input("Nguồn vốn")
c3, c4, c5, c6 = st.columns(4)
tt = c3.selectbox("Đơn vị lập (nội bộ, không in ra)", TRUNG_TAM, index=8,
                  help="Chỉ để quản lý nội bộ. Đề cương phát hành cho Chủ đầu tư chỉ mang tên Công ty Cổ phần TEXO Tư vấn và Đầu tư.")
tvgs_truong = c4.text_input("TVGS trưởng")
thoi_gian = c5.number_input("Thời gian thực hiện (tháng)", 0, 120, 12)
ngay = c6.date_input("Tháng lập đề cương", dt.date.today())

st.markdown("**Bước 2 – Quy mô công trình**")
c1, c2, c3, c4, c5 = st.columns([2.2, 1, 1, 1, 1])
loai = c1.selectbox("Loại công trình / gói thầu", G.LOAI_CT)
cap = c2.selectbox("Cấp công trình", G.CAP_CT, index=2)
so_tang = c3.number_input("Số tầng nổi", 0, 120, 9)
so_ham = c4.number_input("Số tầng hầm", 0, 10, 0)
dt_san = c5.number_input("Tổng DT sàn (m²)", 0.0, 2_000_000.0, 10000.0, step=500.0)
c1, c2, c3 = st.columns([1.3, 1.3, 1])
mong = c1.multiselect("Giải pháp nền móng", G.MONG, default=["Cọc ép / cọc đóng BTCT"])
ket_cau = c2.multiselect("Giải pháp kết cấu", G.KET_CAU, default=["BTCT toàn khối"])
chieu_cao = c3.number_input("Chiều cao công trình (m)", 0.0, 700.0, 0.0)
c1, c2, c3, c4, c5, c6 = st.columns(6)
noi_that = c1.checkbox("Bàn giao nội thất")
thang_may = c2.checkbox("Có thang máy", value=so_tang >= 6)
tba = c3.checkbox("Trạm biến áp, máy phát")
xlnt = c4.checkbox("Xử lý nước thải")
htnn = c5.checkbox("Hạ tầng ngoài nhà", value=True)
cdt_cao = c6.checkbox("CĐT yêu cầu cao")
mo_ta = st.text_area("Mô tả quy mô, công năng (mỗi dòng một ý – đưa nguyên vào mục Quy mô)", height=80)
cac_ben_txt = st.text_area("Các bên tham gia khác (mỗi dòng: Vai trò | Tên đơn vị) – dùng cho mẫu Nâng cao", height=70,
                           placeholder="Tư vấn thiết kế | Công ty …\nTư vấn thẩm tra | Công ty …")

info = dict(du_an=du_an, cong_trinh=cong_trinh, goi_thau=goi_thau, dia_diem=dia_diem, chu_dau_tu=cdt, dai_dien_cdt=dd_cdt,
            hop_dong=hop_dong, nguon_von=nguon_von, trung_tam=tt if tt != "Khác" else "", tvgs_truong=tvgs_truong,
            thoi_gian=thoi_gian or "", ngay=ngay, loai_ct=loai, cap_ct=cap, so_tang=so_tang, so_ham=so_ham, dt_san=dt_san,
            chieu_cao=chieu_cao or "", mong=mong, ket_cau=ket_cau, noi_that=noi_that, thang_may=thang_may, tba=tba, xlnt=xlnt,
            ha_tang_ngoai_nha=htnn, cdt_yeu_cau_cao=cdt_cao, mo_ta_quy_mo=mo_ta,
            cac_ben=[tuple(x.split("|", 1)) for x in cac_ben_txt.splitlines() if "|" in x])
info["cac_ben"] = [(a.strip(), b.strip()) for a, b in info["cac_ben"]]
info["nguoi_ky_tvgs"] = CFG.get("nguoi_ky_tvgs", "")

st.markdown("**Bước 3 – Mẫu đề cương**")
de_xuat, ly_do = G.de_xuat_muc_mau(info)
st.info(ly_do)
level = st.radio("Mẫu", ["Cơ bản", "Nâng cao"], index=0 if de_xuat == "Cơ bản" else 1, horizontal=True,
                 help="Cơ bản: đủ thành phần bắt buộc theo khung chuẩn. Nâng cao: thêm hệ thống quản lý chất lượng công tác giám sát "
                      "(ma trận trách nhiệm, ITP, NCR, RFI, thời hạn xử lý hồ sơ, cảnh báo sớm tiến độ, kế hoạch an toàn, phiếu kiểm tra chi tiết).")

st.markdown("**Bước 4 – Hạng mục giám sát chi tiết** (đã gợi ý theo quy mô – anh/chị chỉnh thêm, bớt)")
goi_y = G.de_xuat_hang_muc(info)
key = "hm_" + str(abs(hash(json.dumps([loai, cap, so_tang, so_ham, mong, ket_cau, noi_that, thang_may, tba, xlnt, htnn]))))
chon = []
cols = st.columns(2)
for k, nh in enumerate(NHOM):
    ms = [m for m in LIB if m["nhom"] == nh]
    with cols[k % 2].expander(f"{nh} ({sum(1 for m in ms if m['id'] in goi_y)}/{len(ms)} gợi ý)", expanded=False):
        sel = st.multiselect(nh, [m["id"] for m in ms], default=[m["id"] for m in ms if m["id"] in goi_y],
                             format_func=lambda i: LIBD[i]["ten"], key=key + nh, label_visibility="collapsed")
        chon += sel
modules = [m for m in [x["id"] for x in LIB] if m in chon]
st.caption(f"Đã chọn {len(modules)} hạng mục.")

st.markdown("**Bước 5 – Nhân sự đoàn TVGS** (gợi ý theo cấp công trình – sửa trực tiếp trong bảng)")
staff_df = pd.DataFrame(G.de_xuat_nhan_su(info, modules, level))
staff_df = staff_df.rename(columns={"chuc_danh": "Chức danh", "ho_ten": "Họ và tên", "chuyen_mon": "Chuyên môn, chứng chỉ", "nhiem_vu": "Nhiệm vụ chính"})
staff_ed = st.data_editor(staff_df, num_rows="dynamic", width="stretch", key="staff_" + level + key)

st.divider()
if st.button("📄 Tạo đề cương", type="primary", disabled=not (du_an and cdt)):
    staff = [dict(chuc_danh=r["Chức danh"], ho_ten=r.get("Họ và tên") or "", chuyen_mon=r.get("Chuyên môn, chứng chỉ") or "",
                  nhiem_vu=r.get("Nhiệm vụ chính") or "") for _, r in staff_ed.iterrows() if r.get("Chức danh")]
    if CFG.get("ai"):
        with st.spinner("AI đang soạn phần đặc điểm công trình và trọng tâm giám sát…"):
            r = AI.lap(info, modules, LIB, CFG["ai"])
        if r.get("ok"):
            info["_ai"] = r["data"]
            them = [m for m in (r["data"].get("hang_muc_bo_sung") or []) if m in LIBD and m not in modules]
            if them:
                st.info("AI gợi ý cân nhắc bổ sung: " + "; ".join(LIBD[m]["ten"] for m in them) + " (chọn thêm ở Bước 4 nếu phù hợp).")
        else:
            st.error("AI lỗi – đề cương vẫn tạo theo bộ quy tắc. " + r.get("error", ""))
    with st.spinner("Đang dựng đề cương…"):
        tmp = tempfile.mkdtemp()
        safe = "".join(ch for ch in (cong_trinh or du_an)[:40] if ch.isalnum() or ch in " -_").strip().replace(" ", "_")
        fn = f"De_cuong_TVGS_{safe}_{'CoBan' if level == 'Cơ bản' else 'NangCao'}_{dt.date.today():%y%m%d}.docx"
        out = os.path.join(tmp, fn)
        G.generate(info, level, modules, staff, out)
        res = checker.check_files([(fn, out)], {"muc_mau": level, "ten_du_an": du_an, "chu_dau_tu": cdt,
                                                "hang_muc": modules, "ngay": dt.date(ngay.year, ngay.month, 1)})
        st.session_state["out"] = (fn, open(out, "rb").read(), res)

if "out" in st.session_state:
    fn, data, res = st.session_state["out"]
    st.success(f"Đã tạo {fn}")
    c1, c2, c3 = st.columns(3)
    ui.kpi(c1, res["diem"], "Tự kiểm theo khung", res["muc_mau"], res["mau"])
    ui.kpi(c2, sum(1 for h in res["hang_muc"] if h["trang_thai"].startswith("Có mục")), "Hạng mục chi tiết", "có mục giám sát riêng")
    ui.kpi(c3, len(res["phap_ly"]["het"]), "Căn cứ hết hiệu lực", "phải bằng 0", "green" if not res["phap_ly"]["het"] else "red")
    st.download_button("⬇️ Tải đề cương (.docx)", data, file_name=fn, type="primary",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    ui.callout("⚖️ Trước khi trình ký: rà soát văn bản pháp luật, tiêu chuẩn bằng TEXO Legal Reviewer. "
               "Đề cương chỉ mang tên Công ty TEXO – không thêm tên Trung tâm.", "orange")
    st.caption("Mở bằng Word → chọn **Yes** khi Word hỏi cập nhật trường để mục lục có số trang. "
               "Đoàn TVGS rà lại thông số kỹ thuật theo hồ sơ thiết kế, chỉ dẫn kỹ thuật của dự án trước khi trình ký.")
