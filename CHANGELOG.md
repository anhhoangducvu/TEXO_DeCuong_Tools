# Nhật ký phiên bản – Bộ công cụ Đề cương TVGS

## 1.3.2 – 14/11/2026
- Bìa và tờ lót: dòng địa điểm, tháng lập ghim ở chân trang (khung đoạn neo lề dưới), không còn nằm sát khối chữ ký; skill kiểm tra soi thêm điểm này

## 1.3.1 – 13/11/2026
- Tờ lót phê duyệt: ô "ĐẠI DIỆN TƯ VẤN GIÁM SÁT" rộng hơn để tên Công ty nằm trọn một dòng (không rơi chữ "ĐẦU TƯ"); skill kiểm tra soi thêm khối chữ ký tờ lót

## 1.3.0 – 12/11/2026
- Sửa lỗi chính tả, gõ phím và 15 viện dẫn văn bản hết hiệu lực trong thư viện; thêm bộ quy tắc dùng chung `core/data/sua_loi_noi_dung.json` + `core/sua_loi.py` (app Tạo tự làm sạch thư viện khi nạp; app Kiểm tra soi lỗi chính tả đã biết); bộ kiểm tra nhận cả cách ghi số hiệu lệch chuẩn ("NĐ 136/2020/CP", "40/2013/ QH13"); +12 văn bản hết hiệu lực trong `phap_ly.json`
- Khổ giấy A4 lề trên 20 mm, dưới 20 mm, trái 30 mm, phải 20 mm; độ rộng bảng tính lại theo lề mới; sửa số trang chân trang bị to
- `_build`: dựng lại thư viện tự áp bộ quy tắc sửa lỗi; `dong-bo` chép đè lõi sang skill (không cần quyền xóa)

## 1.2.0 – 23/10/2026
- Đăng nhập gọn (logo, tên app, mật khẩu); thanh bên sau đăng nhập: người ký kiểm + Trợ lý AI tùy chọn (Claude/Gemini/ChatGPT/tương thích OpenAI); AI bổ sung nhận xét chuyên môn vào phiếu và phần trọng tâm giám sát vào đề cương; giảm hiển thị tên người xây dựng

## 1.1.0 – 23/10/2026
- Thêm 8 đề cương mới (TT05, TT06 ×3, TT09 ×2, TT10 ×2) – 16 bộ nguồn; thư viện 60 hạng mục (cọc ép 2026, công tác đất, quan trắc, nhóm trạm XLNT: bể, thử kín, ống, thiết bị, PLC/SCADA, chạy thử, ITP; điểm HP/WP/RP); tách skill texo-lap-decuong; tiêu chí HT06 không lộ đơn vị nội bộ; đề cương phát hành chỉ mang tên Công ty TEXO; danh sách Trung tâm 01–03, 05–12, 18; ghi người xây dựng Hoàng Đức Vũ; nhắc rà soát pháp lý bằng TEXO Legal Reviewer; cơ chế cập nhật cap_nhat.py

## 1.0.0 – 23/10/2026
- Phiên bản đầu: khung 65 tiêu chí, thư viện 50 hạng mục từ 8 bộ đề cương (TT02, TT03, TT08, TT09 ×3, TT12 ×2); app Tạo, app Kiểm tra, skill texo-kiemtra-decuong.
