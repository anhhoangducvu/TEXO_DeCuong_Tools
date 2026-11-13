# Nhật ký – Bộ công cụ Đề cương TVGS

## 14/11/2026 – v1.3.2
**Anh Vũ yêu cầu:** dòng "HÀ NỘI, THÁNG …" trên bìa và tờ lót phải nằm dưới cùng, không sát chỗ ký (lỗi ở cả skill và app).
**Đã làm:** `core/generator.py` thêm `_ghim_cuoi_trang()` – đoạn địa điểm, tháng lập đặt trong khung đoạn neo lề dưới, căn giữa; skill kiểm tra soi thêm điểm này; `dong-bo` lên 1.3.2, đóng gói lại 2 file .skill.
**Kiểm thử:** in thử bìa + tờ lót (dự án ngắn, ít dòng thông tin) – dòng tháng nằm ở chân trang, khối ký có khoảng trống rộng.

## 14/11/2026 – v1.3.1 (cập nhật app theo skill)
**Anh Vũ yêu cầu:** đưa vào app các thay đổi gần đây của skill (sửa lỗi chính tả, văn bản cũ, khổ giấy, khối chữ ký). Bộ công cụ đã chuyển sang `D:\My Agents\TEXO_De cuong\TEXO_DeCuong_Tools`.
**Đã làm:** chép lõi 1.3.1 vào `core/` (giữ `ui.py`, logo của app); `_build/build_library.py`, `build_snippets.py` áp bộ quy tắc sửa lỗi khi dựng lại thư viện; `cap_nhat.py dong-bo` chép đè lõi (không xóa); đồng bộ lõi sang `_skills/` và đóng gói lại 2 file .skill 1.3.1; cập nhật `CAP_NHAT.md` (mục e – báo lỗi chính tả), `CHANGELOG.md`, `README.md`, đường dẫn mới trong SKILL.md.
**Kiểm thử:** chạy thử 2 app (đăng nhập texo2026, tạo đề cương Nâng cao, mở trang kiểm tra) – không lỗi; đề cương ra A4 lề 20/20/30/20 mm, tên Công ty ở khối ký nằm một dòng; tự kiểm 100/100, 0 lỗi chính tả, 0 văn bản hết hiệu lực.
**Lưu bản cũ:** `_luu_tru/261114 ban cu v1.2.0/` (lõi, _build, _skills, tài liệu, 2 file .skill cũ); gói cập nhật `_luu_tru/261114 goi cap nhat de cuong v1.3.1.zip`.
**Có thể xóa khi anh thấy ổn:** gói zip trong `_luu_tru/`; 6 file trong `De_cuong_mau_vi_du/` và 16 phiếu trong `Ket_qua_kiem_tra/` là bản sinh từ v1.1–1.2 (còn lỗi chính tả, lề cũ) – nên tạo/kiểm lại bằng app mới rồi thay.
**Đề cương nguồn:** `dung-lai` mặc định đọc thư mục cha `D:\My Agents\TEXO_De cuong` (16 bộ đề cương nguồn cần nằm ở đó, hoặc đặt biến `DC_SRC`).

## 23/10/2026 (tối) – v1.2.0
**Anh Vũ yêu cầu:** màn hình đăng nhập gọn như app khối lượng; vào trong mới có thanh bên người ký kiểm; cho chọn AI; tên người xây dựng xuất hiện quá nhiều – giảm cho tinh tế.
**Đã làm:** đăng nhập chỉ còn logo, tên app, ô mật khẩu (không thanh bên); thanh bên sau đăng nhập: người kiểm tra, người duyệt (in vào phiếu) / đại diện TVGS ký tờ lót, người lập (app Tạo); Trợ lý AI tùy chọn (Claude, Gemini, ChatGPT, tương thích OpenAI – lấy danh sách model, kiểm tra kết nối, lưu key tại máy). AI chạy trên nền kết quả bộ quy tắc: app Kiểm tra thêm mục "Nhận xét chuyên môn (AI hỗ trợ)" vào phiếu; app Tạo thêm mục "Đặc điểm công trình và trọng tâm giám sát" và gợi ý hạng mục bổ sung. Tên người xây dựng chỉ còn một dòng nhỏ cuối thanh bên, cuối README và cuối SKILL.md; bỏ khỏi đầu trang app, footer app, footer và cuối phiếu (phiếu giữ khối ký người duyệt). Phiếu 16 bộ đã xuất lại.
**Lưu ý:** phần gọi AI đã thử bằng phản hồi giả lập; lần đầu dùng key thật bấm "Lấy danh sách model" và "Kiểm tra kết nối".

## 23/10/2026 (chiều) – v1.1.0
**Anh Vũ yêu cầu:** đọc thêm đề cương mới; tách skill lập đề cương; Công ty không có Trung tâm 04, có Trung tâm 18; mọi nội dung ghi người xây dựng Hoàng Đức Vũ; nhắc kiểm tra pháp luật mới nhất bằng công cụ đã xây dựng (TEXO Legal Reviewer); có cơ chế cập nhật; tài liệu phát hành ra ngoài chỉ mang tên Công ty TEXO.

**8 đề cương mới đã đọc:** TT5 Taseco Thủy Nguyên · TT6 cọc ép (2026) · TT6 hạ tầng · TT6 trạm XLNT 19.000 m³/ngđ (2026) · TT9 khảo sát Thái Nguyên (PDF, file không có đuôi) · TT9 NOXH Ao Trũng cọc thử (PDF, 2026) · TT10 HI-P Bắc Ninh (song ngữ Việt – Trung, 2026) · TT10 Nhôm Ngọc Diệp.

**Đưa vào thư viện:** cọc ép (thay bằng bản TT6 2026); công tác đất – hố đào – hạ nước ngầm – san nền; nhóm trạm XLNT (bể BTCT công nghệ, chống thấm – thử kín bể, đường ống công nghệ – thử áp – súc rửa, thiết bị cơ khí – công nghệ, điện động lực – PLC/SCADA – loop test, an toàn hóa chất, chạy thử – vận hành thử, ITP tóm tắt); bổ sung hạ tầng, cây xanh (TT6); quan trắc lún – nghiêng – chuyển vị (soạn từ TT02). Điểm kiểm soát HP/WP/RP hiển thị trong bảng giám sát chi tiết. Thêm loại công trình "Công trình xử lý nước thải, hạ tầng môi trường" vào app Tạo.

**Chưa đưa vào (ghi để làm tiếp):** TT9 cọc thử, TT9 khảo sát (PDF, bảng bóc không sạch – đã có mục tương đương từ Harmonia, TT08); TT10 HI-P song ngữ (gợi ý phương án mẫu song ngữ cho dự án FDI); TT02 phòng ngừa sai sót chi tiết theo công tác.

**Phát hiện khi kiểm 16 bộ** (phiếu ở `Ket_qua_kiem_tra/`): 11/16 bộ còn viện dẫn văn bản hết hiệu lực; cả 3 bộ đã dùng văn bản 2026 nhưng vẫn sót Luật 50/2014 hoặc NĐ 175/2024 (TT02 VNM, TT6 XLNT); TT03 tên CĐT không thống nhất; TT10 Ngọc Diệp lẫn tên giai đoạn; TT12 Taseco và TT10 HI-P còn nhiều chỗ trống chờ điền; không bộ nào in tên Trung tâm ra ngoài.

**Thay đổi công cụ:** tiêu chí HT06 (không lộ đơn vị nội bộ); bỏ qua ô trống trong biểu mẫu biên bản khi đếm chỗ trống; đọc được file không có đuôi; tên người xây dựng trên app, phiếu, skill, script; nhắc TEXO Legal Reviewer trên app, phiếu, skill, script; cơ chế cập nhật `_build/cap_nhat.py` + `CAP_NHAT.md` + `CHANGELOG.md` + sổ đề cương nguồn.

**Thư mục cũ có thể xóa:** `Ket_qua_kiem_tra_8_bo/`, `De_cuong_mau_vi_du/MAU_De_cuong_TVGS_*_(vi du CT1 25 tang).docx` (đã thay bằng bản mới).

## 23/10/2026 (sáng) – v1.0.0
Đọc 8 bộ đề cương (TT02, TT03, TT08, TT09 ×3, TT12 ×2); lập khung chuẩn 65 tiêu chí, thư viện 50 hạng mục; app Tạo, app Kiểm tra, skill texo-kiemtra-decuong.
