# -*- coding: utf-8 -*-
"""Bước 3: dựng các mục của mẫu Nâng cao. Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật TEXO."""
import json, re, sys
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
ROOT = _os.path.dirname(HERE)
SRC_DIR = _os.environ.get("DC_SRC") or _os.path.dirname(ROOT)   # thư mục chứa các đề cương nguồn (mặc định: thư mục cha của bộ công cụ)
BLOCKS = _os.path.join(HERE, "_blocks")
DATA = _os.path.join(ROOT, "core", "data")
B=BLOCKS+"/"
H=json.load(open(B+"TT09 De-cuong-TVGS_Harmonia_Bay-Da-Nang-17-10-2026-4b3388.json"))
T=json.load(open(B+"TT12 Mau de cuong co ban__De cuong TVGS - TT12 - Mau co ban.json"))
SN={
 "muc_tieu":(H,r"^1\. Mục tiêu, ý nghĩa của đề cương",r"^2\. Giới thiệu về dự án"),
 "du_lieu_dau_vao":(H,r"^4\. Hồ sơ và dữ liệu đầu vào",r"^B\. SƠ ĐỒ TỔ CHỨC"),
 "dieu_dong_dao_tao":(H,r"^3\. Kế hoạch điều động và đánh giá nhân sự",r"^C\. PHẠM VI CÔNG VIỆC"),
 "pham_vi_tvgs":(H,r"^C\. PHẠM VI CÔNG VIỆC VÀ CHỨC NĂNG",r"^1\. Trách nhiệm, phối hợp và chế độ làm việc"),
 "trach_nhiem_phoi_hop":(H,r"^1\. Trách nhiệm, phối hợp và chế độ làm việc",r"^3\. Quy trình đình chỉ khẩn cấp"),
 "dinh_chi":(H,r"^3\. Quy trình đình chỉ khẩn cấp",r"^4\. Ma trận trách nhiệm"),
 "ma_tran":(H,r"^4\. Ma trận trách nhiệm",r"^D\. CÔNG TÁC GIÁM SÁT VÀ QUẢN LÝ HỒ SƠ"),
 "quan_ly_ho_so":(H,r"^D\. CÔNG TÁC GIÁM SÁT VÀ QUẢN LÝ HỒ SƠ",r"^E\. CÔNG TÁC QUẢN LÝ CHẤT LƯỢNG"),
 "chuan_bi_thi_cong":(H,r"^1\.1\. Kiểm tra pháp lý dự án",r"^2\. Giai đoạn thi công"),
 "ke_hoach_nghiem_thu":(H,r"^2\.1\. Kế hoạch nghiệm thu",r"^2\.3\. Các quy trình nghiệm thu"),
 "quy_trinh_nghiem_thu":(H,r"^2\.3\. Các quy trình nghiệm thu tiêu biểu",r"^F\. CÔNG TÁC GIÁM SÁT TIẾN ĐỘ"),
 "tien_do":(H,r"^F\. CÔNG TÁC GIÁM SÁT TIẾN ĐỘ",r"^G\. CÔNG TÁC GIÁM SÁT KHỐI LƯỢNG"),
 "khoi_luong":(H,r"^G\. CÔNG TÁC GIÁM SÁT KHỐI LƯỢNG",r"^H\. CÔNG TÁC GIÁM SÁT ATLĐ"),
 "atld_rui_ro":(H,r"^H\. CÔNG TÁC GIÁM SÁT ATLĐ",r"^I\. CÔNG TÁC QUẢN LÝ THAY ĐỔI THIẾT KẾ"),
 "thay_doi_thiet_ke":(H,r"^I\. CÔNG TÁC QUẢN LÝ THAY ĐỔI THIẾT KẾ",r"^J\. CÔNG TÁC BÁO CÁO"),
 "bao_cao":(H,r"^J\. CÔNG TÁC BÁO CÁO",r"^K\. PHƯƠNG THỨC GIAO TIẾP"),
 "giao_tiep":(H,r"^K\. PHƯƠNG THỨC GIAO TIẾP",r"^PHẦN B"),
 "nghiem_thu_2026":(H,r"^B\. CÁC BƯỚC NGHIỆM THU CHẤT LƯỢNG",r"^C\. CÁC CÔNG TÁC GIÁM SÁT THI CÔNG THEO HẠNG MỤC"),
 "ke_hoach_an_toan":(H,r"^PHẦN C: KẾ HOẠCH QUẢN LÝ AN TOÀN",None),
 "tai_lieu_bat_buoc":(H,r"^3\. Các tài liệu bắt buộc của TVGS",r"^B\. CÁC BƯỚC NGHIỆM THU"),
}
REPL=[(r"Công ty [Cc]ổ phần [Đđ]ầu tư Blue Land","{CDT}"),(r"công ty Cổ phần đầu tư Blue Land","{CDT}"),(r"Blue ?Land","{CDT}"),
 (r"(dự án )?Tổ hợp [Tt]rung tâm thương mại và căn hộ Đà Nẵng\s*[–-]\s*Harmonia Bay","{DU_AN}"),(r"Harmonia Bay","{DU_AN}"),
 (r"Thời gian thực hiện dịch vụ theo Hợp đồng và Phụ lục 03 là 20 tháng\.","Thời gian thực hiện dịch vụ theo Hợp đồng là {THOI_GIAN} tháng."),
 (r"phân bổ nhân lực tại Bảng 4 – Lịch công tác cho từng vị trí","phân bổ nhân lực theo lịch công tác của hợp đồng cho từng vị trí"),
 (r"Căn cứ Điều 5 về nội dung, khối lượng công việc; Điều 10 về quyền và nghĩa vụ của TVGS,\s*","Căn cứ các điều khoản về nội dung, khối lượng công việc, quyền và nghĩa vụ của TVGS, "),
 (r"theo mục G\.1 và quy trình tại mục G\.3, Phần A","theo nguyên tắc và quy trình xác nhận khối lượng nêu trên"),
 (r"03 tầng hầm","các tầng hầm"),(r"semi top-down","theo biện pháp thi công tầng hầm được duyệt"),(r"biện pháp thi công\s*/\s*tầng hầm phải được\s*/?\s*thẩm tra\.?","Biện pháp thi công đặc biệt phải được thẩm tra theo quy định."),
 (r"cọc khoan nhồi, móng và tầng hầm","phần ngầm"),(r"BQLD\b","BQLDA"),(r"…{2,}|\.{4,}","…"),(r"theo nguyên tắc tại mục G\.1","theo nguyên tắc nêu trên"),(r"tại mục G\.\d+(, Phần A)?","nêu trên"),(r"\s+"," ")]
def clean(t):
    for a,b in REPL: t=re.sub(a,b,t)
    return t.strip()
def find(doc,rx,mi=250):
    r=re.compile(rx,re.I)
    for i,b in enumerate(doc):
        if i>=mi and b['k']=='p' and r.search(b['t'].strip()): return i
    raise SystemExit("not found "+rx)
out={}
for k,(doc,s_rx,e_rx) in SN.items():
    s=find(doc,s_rx); e=find(doc,e_rx,s+1) if e_rx else len(doc)
    items=[]
    for b in doc[s+1:e]:
        if b['k']=='p':
            t=clean(b['t'])
            if not t or re.fullmatch(r"(Diễn giải lưu đồ|Lưu đồ.*)",t): continue
            lv=b.get('lvl',0)
            sub = bool(re.match(r"^(\d+(\.\d+)*\.?|[a-g]\.)\s+\S",t) and len(t)<110) or (lv and len(t)<110)
            items.append(["h" if sub else ("b" if re.match(r"^[-•+]\s*",t) else "p"), re.sub(r"^[-•+]\s*","",t)])
        else:
            rows=[[clean(" ".join(c)) for c in r] for r in b['rows']]
            if rows: items.append(["t",rows])
    # ghép đoạn bị ngắt dòng (dòng bắt đầu bằng chữ thường)
    merged=[]
    for it in items:
        if merged and it[0] in ("p","h") and merged[-1][0] in ("p","h","b") and re.match(r"^[a-zàáảãạăâđèéẻẽẹêìíỉĩịòóỏõọôơùúủũụưỳýỷỹỵ]",it[1]):
            merged[-1][1]+=" "+it[1]; continue
        merged.append(it)
    # tách các mục a., b., c. bị dính vào cuối đoạn
    final=[]
    for it in merged:
        if it[0]=="t": final.append(it); continue
        if final and final[-1][0]!="t" and final[-1][1].endswith("NĐ-") :
            final[-1][1]+=it[1]; continue
        parts=re.split(r"(?<=[\.;:\)])\s+(?=[a-g]\.\s+[A-ZĐ])",it[1])
        final.append([it[0],parts[0]])
        for p in parts[1:]:
            m=re.match(r"^([a-g]\.\s+[^.:]{3,60}?)([\.:]\s+|$)(.*)$",p)
            if m and len(m.group(1))<70:
                final.append(["h",m.group(1).strip()])
                if m.group(3).strip(): final.append(["p",m.group(3).strip()])
            else:
                final.append(["p",p])
    out[k]=final
    print(k, len(merged))
json.dump(out,open(_os.path.join(DATA,'noi_dung_nang_cao.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
