# Cơ chế cập nhật – Bộ công cụ Đề cương TVGS TEXO

Mọi cập nhật do anh Vũ chỉ đạo, Claude thực hiện. Một bộ dữ liệu duy nhất (`core/data/`) dùng chung cho 2 app và 2 skill, nên chỉ sửa một chỗ rồi đồng bộ.

## 1. Bộ dữ liệu
| File | Nội dung |
|---|---|
| `core/data/VERSION.json` | Phiên bản, ngày, người xây dựng, số đề cương nguồn |
| `core/data/phap_ly.json` | Văn bản hiện hành / hết hiệu lực (thay bằng gì) / cần rà soát; `ngay_cap_nhat` |
| `core/data/khung_tieuchi.json` | 66 tiêu chí khung chuẩn (B bắt buộc, N nâng cao) |
| `core/data/thu_vien_hang_muc.json` | 60 hạng mục giám sát chi tiết (sinh tự động – không sửa tay, sửa ở nguồn) |
| `core/data/noi_dung_nang_cao.json` | Các mục của mẫu Nâng cao (sinh tự động) |
| `_build/so_de_cuong_nguon.json` | Sổ các đề cương nguồn đã quét: đơn vị, mẫu, điểm, đã đưa vào thư viện chưa |
| `_build/thu_vien_bo_sung.json` | Hạng mục soạn tay (từ đề cương PDF không bóc bảng tự động được) |
| `CHANGELOG.md` | Lịch sử phiên bản |

## 2. Các tình huống
**a) Có văn bản pháp luật mới / văn bản hết hiệu lực**
1. Thêm vào `hien_hanh` (ký hiệu, ngày, nội dung, nhóm, mẫu B/N); chuyển văn bản cũ sang `het_hieu_luc` kèm `thay_the`; văn bản chưa chắc chắn → `can_ra_soat`. Sửa `ngay_cap_nhat`.
2. Nếu văn bản cũ còn trong thư viện nội dung: thêm luật thay thế vào `REPL` trong `_build/build_library.py` và `_build/build_snippets.py`, chạy `dung-lai`.
3. `python _build/cap_nhat.py dong-bo "Cập nhật pháp lý: …" minor`.
4. Đối chiếu bằng TEXO Legal Reviewer.

**b) Cập nhật tiêu chuẩn của một hạng mục**
- Hạng mục bóc từ đề cương: sửa tiêu chuẩn trong đề cương nguồn tốt nhất (hoặc thêm luật thay chữ trong `REPL`), chạy `dung-lai`.
- Hạng mục soạn tay: sửa `_build/thu_vien_bo_sung.json`, chạy `dung-lai`.
- `dong-bo "Cập nhật tiêu chuẩn …"`.

**c) Có đề cương mẫu mới của Trung tâm**
1. Chép vào `D:\Ktra HS\De cuong` (đặt tên bắt đầu bằng mã Trung tâm, ví dụ `TT18 …`; bộ nhiều file thì để chung một thư mục con).
2. `python _build/cap_nhat.py quet` → xem `_build/BAO_CAO_NGUON.md` (điểm, mẫu, văn bản 2026, mới).
3. Claude đọc đề cương mới, so với thư viện: hạng mục nào tốt hơn/mới (bảng rõ ràng, căn cứ 2026, có điểm HP/WP) thì khai báo nguồn trong `MODULES` của `_build/build_library.py`; mục quản lý nâng cao tốt hơn thì khai báo trong `_build/build_snippets.py`.
4. `dung-lai` → chạy thử app Tạo và app Kiểm tra → `dong-bo "Thêm đề cương … vào thư viện" minor`.
5. Đánh dấu `da_dua_vao_thu_vien` trong sổ nguồn, ghi `NHAT_KY.md`.

**d) Thêm/đổi tiêu chí khung chuẩn** – sửa `khung_tieuchi.json`, chạy thử trên các đề cương trong sổ nguồn, `dong-bo`.

## 3. Lệnh
```bash
python _build/cap_nhat.py quet                        # dò, chấm đề cương nguồn, ghi sổ + BAO_CAO_NGUON.md
python _build/cap_nhat.py dung-lai                    # dựng lại thư viện hạng mục và mục nâng cao
python _build/cap_nhat.py dong-bo "nội dung" [patch|minor|major]   # tăng phiên bản, CHANGELOG, chép lõi sang skill, đóng gói .skill
```
Biến `DC_SRC` đổi thư mục đề cương nguồn nếu cần. Sau `dong-bo`: cài lại hai file `texo-kiemtra-decuong.skill`, `texo-lap-decuong.skill`; khởi động lại app.
