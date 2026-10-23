# -*- coding: utf-8 -*-
"""Lớp AI (tùy chọn) trên nền kết quả rule-based – kiểm tra và lập đề cương TVGS.
Không có API key → hai app vẫn chạy đầy đủ bằng bộ quy tắc."""
import json

from . import extract as ex
from . import llm

SYS_CHECK = (
    "Bạn là chuyên gia tư vấn giám sát thi công xây dựng tại Việt Nam, làm việc tại Phòng Kỹ thuật một công ty tư vấn hạng I. "
    "Nhiệm vụ: thẩm định nội dung một đề cương tư vấn giám sát (TVGS) do đoàn lập trước khi trình ký. "
    "Kết quả đối chiếu khung chuẩn bằng máy đã có sẵn – KHÔNG lặp lại các mục máy đã nêu; tập trung vào chất lượng nội dung: "
    "sự phù hợp quy mô, loại – cấp công trình; hạng mục giám sát còn thiếu so với công trình thực tế; thông số kỹ thuật, dung sai sai/thiếu; "
    "nhân sự đoàn; trình tự nghiệm thu theo Nghị định 207/2026/NĐ-CP; điều khoản viện dẫn sai văn bản; cam kết vượt hợp đồng hoặc bất lợi cho đơn vị tư vấn "
    "(nhận trách nhiệm thay nhà thầu, thời hạn phản hồi quá ngắn, ký thay chủ đầu tư…); mâu thuẫn số liệu giữa các phần; câu chữ chép từ dự án khác. "
    "Chỉ nêu điều có căn cứ trong văn bản, trích ngắn vị trí. Văn bản pháp luật: chỉ nhắc khi chắc chắn, còn lại ghi 'cần rà soát'. "
    "Trả về DUY NHẤT một JSON hợp lệ, không giải thích ngoài JSON, không rào ```."
)
SCHEMA_CHECK = """{
 "nhan_xet_chung": "2-4 câu đánh giá tổng thể",
 "phat_hien": [{"noi_dung": "vấn đề", "vi_tri": "mục/đoạn trích ngắn", "muc_do": "high|mid|info", "de_xuat": "cách sửa cụ thể"}],
 "diem_tot": ["điểm làm tốt, tối đa 3"]
}"""

SYS_GEN = (
    "Bạn là tư vấn giám sát trưởng giàu kinh nghiệm tại Việt Nam. Viết phần đặc thù cho đề cương TVGS của một công trình cụ thể, "
    "văn phong kỹ thuật, ngắn gọn, đúng thuật ngữ; căn cứ pháp lý hiện hành: Luật Xây dựng 135/2025/QH15, Nghị định 207/2026/NĐ-CP. "
    "Không bịa số liệu không được cung cấp; không nêu tên đơn vị nội bộ, chỉ dùng 'Tư vấn giám sát' hoặc 'TEXO'. "
    "Trả về DUY NHẤT một JSON hợp lệ, không rào ```."
)
SCHEMA_GEN = """{
 "dac_diem": ["3-6 đặc điểm kỹ thuật/thi công đáng chú ý của công trình, mỗi ý 1 câu"],
 "trong_tam": [{"cong_tac": "công tác", "rui_ro": "rủi ro chất lượng/an toàn chính", "bien_phap": "biện pháp giám sát, điểm dừng cần kiểm soát"}],
 "hang_muc_bo_sung": ["mã hạng mục nên bổ sung, chỉ chọn trong danh sách được cung cấp"]
}"""


def _cfg_ok(cfg):
    return bool(cfg and cfg.get("key") and cfg.get("model") and cfg.get("provider"))


def kiem_tra(blocks, res, cfg, max_chars=60000):
    """Trả {ok, data|error}. data theo SCHEMA_CHECK."""
    if not _cfg_ok(cfg):
        return {"ok": False, "error": "Chưa cấu hình AI."}
    text = ex.full_text(blocks)
    if len(text) > max_chars:
        text = text[: int(max_chars * 0.7)] + "\n…(lược bớt)…\n" + text[-int(max_chars * 0.3):]
    may = {
        "mau": res["muc_mau"], "diem": res["diem"],
        "chua_dat": [f"{r['id']} {r['ten']}: {r['trang_thai']}" for r in res["tieu_chi"] if r["trang_thai"] != "Đạt"],
        "hang_muc": [f"{h['ten']}: {h['trang_thai']}" for h in res["hang_muc"]],
        "het_hieu_luc": [h["ten"] for h in res["phap_ly"]["het"]],
        "nghi_lan_ten": res["chat_luong"]["nghi_lan_ten"],
    }
    user = ("KẾT QUẢ ĐỐI CHIẾU BẰNG MÁY (đã có, không lặp lại):\n" + json.dumps(may, ensure_ascii=False) +
            "\n\nYÊU CẦU: trả JSON theo mẫu:\n" + SCHEMA_CHECK + "\nTối đa 15 phát hiện, xếp từ nặng đến nhẹ.\n\nNỘI DUNG ĐỀ CƯƠNG:\n" + text)
    return llm.ask_json(cfg["provider"], cfg["model"], cfg["key"], user, cfg.get("base_url"), system=SYS_CHECK)


def lap(info, modules, lib, cfg):
    """Gợi ý phần đặc thù công trình cho đề cương. Trả {ok, data|error}."""
    if not _cfg_ok(cfg):
        return {"ok": False, "error": "Chưa cấu hình AI."}
    keep = ("du_an", "cong_trinh", "dia_diem", "loai_ct", "cap_ct", "so_tang", "so_ham", "dt_san", "chieu_cao",
            "mong", "ket_cau", "mo_ta_quy_mo", "thoi_gian")
    tt = {k: info.get(k) for k in keep if info.get(k)}
    ds = {m["id"]: m["ten"] for m in lib}
    user = ("THÔNG TIN CÔNG TRÌNH:\n" + json.dumps(tt, ensure_ascii=False, default=str) +
            "\n\nHẠNG MỤC ĐÃ CHỌN: " + ", ".join(ds.get(m, m) for m in modules) +
            "\n\nDANH SÁCH MÃ HẠNG MỤC CÓ THỂ BỔ SUNG: " + json.dumps({k: v for k, v in ds.items() if k not in modules}, ensure_ascii=False) +
            "\n\nTrả JSON theo mẫu:\n" + SCHEMA_GEN + "\nTrọng tâm giám sát 4-8 dòng.")
    return llm.ask_json(cfg["provider"], cfg["model"], cfg["key"], user, cfg.get("base_url"), system=SYS_GEN)
