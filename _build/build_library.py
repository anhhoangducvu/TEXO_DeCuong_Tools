# -*- coding: utf-8 -*-
"""Bước 2: dựng thư viện hạng mục giám sát chi tiết từ các bộ đề cương mẫu của các Trung tâm.
Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật TEXO.
Thêm đề cương mới: khai báo vào SRC/NGUON, rồi thêm/đổi nguồn trong MODULES."""
import json, re, os, unicodedata
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
ROOT = _os.path.dirname(HERE)
SRC_DIR = _os.environ.get("DC_SRC") or _os.path.dirname(ROOT)   # thư mục chứa các đề cương nguồn (mặc định: thư mục cha của bộ công cụ)
BLOCKS = _os.path.join(HERE, "_blocks")
DATA = _os.path.join(ROOT, "core", "data")
B = BLOCKS + "/"
SRC = {
    "TAS": "TT12 250415 De cuong TVGS Taseco Long Thanh__1744702170de-cuong-tvgs-nha-suat-an-long-thanh.json",
    "T03X": "TT03 250321 De cuong TVGS The Charm An Hung__phan 3_chuong 1_muc 4a_De cuong chi tiet_XD.json",
    "T03M": "TT03 250321 De cuong TVGS The Charm An Hung__phan 3_chuong 1_mục 4b_De cuong chi tiet_MEP.json",
    "T12": "TT12 Mau de cuong co ban__De cuong TVGS - TT12 - Mau co ban.json",
    "HAR": "TT09 De-cuong-TVGS_Harmonia_Bay-Da-Nang-17-10-2026-4b3388.json",
    "T08": "TT08 231223 De cuong TVGS Thi Cong Hang Muc Khoan Khao Sat Dia Chat – Phuc Vu Lap Bao Cao Nghien Cuu Kha Thi.json",
    "TRD": "TT09 De cuong giam sat Trac dac.json",
    "T6C": "TT6 De cuong GS coc ep.json",
    "T6X": "TT6 DE-CUONG-GIAM-SAT-TEXO-Tram-XLNT.json",
    "T6H": "TT6 De cuong Ha tang.json",
}
NGUON = {"TAS": "TT12 – Taseco Long Thành (04/2025)", "T03X": "TT03 – The Charm An Hưng (03/2025)",
         "T03M": "TT03 – The Charm An Hưng (03/2025)", "T12": "TT12 – Mẫu cơ bản",
         "HAR": "TT09 – Harmonia Bay Đà Nẵng (10/2026)", "T08": "TT08 – Khoan khảo sát địa chất",
         "TRD": "TT09 – Giám sát trắc đạc", "T6C": "TT06 – Cọc ép (2026)", "T6X": "TT06 – Trạm XLNT (2026)",
         "T6H": "TT06 – Hạ tầng (2026)"}
DOCS = {k: json.load(open(B + v)) for k, v in SRC.items()}

# (id, tên, nhóm, từ khóa nhận diện trong đề cương, [(nguồn, regex tiêu đề bắt đầu, min_index, regex kết thúc|None)], checklist nguồn)
MODULES = [
 ("NANGLUC", "Kiểm tra sự phù hợp năng lực của nhà thầu thi công", "Chung", ["năng lực.{0,30}nhà thầu"], [("TAS", r"^kiểm tra sự phù hợp năng lực", 300, None)]),
 ("VATLIEU", "Giám sát vật liệu, thiết bị, sản phẩm chế tạo sẵn lắp đặt vào công trình", "Chung", ["vật liệu.{0,30}(chế tạo sẵn|thiết bị)", "nghiệm thu vật liệu"], [("TAS", r"^Giám sát vật liệu, thiết bị chế tạo sẵn", 300, None)]),
 ("TRACDIA", "Giám sát công tác trắc địa", "Chung", ["trắc địa", "trắc đạc"], [("TAS", r"^Giám sát công tác trắc địa", 300, None)]),
 ("EPCOC", "Giám sát thi công ép cọc (đóng, ép cọc BTCT)", "Nền móng", ["ép cọc", "cọc ép", "đóng cọc"], [("T6C", r"^II\. GIÁM SÁT THI CÔNG ÉP CỌC", 200, r"^PHẦN 4")]),
 ("TNCOC", "Giám sát công tác thí nghiệm cọc", "Nền móng", ["thí nghiệm cọc", "nén tĩnh", "\\bpda\\b", "\\bpit\\b"], [("T12", r"^GIÁM SÁT CÔNG TÁC THÍ NGHIỆM CỌC", 100, None)]),
 ("KHOANNHOI", "Giám sát thi công cọc khoan nhồi, hạ Kingpost", "Nền móng", ["khoan nhồi", "kingpost", "barrette"], [("HAR", r"^3\. Giám sát thi công cọc khoan nhồi", 500, r"^4\. Giám sát đào đất")]),
 ("TUONGVAY", "Giám sát thi công tường vây (tường trong đất)", "Nền móng", ["tường vây", "tường trong đất", "diaphragm"], [("HAR", r"^2\. Giám sát thi công tường vây", 500, r"^3\. Giám sát thi công cọc")]),
 ("MONG", "Giám sát thi công phần móng (đào đất, bê tông lót, móng, lấp đất)", "Nền móng", ["phần móng", "đài móng", "hố móng", "giám sát móng"], [("TAS", r"^Giám sát phần móng", 300, None)]),
 ("HAM", "Giám sát đào đất, hệ chống và kết cấu tầng hầm", "Nền móng", ["tầng hầm", "top.?down", "hệ chống"], [("HAR", r"^4\. Giám sát đào đất và hệ chống", 500, r"^6\. Giám sát thi công kết cấu thân")]),
 ("BTCT", "Giám sát kết cấu bê tông cốt thép toàn khối (cốp pha, cốt thép, bê tông)", "Kết cấu", ["bê tông cốt thép toàn khối", "btct toàn khối", "cốp ?pha", "ván khuôn"], [("TAS", r"^Giám sát hạng mục kết cấu bê tông cốt thép toàn khối", 300, None)]),
 ("DUL", "Giám sát thi công cáp dự ứng lực", "Kết cấu", ["dự ứng lực", "ứng lực trước", "\\bdul\\b"], [("HAR", r"^6\.1\.3 Giám sát thi công cáp dự ứng lực", 500, r"^6\.2 Giám sát thi công kết cấu thép")]),
 ("KCTHEP", "Giám sát gia công, lắp dựng kết cấu thép", "Kết cấu", ["kết cấu thép", "nhà thép", "lắp dựng thép"], [("HAR", r"^6\.2 Giám sát thi công kết cấu thép", 500, r"^7\. Giám sát lắp đặt hệ thống MEP")]),
 ("CHONGTHAM", "Giám sát thi công chống thấm", "Hoàn thiện", ["chống thấm"], [("TAS", r"^Giám sát thi công chống thấm", 300, None)]),
 ("XAYTRAT", "Giám sát xây, trát, ốp, lát, láng", "Hoàn thiện", ["xây,? trát", "xây tường", "ốp,? lát", "láng"], [("TAS", r"^Giám sát hạng mục hoàn thiện: xây", 300, None)], "T03X:xây|trát|láng|lát|ốp"),
 ("CUANHOM", "Giám sát lắp đặt cửa, vách nhôm kính, cửa nhựa", "Hoàn thiện", ["nhôm kính", "cửa nhựa", "vách kính"], [("TAS", r"^Giám sát lắp đặt hệ cửa nhôm kính", 300, None)], "T03X:nhôm kính"),
 ("CUAGO", "Giám sát gia công, lắp đặt cửa gỗ", "Hoàn thiện", ["cửa gỗ"], [("TAS", r"^Giám sát gia công và lắp đặt cửa gỗ", 300, None)], "T03X:khuôn cửa|cánh cửa"),
 ("CUACC", "Giám sát lắp đặt cửa thép chống cháy", "Hoàn thiện", ["cửa (thép )?chống cháy"], [("TAS", r"^Giám sát lắp đặt cửa thép chống cháy", 300, None)]),
 ("SONBA", "Giám sát thi công sơn, bả", "Hoàn thiện", ["sơn,? bả", "sơn tường", "bả mastic"], [("TAS", r"^Giám sát hạng mục thi công sơn bả", 300, None)], "T03X:bả mastic|sơn lót|sơn phủ|trước khi sơn"),
 ("TRAN", "Giám sát thi công trần, vách thạch cao", "Hoàn thiện", ["thạch cao", "đóng trần"], [("TAS", r"^Giám sát thi công trần thạch cao", 300, None)], "T03X:trần thạch cao|trần chìm"),
 ("CHONGMOI", "Giám sát công tác phòng chống mối", "Hoàn thiện", ["chống mối", "phòng mối"], [("TAS", r"^Giám sát công tác chống mối", 300, None)]),
 ("EPOXY", "Giám sát thi công sơn epoxy sàn, nền", "Hoàn thiện", ["epoxy"], [("T03X", r"^giám sát thi công sơn epoxy", 0, None)]),
 ("SANGO", "Giám sát thi công sàn gỗ", "Hoàn thiện", ["sàn gỗ"], [("T03X", r"^giám sát thi công SÀN GỖ", 0, None)], "T03X:sàn gỗ"),
 ("NOITHAT", "Giám sát lắp đặt nội thất, tủ bếp, thiết bị gia dụng", "Hoàn thiện", ["nội thất", "tủ bếp"], [("T03X", r"^GIÁM SÁT THI CÔNG LẮP ĐẶT NỘI THẤT", 0, None)], "T03X:tủ bếp|bếp từ"),
 ("LANCAN", "Giám sát lắp đặt lan can", "Hoàn thiện", ["lắp đặt lan can", "thi công lan can"], [("HAR", r"^10\.5 Giám sát thi công lắp đặt lan can", 500, r"^10\.6 Giám sát thi công lắp đặt cửa")]),
 ("TBVS", "Giám sát lắp đặt thiết bị vệ sinh", "Hoàn thiện", ["thiết bị vệ sinh"], [("HAR", r"^10\.9 Giám sát lắp đặt thiết bị vệ sinh", 500, r"^10\.10 Giám sát lắp đặt")]),
 ("MEPCHUNG", "Giám sát thi công hệ thống cơ điện – phần chung", "Cơ điện (MEP)", ["cơ điện.{0,10}phần chung", "\\bmep\\b"], [("TAS", r"^Giám sát thi công hệ thống cơ điện", 300, None)]),
 ("ONGDIEN", "Giám sát lắp đặt ống luồn dây điện âm tường, âm sàn, đi nổi", "Cơ điện (MEP)", ["ống (luồn|điện)"], [("TAS", r"^Giám sát lắp đặt ống điện âm tường", 300, None)], "T03M:ống luồn dây"),
 ("RANHCAP", "Giám sát rãnh cáp, ống bảo vệ cáp chôn ngầm", "Cơ điện (MEP)", ["rãnh cáp", "cáp chôn ngầm"], [("TAS", r"^Giám sát rãnh cáp", 300, None)]),
 ("MANGCAP", "Giám sát lắp đặt thang, máng cáp, trunking", "Cơ điện (MEP)", ["máng cáp", "thang cáp", "trunking"], [("TAS", r"^giám sát lắp đặt thang, máng cáp", 300, None)], "T03M:thang máng cáp"),
 ("CAPDIEN", "Giám sát kéo rải dây, cáp điện", "Cơ điện (MEP)", ["kéo rải", "rải cáp"], [("TAS", r"^Giám sát kéo rải cáp điện", 300, None)], "T03M:kéo rải"),
 ("TBDIEN", "Giám sát lắp đặt thiết bị điện", "Cơ điện (MEP)", ["thiết bị điện"], [("TAS", r"^Giám sát lắp đặt thiết bị điện", 300, None)], "T03M:lắp đặt thiết bị điện"),
 ("MAYPHAT", "Giám sát lắp đặt máy phát điện dự phòng", "Cơ điện (MEP)", ["máy phát"], [("TAS", r"^Giám sát lắp đặt máy phát điện", 300, None)]),
 ("CHONGSET", "Giám sát lắp đặt hệ thống chống sét, tiếp địa", "Cơ điện (MEP)", ["chống sét", "tiếp địa"], [("TAS", r"^Giám sát lắp đặt hệ thống chống sét", 300, None)]),
 ("TBA", "Giám sát lắp đặt trạm biến áp", "Cơ điện (MEP)", ["trạm biến áp", "máy biến áp"], [("TAS", r"^Giám sát lắp đặt trạm biến áp", 300, None)]),
 ("CSNGOAI", "Giám sát lắp đặt hệ thống chiếu sáng ngoài nhà", "Cơ điện (MEP)", ["chiếu sáng ngoài nhà", "chiếu sáng (công cộng|đường)"], [("TAS", r"^Giám sát lắp đặt hệ thống chiếu sáng ngoài nhà", 300, None)]),
 ("CTN", "Giám sát lắp đặt hệ thống cấp thoát nước", "Cơ điện (MEP)", ["cấp thoát nước", "cấp nước", "thoát nước"], [("TAS", r"^Giám sát lắp đặt hệ thống cấp thoát nước", 300, None)], "T03M:đường ống thoát nước|đường ống cấp nước|thử kín đường ống thoát|thử áp đường ống cấp"),
 ("HVAC", "Giám sát lắp đặt hệ thống thông gió, điều hòa không khí", "Cơ điện (MEP)", ["điều hòa", "điều hoà", "thông gió", "hvac"], [("TAS", r"^Giám sát lắp đặt hệ thống thông gió", 300, None)], "T03M:nước ngưng|máy điều hòa"),
 ("PCCC", "Giám sát thi công hệ thống phòng cháy chữa cháy", "Cơ điện (MEP)", ["phòng cháy chữa cháy", "báo cháy", "chữa cháy", "sprinkler"], [("TAS", r"^Giám sát thi công hệ thống phòng cháy", 300, None)], "T03M:báo cháy|chữa cháy|sprinkler"),
 ("DIENNHE", "Giám sát hệ thống điện nhẹ: camera, truyền hình, loa, điện thoại, mạng", "Cơ điện (MEP)", ["camera", "điện nhẹ", "internet", "loa thông báo"], [("TAS", r"^Giám sát thi công hệ thống camera", 300, None)], "T03M:internet|camera"),
 ("THANGMAY", "Giám sát lắp đặt thang máy", "Cơ điện (MEP)", ["thang máy"], [("TAS", r"^Giám sát lắp đặt thang máy", 300, None)]),
 ("BUSWAY", "Giám sát lắp đặt hệ thống busway", "Cơ điện (MEP)", ["busway", "thanh dẫn"], [("T03M", r"^giám sát lắp đặt hệ thống busway", 0, None)]),
 ("BMS", "Giám sát lắp đặt hệ thống quản lý tòa nhà BMS", "Cơ điện (MEP)", ["\\bbms\\b", "quản lý tòa nhà"], [("T03M", r"^giám sát lắp đặt hệ thống quản lý to", 0, None)]),
 ("KSXE", "Giám sát hệ thống kiểm soát xe tự động", "Cơ điện (MEP)", ["kiểm soát xe", "bãi đỗ xe"], [("T03M", r"^giám sát hệ thống kiểm soát xe", 0, None)]),
 ("XLNT", "Giám sát lắp đặt hệ thống xử lý nước thải", "Cơ điện (MEP)", ["xử lý nước thải", "\\bxlnt\\b"], [("HAR", r"^7\.7 Giám sát lắp đặt hệ thống xử lý nước thải", 500, r"^8\. Giám sát công tác hoàn thiện thô")]),
 ("HTKT", "Giám sát thi công hạ tầng kỹ thuật, đường giao thông, sân đường nội bộ", "Hạ tầng", ["hạ tầng kỹ thuật", "đường giao thông", "sân đường", "đường nội bộ"], [("T03X", r"^GIÁM SÁT THI CÔNG hạ tầng kỹ thuật", 0, None), ("T6H", r"^giám sát HẠ TẦNG, đường giao thông nội bộ", 200, None)]),
 ("CAYXANH", "Giám sát thi công cảnh quan, cây xanh", "Hạ tầng", ["cây xanh", "cảnh quan"], [("T03X", r"^GIÁM SÁT THI CÔNG cây xanh", 0, None), ("T6H", r"^giám sát trồng cây xanh", 200, None)]),
 ("KHOANKS", "Giám sát khoan khảo sát địa chất công trình", "Chuyên đề", ["khảo sát địa chất", "khoan khảo sát", "hố khoan"], [("T08", r"^II\. GIÁM SÁT THI CÔNG KHOAN KHẢO SÁT", 400, None)]),
 ("TRACDAC", "Giám sát thi công trắc đạc, quan trắc (gói chuyên đề)", "Chuyên đề", ["quan trắc", "trắc đạc"], [("TRD", r"^II\. GIÁM SÁT CÔNG TÁC THI CÔNG TRẮC ĐẠC", 300, None)]),
 ("DAODAT", "Giám sát công tác đất: hố đào, hạ mực nước ngầm, đắp – lấp hoàn trả, san nền", "Nền móng", ["công tác đất", "hố đào", "đào đất", "san nền", "đắp đất"], [("T6X", r"^IV\. GIÁM SÁT CÔNG TÁC ĐẤT", 200, r"^V\. GIÁM SÁT CỌC")]),
 ("BE_BTCT", "Giám sát kết cấu BTCT bể công nghệ (bể chứa, bể xử lý)", "Công trình xử lý nước thải", ["bể công nghệ", "bể xử lý", "bể chứa"], [("T6X", r"^VI\. GIÁM SÁT KẾT CẤU BTCT CÁC BỂ", 200, r"^VII\.")]),
 ("BE_THAM", "Giám sát chống thấm, khe – mạch ngừng và thử kín bể", "Công trình xử lý nước thải", ["thử kín bể", "waterstop", "mạch ngừng"], [("T6X", r"^VII\. GIÁM SÁT CHỐNG THẤM", 200, r"^VIII\.")]),
 ("ONG_CN", "Giám sát lắp đặt đường ống công nghệ (HDPE, uPVC, thép, inox), thử áp, súc rửa", "Công trình xử lý nước thải", ["đường ống công nghệ", "test pack", "súc rửa"], [("T6X", r"^X\. GIÁM SÁT ĐƯỜNG ỐNG CÔNG NGHỆ", 200, r"^XI\.")]),
 ("TB_CN", "Giám sát lắp đặt thiết bị cơ khí – công nghệ (bơm, máy thổi khí, khuấy, hóa chất)", "Công trình xử lý nước thải", ["thiết bị công nghệ", "thiết bị cơ khí", "máy thổi khí", "bơm định lượng"], [("T6X", r"^XI\. GIÁM SÁT LẮP ĐẶT THIẾT BỊ CƠ KHÍ", 200, r"^XII\.")]),
 ("DIEN_DK", "Giám sát điện động lực, điều khiển, đo lường (MCC, PLC/SCADA, loop test)", "Công trình xử lý nước thải", ["plc", "scada", "loop test", "điều khiển"], [("T6X", r"^XII\. GIÁM SÁT HỆ THỐNG ĐIỆN ĐỘNG LỰC", 200, r"^XIII\.")]),
 ("AT_HC", "Giám sát an toàn hóa chất, không gian hạn chế, nâng hạ thiết bị", "Công trình xử lý nước thải", ["hóa chất", "không gian hạn chế"], [("T6X", r"^XIV\. GIÁM SÁT AN TOÀN HÓA CHẤT", 200, r"^XV\.")]),
 ("CHAYTHU_CN", "Giám sát chạy thử, commissioning và vận hành thử công nghệ", "Công trình xử lý nước thải", ["commissioning", "vận hành thử", "chạy thử liên động"], [("T6X", r"^XV\. GIÁM SÁT THỬ NGHIỆM, CHẠY THỬ", 200, r"^XVI\."), ("T6X", r"^XVI\. GIÁM SÁT VẬN HÀNH THỬ CÔNG NGHỆ", 200, r"^XVII\.")]),
 ("ITP_CN", "Kiểm tra theo ma trận điểm kiểm soát tối thiểu (ITP tóm tắt) công trình công nghệ", "Công trình xử lý nước thải", ["ma trận điểm kiểm soát", "itp tóm tắt", "hold point"], [("T6X", r"^XIX\. MA TRẬN ĐIỂM KIỂM SOÁT", 200, r"^XX\.")]),
 ("CHAYTHU", "Giám sát chạy thử, nghiệm thu và bàn giao đưa công trình vào sử dụng", "Chung", ["chạy thử", "bàn giao"], [("HAR", r"^11\. Giám sát chạy thử", 500, r"^PHẦN C")]),
 ("ATLD", "Giám sát an toàn lao động, PCCC, vệ sinh môi trường tại hiện trường", "Chung", ["an toàn lao động"], [("T12", r"^GIÁM SÁT AN TOÀN LAO ĐỘNG, PCCC", 100, None)]),
]

STD_RE = re.compile(r"^[-–•+\s]*(TCVN|QCVN|TCXD|TCXDVN|TCN|22 ?TCN|ASTM|BS|EN|ISO|IEC|ACI|NFPA|JIS|AASHTO|Thông tư|Nghị định|Luật|TCCS|CĐKT|Chỉ dẫn|chỉ dẫn|Biện pháp thi công|Bản vẽ|Hồ sơ thiết kế|HSTK|BPTC|Tiêu chí|Đề cương thí nghiệm|Danh mục)", re.I)
HS_RE = re.compile(r"^[-–•+\s]*(X[aá]c nh[aậ]n|Biên bản|Phiếu|Nhật ký|Hồ sơ nghiệm thu)", re.I)
REPL = [
    (r"Nghị định (số )?06/2021/NĐ-CP( ngày 26/0?1/2021)?( của Chính phủ)?", "Nghị định số 207/2026/NĐ-CP"),
    (r"Nghị định (số )?06/2021/CP( ngày 26/0?1/2021)?( của Chính phủ)?", "Nghị định số 207/2026/NĐ-CP"),
    (r"NĐ 06/2021(/NĐ-CP)?", "NĐ 207/2026/NĐ-CP"),
    (r"Nghị định (số )?175/2024/NĐ-CP", "Nghị định số 217/2026/NĐ-CP"),
    (r"Thông tư (số )?10/2021/TT-BXD", "Thông tư số 32/2026/TT-BXD"),
    (r"\(?(Điều|điều) \d+ (của )?Nghị định số 207/2026/NĐ-CP\)?", "theo Nghị định số 207/2026/NĐ-CP"),
    (r"Thông tư liên tịch số 21/2013/TTLT-BXD[^\n]*", "Quy định hiện hành về an toàn điện và hồ sơ thiết kế được duyệt"),
    (r"Taseco|TASECO", "Chủ đầu tư"), (r"Blue ?Land", "Chủ đầu tư"), (r"Harmonia Bay", "dự án"),
    (r" 03 tầng hầm", " các tầng hầm"), (r"Xac nhận", "Xác nhận"), (r"Trungking", "Trunking"), (r"Lắt đặt", "Lắp đặt"),
    (r"quyét", "quét"),
    (r"(Nghị định|NĐ) ?(số )?50/2024/N[DĐ]-CP", "Nghị định số 105/2025/NĐ-CP"),
    (r"Thông tư (số )?149/2020/TT-BCA", "Thông tư số 36/2025/TT-BCA"),
    (r"Luật (PCCC|Phòng cháy và chữa cháy|phòng cháy chữa cháy)[^;,.]*(27/2001/QH10|40/2013/QH13)", "Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ số 55/2024/QH15"),
    (r"Nghị định (số )?136/2020/N[DĐ]-CP", "Nghị định số 105/2025/NĐ-CP"),
    (r"Checlist", "Checklist"),
    (r"thuộc Phụ lục VI nghị định 50/2024/ND-CP", "theo quy định tại Nghị định số 105/2025/NĐ-CP"),
    (r"\(theo NĐ 46/2015/NĐ-CP\)", "(theo Nghị định số 207/2026/NĐ-CP)"),
    (r"…{2,}|\.{4,}", "…"),
    (r"trình tự các tầng hầm semi top-down", "trình tự thi công các tầng hầm theo biện pháp được duyệt"),
    (r"biện pháp semi top-down", "biện pháp thi công tầng hầm"),
    (r"trình tự semi top-down", "trình tự theo biện pháp thi công tầng hầm được duyệt"),
    (r"theo phương pháp semi top-down", "theo biện pháp thi công tầng hầm được duyệt (bottom-up/top-down/semi top-down)"),
    (r"(Nghị định|nghị định|NĐ) ?(số )?175/2024/N[ĐD]-CP", "Nghị định số 212/2026/NĐ-CP"),
    (r"tuân thủ điều 86 nghị định 175/2024", "tuân thủ quy định về điều kiện năng lực tại Nghị định số 212/2026/NĐ-CP"),
    (r"trình tự thi công semi top-down", "trình tự thi công tầng hầm"),
]


def clean(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    for a, b in REPL:
        t = re.sub(a, b, t)
    return t


def strip_bullet(t):
    return re.sub(r"^[-–•+]\s*", "", t).strip()


def norm(t):
    return unicodedata.normalize("NFC", t)


def find_start(doc, rx, mi):
    r = re.compile(rx, re.I)
    for i, b in enumerate(doc):
        if i >= mi and b["k"] == "p" and r.search(b["t"].strip()):
            return i
    return None


def slice_blocks(doc, s, end_rx):
    out = []
    lv0 = doc[s].get("lvl", 0) or 9
    er = re.compile(end_rx, re.I) if end_rx else None
    for b in doc[s + 1:]:
        if b["k"] == "p":
            if er and er.search(b["t"].strip()):
                break
            if not er and b.get("lvl", 0) and b["lvl"] <= lv0 and b.get("st", "").lower().startswith("heading"):
                break
            if not er and b.get("lvl", 0) and b["lvl"] <= lv0:
                break
        out.append(b)
    return out


def colmap(head):
    m = {}
    for j, c in enumerate(head):
        h = " ".join(c).lower()
        if re.fullmatch(r"s?tt", h.strip()):
            m.setdefault("idx", j)
        elif "phương pháp" in h and "nội dung" in h and "kiểm tra giám sát" in h:
            m.setdefault("pp", j)
        elif "tiêu chuẩn" in h or "tài liệu" in h or h.strip().startswith("căn cứ"):
            m.setdefault("tc", j)
        elif "phương pháp" in h or "yêu cầu" in h or "tiêu chí" in h:
            m.setdefault("pp", j)
        elif "nội dung thi công" in h:
            m.setdefault("pp", j)
        elif "thời điểm" in h:
            m.setdefault("pp", j)
        elif h.strip() in ("điểm", "loại", "điểm kiểm soát hp/wp"):
            m.setdefault("diem", j)
        elif ("nội dung" in h or "yêu cầu" in h) and "muc" in m:
            m.setdefault("pp", j)
        elif "nội dung" in h or "công việc" in h or h.strip() in ("đối tượng", "hệ thống", "nhóm thiết bị", "giai đoạn", "nhóm hồ sơ", "điểm kiểm soát"):
            m.setdefault("muc", j)
        elif "hồ sơ" in h or "xác nhận" in h:
            m.setdefault("hs", j)
    return m


def split_item(lines):
    name, tc, hs = [], [], []
    mode = "name"
    merged = []
    for l in lines:
        if merged and re.match(r"^\s*\d{3,5}[\-:]", l) and re.search(r"(TCVN|QCVN|TCXD)\s*$", merged[-1]):
            merged[-1] = merged[-1].rstrip() + " " + l.strip()
        else:
            merged.append(l)
    lines = merged
    for k, l in enumerate(lines):
        l = clean(l)
        if not l:
            continue
        if k == 0:
            if re.search(r"\b(TCVN|QCVN|TCXD)\b", l) and len(l) > 25:
                mm = re.search(r"\b(TCVN|QCVN|TCXD)", l)
                name.append(l[:mm.start()].strip(" /-–"))
                tc.append(l[mm.start():])
            else:
                name.append(strip_bullet(l))
            continue
        if HS_RE.match(l):
            mode = "hs"
            rest = re.sub(r"^[-–•+\s]*X[aá]c nh[aậ]n\s*:?\s*", "", l).strip()
            if rest:
                hs.append(strip_bullet(rest))
            continue
        if mode == "hs":
            hs.append(re.sub(r"^\d+[\.\)]\s*", "", strip_bullet(l)))
            continue
        if STD_RE.match(l) or "tiêu chuẩn" in l.lower() or "quy chuẩn" in l.lower():
            tc.append(strip_bullet(l))
            mode = "tc"
            continue
        if mode == "name" and len(name) == 1 and len(name[0]) < 25 and not re.match(r"^\d+[\.\)]", l):
            name.append(strip_bullet(l))
        else:
            hs.append(re.sub(r"^\d+[\.\)]\s*", "", strip_bullet(l)))
    hs = [h[:1].upper() + h[1:] for h in hs if h]
    return " ".join(x for x in name if x).strip(" :"), tc, hs


def parse_table(rows, cur_group):
    """Trả (các hàng chuẩn hóa, nhóm hiện tại, là_checklist)."""
    out = []
    if not rows:
        return out, cur_group, False
    head = rows[0]
    htxt = " ".join(" ".join(c) for c in head).lower()
    if "đánh giá" in htxt and "công việc kiểm tra" in htxt:
        return rows, cur_group, True
    m = colmap(head) if re.search(r"nội dung|công việc|điểm kiểm soát|đối tượng|hệ thống|nhóm thiết bị", htxt) else {}
    body = rows[1:] if m else rows
    if not m:
        if len(head) == 2:
            m = {"muc": 0, "pp": 1}
        elif len(head) == 5 and re.fullmatch(r"\d+", " ".join(head[0])):
            m = {"idx": 0, "muc": 1, "pp": 2, "tc": 3, "hs": 4}
        else:
            m = {"muc": 0, "pp": len(head) - 1}
    if "muc" not in m:
        m["muc"] = 0 if m.get("idx") != 0 else 1
    if "pp" not in m:
        m["pp"] = len(head) - 1
    for r in body:
        texts = [" ".join(c).strip() for c in r]
        nonempty = [t for t in texts if t]
        if not nonempty:
            continue
        if m.get("idx") is not None and m["idx"] < len(r) and re.fullmatch(r"[A-H]", texts[m["idx"]] or ""):
            cur_group = clean(" ".join(t for j, t in enumerate(texts) if j != m["idx"] and t)).upper()
            continue
        uniq = set(nonempty)
        if len(uniq) == 1 and (len(r) == 1 or len(nonempty) < len(r) or len(nonempty) == len(r)) and len(nonempty[0]) < 90 and (nonempty[0].isupper() or len(r) == 1 or len(nonempty) == len(r)):
            cur_group = clean(nonempty[0]).upper()
            continue
        mu = r[m["muc"]] if m["muc"] < len(r) else []
        name, tc, hs = split_item(mu)
        if m.get("tc") is not None and m["tc"] < len(r):
            tc += [strip_bullet(clean(x)) for x in r[m["tc"]] if clean(x)]
        if m.get("hs") is not None and m["hs"] < len(r):
            hs += [strip_bullet(clean(x)) for x in r[m["hs"]] if clean(x)]
        pp = [strip_bullet(clean(x)) for x in (r[m["pp"]] if m["pp"] < len(r) and m["pp"] != m["muc"] else []) if clean(x)]
        if not name and not pp:
            continue
        diem = " ".join(r[m["diem"]]).strip() if m.get("diem") is not None and m["diem"] < len(r) else ""
        out.append(dict(nhom=cur_group, muc=name, tc=tc, hs=hs, pp=pp, **({"diem": diem} if diem else {})))
    return out, cur_group, False


def parse_slice(blks):
    rows, tieu_chuan, checklists, bang_phu = [], [], [], []
    group, mode, para_row = "", None, None
    for b in blks:
        if b["k"] == "t":
            rr, group, is_ck = parse_table(b["rows"], group)
            if is_ck:
                checklists.append(dict(ten=para_row["muc"] if para_row else "", rows=rr))
            elif rr and not rr[0]["pp"] and len(b["rows"][0]) > 3:
                bang_phu.append(dict(ten=(para_row or {}).get("muc", ""), rows=b["rows"]))
            else:
                rows += rr
            continue
        t = clean(b["t"])
        if not t:
            continue
        low = t.lower()
        if re.match(r"^[\d\.]*\s*(tiêu chuẩn (tham chiếu|và tài liệu áp dụng)|hồ sơ và tiêu chuẩn tham chiếu|các tiêu chuẩn áp dụng)", low):
            mode = "tc"; continue
        is_head = (len(t) < 110 and (re.match(r"^\d+(\.\d+)+\.?\s", t) or (t.endswith(":") and len(t) < 90 and not t.startswith("-"))) )
        if is_head:
            mode = "pp"
            lab = re.sub(r"^\d+(\.\d+)*\.?\s*", "", t).rstrip(":").strip()
            if re.match(r"^nội dung giám sát", lab.lower()):
                lab = "Nội dung giám sát"
            para_row = dict(nhom=group, muc=lab, tc=[], hs=[], pp=[])
            rows.append(para_row)
            continue
        if mode == "tc":
            tieu_chuan.append(strip_bullet(t)); continue
        if para_row is None:
            para_row = dict(nhom=group, muc="Nội dung giám sát", tc=[], hs=[], pp=[])
            rows.append(para_row)
        para_row["pp"].append(strip_bullet(t))
    rows = [r for r in rows if r["pp"] or r["tc"] or r["hs"]]
    return rows, tieu_chuan, checklists, bang_phu


def find_checklists(spec):
    if not spec:
        return []
    src, pats = spec.split(":", 1)
    doc = DOCS[src]
    rx = re.compile(pats, re.I)
    out = []
    for i, b in enumerate(doc):
        if b["k"] == "p" and re.search(r"n[ộo]i dung kiểm tra|nội dung kiểm tra", b["t"], re.I) and rx.search(b["t"]):
            # bảng ngay sau
            for nb in doc[i + 1:i + 3]:
                if nb["k"] == "t":
                    rows = nb["rows"]
                    ht = " ".join(" ".join(c) for c in rows[0]).lower()
                    if "công việc kiểm tra" in ht or "kết quả kiểm tra" in ht:
                        title = re.sub(r"^[\d\.]+\s*", "", clean(b["t"]))
                        out.append(dict(ten=title[:1].upper() + title[1:].lower(), rows=rows))
                    break
    return out


lib = []
for spec in MODULES:
    mid, ten, nhom, kw, srcs = spec[:5]
    ck_spec = spec[5] if len(spec) > 5 else None
    rows_all, tcs, cks, bps, nguon = [], [], [], [], []
    for (sk, rx, mi, er) in srcs:
        doc = DOCS[sk]
        s = find_start(doc, rx, mi)
        if s is None:
            print("!! không thấy", mid, sk, rx); continue
        blks = slice_blocks(doc, s, er)
        rows, tc, ck, bp = parse_slice(blks)
        rows_all += rows; tcs += tc; cks += ck; bps += bp; nguon.append(NGUON[sk])
    cks += find_checklists(ck_spec)
    # gom tiêu chuẩn từ các hàng
    std = []
    for x in tcs + [t for r in rows_all for t in r["tc"]]:
        for piece in re.split(r"\s*;\s*|\s*/\s*", x):
            p = piece.strip(" .;")
            if re.match(r"^(TCVN|QCVN|TCXD|TCXDVN|TCN|ASTM|BS|EN|ISO|IEC|NFPA|ACI|JIS)\b", p) and p not in std:
                std.append(p)
    lib.append(dict(id=mid, ten=ten, nhom=nhom, tu_khoa=kw, nguon=nguon, tieu_chuan_tham_chieu=tcs,
                    tieu_chuan=std, hang=rows_all, checklist=cks, bang_phu=bps))
    print(f"{mid:10s} rows={len(rows_all):3d} tc={len(std):3d} ck={len(cks)} bp={len(bps)}  {ten}")

# hạng mục bổ sung soạn tay từ đề cương PDF (không bóc bảng tự động được)
BS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thu_vien_bo_sung.json")
if os.path.exists(BS):
    for m in json.load(open(BS, encoding="utf-8")):
        lib = [x for x in lib if x["id"] != m["id"]] + [m]
        print(f"{m['id']:10s} (bổ sung tay) rows={len(m['hang'])}  {m['ten']}")


def deep(x):
    if isinstance(x, str): return clean(x)
    if isinstance(x, list): return [deep(i) for i in x]
    if isinstance(x, dict): return {k: (deep(v) if k not in ("id", "tu_khoa") else v) for k, v in x.items()}
    return x
lib = deep(lib)
json.dump(dict(version="1.0.0", ghi_chu="Thư viện nội dung giám sát chi tiết theo công tác – rút từ đề cương các Trung tâm; đã thay căn cứ NĐ 06/2021, NĐ 175/2024 bằng văn bản 2026.", hang_muc=lib),
          open(_os.path.join(DATA, "thu_vien_hang_muc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
