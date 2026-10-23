---
name: texo-kiemtra-decuong
description: Kiểm tra đề cương tư vấn giám sát (TVGS) do các Trung tâm/đoàn TEXO lập theo khung chuẩn rút từ đề cương các Trung tâm – đủ phần, đủ hạng mục giám sát chi tiết, căn cứ pháp lý 2026, lẫn tên dự án, lộ tên đơn vị nội bộ – và xuất phiếu kiểm tra Word P.KT. Cũng dùng khi anh Vũ muốn cập nhật khung chuẩn, danh mục pháp lý hoặc thêm đề cương mẫu mới vào bộ công cụ.
---

# TEXO – Kiểm tra đề cương Tư vấn giám sát

Xưng "em", gọi "anh Vũ", giọng tích cực, ngắn gọn. Skill này dùng chung lõi (`scripts/core`) với app Kiểm tra đề cương, app Tạo đề cương và skill `texo-lap-decuong` (lập đề cương). Bản gốc của lõi nằm trong bộ công cụ `D:\Ktra HS\De cuong\TEXO_DeCuong_Tools\core`; skill chỉ giữ bản sao do lệnh đồng bộ chép sang.

## Quy tắc chung
1. **Pháp lý mới nhất:** công cụ chỉ dò theo danh mục văn bản đang theo dõi (`core/data/phap_ly.json`). Mọi phiếu, câu trả lời đều nhắc: *bắt buộc rà soát văn bản pháp luật, tiêu chuẩn viện dẫn bằng công cụ TEXO Legal Reviewer trước khi trình ký*.
2. **Nội bộ – đối ngoại:** đề cương gửi Chủ đầu tư chỉ mang tên Công ty Cổ phần TEXO Tư vấn và Đầu tư. Tên Trung tâm, VPĐT, Phòng Kỹ thuật là thông tin nội bộ – thấy trong đề cương thì ghi vào việc cần xử lý (tiêu chí HT06). Phiếu kiểm tra là tài liệu nội bộ nên được ghi đơn vị lập.
3. **Danh sách đơn vị lập:** Trung tâm 01, 02, 03, 05, 06, 07, 08, 09, 10, 11, 12, 18 (Công ty không có Trung tâm 04).

## 1. Kiểm tra đề cương
**Bước 1 – Chạy công cụ:**
```bash
cd <skill>/scripts
python3 kiem_tra.py <file1> [file2 …] --ten "<tên dự án>" --cdt "<chủ đầu tư>" \
   [--mau "Cơ bản|Nâng cao"] [--hang-muc EPCOC,BTCT,…] --json kq.json --out Phieu_kiem_tra_de_cuong_<ten>.docx --don-vi "Trung tâm …"
```
- Tên dự án, CĐT lấy từ phiếu VPĐT/hợp đồng (không lấy từ chính đề cương) để bắt lỗi chép từ đề cương dự án khác.
- `--hang-muc`: mã hạng mục công trình thực tế (`references/khung_chuan.md`); bỏ trống thì công cụ tự suy từ phần quy mô.
- File không có đuôi vẫn đọc được (tự nhận PDF/Word theo nội dung).

Kết quả: điểm khung /100, kết luận, việc phải xử lý, 66 tiêu chí, bảng hạng mục, văn bản hết hiệu lực, chỗ trống chờ điền (bỏ qua ô trống trong biểu mẫu biên bản), nghi lẫn tên dự án/CĐT, tên đơn vị nội bộ.

**Bước 2 – Em đọc thẩm định những điểm công cụ không chấm được:**
1. Quy mô, cấp công trình, giải pháp móng – kết cấu có khớp hợp đồng/HSTK; mẫu Cơ bản có tương xứng quy mô (cấp I trở lên, có hầm, ≥ 9 tầng, ≥ 20.000 m² sàn → nên Nâng cao).
2. Hạng mục giám sát chi tiết có đủ cho mọi công tác chính (ví dụ có cọc khoan nhồi mà chỉ có mục ép cọc; trạm XLNT thiếu thử kín bể, chạy thử).
3. Nhân sự đoàn: số lượng, chuyên ngành, chứng chỉ phù hợp hạng công trình và hợp đồng.
4. Điều khoản pháp lý viện dẫn đúng văn bản 2026 (Luật XD 135/2025/QH15, NĐ 207/2026, NĐ 217/2026, NĐ 212/2026, TT 32/2026/TT-BXD); nhắc chạy TEXO Legal Reviewer cho danh mục tiêu chuẩn.
5. Cam kết vượt hợp đồng hoặc bất lợi cho TEXO (thời hạn phản hồi quá ngắn, nhận trách nhiệm thay nhà thầu…).
6. Bìa, tờ lót, mục lục, header/footer; tên dự án/CĐT thống nhất; không có tên Trung tâm.

**Bước 3 – Phiếu:** phiếu Word do script tạo theo mẫu `texo-mau-trinhbay` (A4, header 3 cột, KPI, khối ký "TRƯỞNG PHÒNG / KỸ THUẬT"). Phát hiện ở Bước 2 bổ sung vào mục 1 của phiếu; render kiểm tra (`soffice --headless --convert-to pdf`) trước khi giao.

**Bước 4 – Trả lời anh Vũ:** kết luận + 3–5 việc phải xử lý + file phiếu + nhắc rà soát pháp lý bằng TEXO Legal Reviewer. Ý kiến ghi VPĐT/Zalo: không markdown, "+" ý chính, "-" ý phụ. Đề cương nằm trong thư mục dự án thì ghi `NHAT_KY_KIEM_TRA.md` ở thư mục đó.

## 2. Cập nhật bộ công cụ (khi anh Vũ nhờ)
Chi tiết: `references/CAP_NHAT.md`. Tóm tắt:

| Anh Vũ nhờ | Em làm |
|---|---|
| Cập nhật văn bản pháp luật | Sửa `core/data/phap_ly.json` (hiện hành / hết hiệu lực / cần rà soát, ngày cập nhật) → `dong-bo` |
| Cập nhật tiêu chuẩn hạng mục | Sửa `tieu_chuan`, `tieu_chuan_tham_chieu` của hạng mục trong `thu_vien_hang_muc.json` (hoặc nguồn trong `_build`) → `dong-bo` |
| Thêm đề cương mẫu mới | Chép vào thư mục `De cuong` → `quet` (chấm, ghi sổ nguồn) → chọn phần tốt hơn thư viện hiện tại → khai báo nguồn trong `_build/build_library.py` (hoặc `thu_vien_bo_sung.json` cho PDF) → `dung-lai` → `dong-bo` |
| Thêm/đổi tiêu chí khung | Sửa `core/data/khung_tieuchi.json` → chạy thử trên vài đề cương → `dong-bo` |

Lệnh (trong thư mục bộ công cụ): `python _build/cap_nhat.py quet | dung-lai | dong-bo "nội dung" [patch|minor|major]`. Lệnh `dong-bo` tăng phiên bản, ghi `CHANGELOG.md`, chép lõi sang cả hai skill trong `_skills/` và đóng gói lại `texo-kiemtra-decuong.skill`, `texo-lap-decuong.skill`. Sau đó cập nhật `NHAT_KY.md` và gửi anh hai file .skill mới.

## 3. Tham khảo
`references/khung_chuan.md` (66 tiêu chí, 60 hạng mục), `references/doi_chieu_mau_cac_trung_tam.md` (kết quả 16 bộ đề cương), `references/CAP_NHAT.md`.

## 4. Lưu ý
- Không ghi nhãn phương pháp tư duy, cách trình bày vào phiếu hay đề cương.
- Đóng gói skill: luôn xuất `.skill`.
- Tên người xây dựng chỉ ghi kín đáo (dòng nhỏ cuối thanh bên app, cuối README); không chèn thêm vào phiếu, đề cương.

_Người xây dựng: Hoàng Đức Vũ – Phòng Kỹ thuật._
