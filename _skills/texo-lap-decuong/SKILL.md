---
name: texo-lap-decuong
description: Lập đề cương tư vấn giám sát (TVGS) cho dự án mới theo khung chuẩn TEXO – mẫu Cơ bản hoặc Nâng cao phù hợp quy mô công trình, tự chọn hạng mục giám sát chi tiết (nền móng, kết cấu, hoàn thiện, MEP, hạ tầng, trạm xử lý nước thải, chuyên đề), căn cứ pháp lý 2026 – xuất Word mang tên Công ty TEXO, có bìa, tờ lót phê duyệt, mục lục.
---

# TEXO – Lập đề cương Tư vấn giám sát

Xưng "em", gọi "anh Vũ". Skill dùng chung lõi (`scripts/core`) với app Tạo đề cương, app Kiểm tra đề cương và skill `texo-kiemtra-decuong`; bản gốc lõi ở `D:\Ktra HS\De cuong\TEXO_DeCuong_Tools\core`.

## Quy tắc bắt buộc
1. **Đề cương là tài liệu phát hành cho Chủ đầu tư → chỉ mang tên Công ty Cổ phần TEXO Tư vấn và Đầu tư.** Không đưa tên Trung tâm, VPĐT, Phòng Kỹ thuật, ghi chú nội bộ vào bìa, header, footer, thân bài. Trung tâm lập (01, 02, 03, 05–12, 18 – không có Trung tâm 04) chỉ ghi ở tên file lưu nội bộ hoặc nhật ký.
2. **Pháp lý mới nhất:** khi giao đề cương, luôn nhắc anh/đoàn rà soát toàn bộ văn bản pháp luật, tiêu chuẩn viện dẫn bằng công cụ **TEXO Legal Reviewer** trước khi trình ký.
3. Đề cương lập xong phải tự kiểm bằng `texo-kiemtra-decuong` (script tự chạy): ≥ 95 điểm, 0 văn bản hết hiệu lực, không lộ tên đơn vị nội bộ.

## Quy trình
1. **Thu thập thông tin** (hỏi gộp, tối đa 2 câu nếu thiếu): tên dự án, công trình, gói thầu, địa điểm, CĐT, hợp đồng TVGS, thời gian; loại công trình, cấp, số tầng nổi/hầm, tổng diện tích sàn, chiều cao, giải pháp móng – kết cấu; có nội thất bàn giao, thang máy, TBA, XLNT, hạ tầng ngoài nhà không; CĐT có yêu cầu cao không. Lấy từ hợp đồng/HSMT/phiếu VPĐT nếu anh gửi kèm.
2. **Điền** `scripts/thong_tin_mau.json` (chép thành `tt.json`). Để trống `hang_muc`, `nhan_su`, `mau` để công cụ gợi ý theo quy mô.
3. **Chạy:**
   ```bash
   cd <skill>/scripts
   python3 tao_de_cuong.py tt.json De_cuong_TVGS_<ten>.docx [--mau "Cơ bản|Nâng cao"]
   ```
   Script in lý do chọn mẫu, số hạng mục và kết quả tự kiểm.
4. **Đọc lại** quy mô, nhân sự đoàn, hạng mục; render (`soffice --headless --convert-to pdf`) xem bìa, tờ lót, mục lục, vài trang bảng. Thiếu hạng mục đặc thù thì bổ sung vào `hang_muc` rồi chạy lại.
5. **Giao:** file Word + 1–2 câu: mẫu, số hạng mục, điểm tự kiểm, nhắc rà soát pháp lý bằng TEXO Legal Reviewer và rà thông số kỹ thuật theo HSTK của dự án.

## Mẫu và gợi ý theo quy mô
- **Cơ bản:** đủ toàn bộ tiêu chí bắt buộc – bìa, tờ lót phê duyệt, mục lục, thông tin – quy mô – phạm vi, cơ sở pháp lý 2026, vai trò các bên, giám sát chất lượng (khởi công → nghiệm thu theo NĐ 207/2026 → hồ sơ hoàn thành), khối lượng, tiến độ, ATLĐ–VSMT–PCCC, báo cáo – họp, tổ chức đoàn, phân cấp ký, đề cương chi tiết theo công tác, biểu mẫu.
- **Nâng cao** (cấp I trở lên, có hầm, ≥ 9 tầng, ≥ 20.000 m² sàn, hoặc CĐT yêu cầu): thêm mục tiêu đề cương, các bên tham gia, dữ liệu đầu vào, ITP, quy trình nghiệm thu tiêu biểu, NCR, thay đổi thiết kế – RFI, thời hạn xác nhận khối lượng, cảnh báo sớm tiến độ, quản lý rủi ro an toàn, đình chỉ khẩn cấp, thời hạn xử lý hồ sơ, điều động – đào tạo nhân sự, ma trận trách nhiệm, kế hoạch an toàn, phiếu kiểm tra chi tiết, điểm kiểm soát HP/WP/RP.
- Loại công trình: dân dụng cao tầng; thấp tầng – công cộng; công nghiệp; hạ tầng kỹ thuật; **trạm xử lý nước thải – hạ tầng môi trường** (bể công nghệ, thử kín bể, đường ống công nghệ, thiết bị, PLC/SCADA, chạy thử – vận hành thử, ITP); gói chuyên đề cọc, khoan khảo sát, trắc đạc – quan trắc.

## Cập nhật
Khi anh nhờ cập nhật pháp lý, tiêu chuẩn, thêm đề cương mẫu: làm theo `references/CAP_NHAT.md` (lệnh `python _build/cap_nhat.py quet | dung-lai | dong-bo`), sau đó gửi lại hai file .skill mới.

## Lưu ý
- Không ghi nhãn phương pháp tư duy, cách trình bày vào đề cương.
- Đóng gói skill: luôn xuất `.skill`.

_Người xây dựng: Hoàng Đức Vũ – Phòng Kỹ thuật._
