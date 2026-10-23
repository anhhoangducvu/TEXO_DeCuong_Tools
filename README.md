# TEXO – Bộ công cụ Đề cương TVGS (v1.1 · 23/10/2026)

| Thành phần | Chạy / cài | Việc |
|---|---|---|
| App Tạo đề cương | `Chay_app_TAO_de_cuong.bat` (cổng 8511) | Nhập thông tin, quy mô → gợi ý mẫu Cơ bản/Nâng cao, hạng mục, nhân sự → đề cương Word mang tên Công ty TEXO, tự kiểm lại |
| App Kiểm tra đề cương | `Chay_app_KIEM_TRA_de_cuong.bat` (cổng 8512) | Tải đề cương (.docx/.pdf, nhiều file) → điểm khung, việc phải xử lý, hạng mục, pháp lý, lẫn tên, lộ tên đơn vị nội bộ → phiếu Word P.KT |
| Skill `texo-lap-decuong.skill` | Lưu vào Claude | Lập đề cương bằng Claude |
| Skill `texo-kiemtra-decuong.skill` | Lưu vào Claude | Kiểm tra đề cương; thực hiện cập nhật bộ công cụ |

Lần đầu: `Cai_dat_lan_dau.bat`. Mật khẩu mặc định `texo2026` (đổi bằng biến môi trường `APP_PASSWORD`).

Sau khi đăng nhập, thanh bên trái gồm: người ký kiểm (người kiểm tra, người duyệt – in vào phiếu) và Trợ lý AI tùy chọn (Claude, Gemini, ChatGPT hoặc endpoint tương thích OpenAI; tự lấy danh sách model, kiểm tra kết nối, có thể lưu key trên máy). Không bật AI thì công cụ chạy bằng bộ quy tắc. Bật AI: app Kiểm tra thêm mục *Nhận xét chuyên môn* vào phiếu; app Tạo thêm mục *Đặc điểm công trình và trọng tâm giám sát* và gợi ý hạng mục nên bổ sung.

## Quy tắc
- **Pháp lý mới nhất:** công cụ chỉ dò theo danh mục văn bản đang theo dõi. Bắt buộc rà soát văn bản pháp luật, tiêu chuẩn viện dẫn bằng công cụ **TEXO Legal Reviewer** trước khi trình ký, phát hành.
- **Đối ngoại:** đề cương gửi Chủ đầu tư chỉ mang tên Công ty Cổ phần TEXO Tư vấn và Đầu tư; tên Trung tâm, VPĐT, Phòng Kỹ thuật là nội bộ (app Kiểm tra bắt lỗi này ở tiêu chí HT06).
- Đơn vị lập (nội bộ): Trung tâm 01, 02, 03, 05–12, 18.

## Cấu trúc
- `core/` – lõi dùng chung; `core/data/` – khung 66 tiêu chí, thư viện 60 hạng mục, mục Nâng cao, danh mục pháp lý, `VERSION.json`.
- `_build/` – dựng lại thư viện từ đề cương nguồn, sổ đề cương nguồn, lệnh cập nhật `cap_nhat.py`.
- `_skills/` – mã nguồn 2 skill (lệnh đồng bộ chép lõi sang và đóng gói .skill).
- `CAP_NHAT.md` – cơ chế cập nhật; `CHANGELOG.md` – lịch sử phiên bản; `NHAT_KY.md` – nhật ký làm việc.
- `Ket_qua_kiem_tra/` – phiếu kiểm tra 16 bộ đề cương mẫu; `De_cuong_mau_vi_du/` – 4 đề cương mẫu (dự án giả định).

_Người xây dựng: Hoàng Đức Vũ – Phòng Kỹ thuật._
