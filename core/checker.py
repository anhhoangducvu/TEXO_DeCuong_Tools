# -*- coding: utf-8 -*-
"""Người xây dựng: Hoàng Đức Vũ – Trưởng phòng Kỹ thuật, Công ty CP TEXO Tư vấn và Đầu tư.
Kiểm tra đề cương TVGS theo khung chuẩn TEXO (rule-based, chạy không cần AI)."""
import datetime as dt
import json
import os
import re
import unicodedata

from . import extract as ex

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


def unaccent(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.replace("đ", "d").replace("Đ", "D").lower()


def _rx(p):
    return re.compile(unaccent(p), re.I | re.M)


MUC_DO = {"high": "Phải xử lý", "mid": "Nên xử lý", "ok": "Đạt", "info": "Lưu ý"}


def detect_date(blocks):
    """Ngày lập đề cương: dòng ngắn kiểu 'HÀ NỘI, 03/2025', 'Hà Nội, tháng 10 năm 2026', 'NĂM 2026' ở phần đầu."""
    cands = []
    for b in blocks[:150]:
        if b["k"] != "p" or len(b["t"]) > 70:
            continue
        t = b["t"]
        if re.search(r"(N[ĐD]|QH|TT|CP|BXD|/\d{4}/)", t):
            continue
        for mm in re.finditer(r"(?<![\d/])(\d{1,2})\s*/\s*(20\d{2})(?![\d/])", t):
            mo, yr = int(mm.group(1)), int(mm.group(2))
            if 1 <= mo <= 12:
                cands.append(dt.date(yr, mo, 1))
        for mm in re.finditer(r"th[aá]ng\s*(\d{1,2})\s*n[aă]m\s*(20\d{2})", t, re.I):
            mo, yr = int(mm.group(1)), int(mm.group(2))
            if 1 <= mo <= 12:
                cands.append(dt.date(yr, mo, 1))
        mm = re.fullmatch(r".{0,30}N[ĂA]M\s*(20\d{2})\s*", t.upper())
        if mm:
            cands.append(dt.date(int(mm.group(1)), 1, 1))
    return max(cands) if cands else None


def _cover_info(blocks):
    first = []
    for b in blocks[:60]:
        if b["k"] == "p":
            first.append(b["t"])
        else:
            for r in b["rows"]:
                first.append(" ".join(" ".join(c) for c in r))
    txt = unaccent("\n".join(first))
    fields = {"Dự án": r"d[uự] [aá]n", "Công trình/Gói thầu": r"(c[oô]ng tr[iì]nh|g[oó]i th[aầ]u)",
              "Địa điểm": r"[dđ][iị]a [dđ]i[eể]m", "Chủ đầu tư": r"ch[uủ] [dđ][aầ]u t[uư]",
              "Đơn vị TVGS": r"(t[uư] v[aấ]n gi[aá]m s[aá]t|texo)"}
    have = [k for k, p in fields.items() if _rx(p).search(txt)]
    return have, [k for k in fields if k not in have]


def _values(blocks, label_rx):
    vals = []
    rx = re.compile(r"^\s*(?:\d+[\.\)]\s*)?(?:" + label_rx + r")\s*[:：]\s*(.{4,160})$", re.I)
    for b in blocks[:400]:
        if b["k"] == "p":
            lines = [b["t"]]
        else:
            lines = []
            for r in b["rows"]:
                cells = [" ".join(c).strip() for c in r]
                cells = [c for c in cells if c and c not in (":", "：")]
                if len(cells) >= 2:
                    lines.append(cells[0] + ": " + cells[-1])
        for ln in lines:
            m = rx.match(ln.replace("|", ":"))
            if m:
                v = re.sub(r"\s+", " ", m.group(1)).strip(" .;:")
                vn = unaccent(v)
                if v and 4 <= len(v) <= 120 and not re.search(r"texo|chu ky|ten,|giam sat truong|tong giam doc|dai dien|xac nhan", vn) \
                        and not re.fullmatch(r"(don vi )?(tu van giam sat|chu dau tu|nha thau.*|tu van thiet ke)", vn.strip()):
                    vals.append(v)
    return vals


def _norm_name(v):
    v = unaccent(v)
    v = re.sub(r"[^a-z0-9 ]", " ", v)
    return re.sub(r"\s+", " ", v).strip()


def check(blocks, meta, opts=None):
    opts = opts or {}
    K = load("khung_tieuchi.json")
    LIB = load("thu_vien_hang_muc.json")["hang_muc"]
    PL = load("phap_ly.json")

    heads = [b["t"] for b in blocks if b["k"] == "p" and (b.get("lvl", 0) > 0 or b.get("toc"))]
    heads_n = [unaccent(h) for h in heads]
    body = ex.full_text(blocks)
    body_n = unaccent(body)
    words = len(body.split())

    # --- mức mẫu
    n_found = 0
    n_total = 0
    for c in K["tieu_chi"]:
        if c["cap"] == "N" and c.get("pat"):
            n_total += 1
            if any(_rx(p).search(h) for p in c["pat"] for h in heads_n):
                n_found += 1
    auto_level = "Nâng cao" if (n_total and n_found / n_total >= 0.5) or words > 60000 else "Cơ bản"
    level = opts.get("muc_mau") or auto_level

    # --- ngày đề cương
    ngay = opts.get("ngay") or detect_date(blocks)
    moc = dt.date.fromisoformat(PL["moc_hieu_luc"])
    # Đề cương không ghi ngày hoặc đã viện dẫn văn bản 2026 → coi như lập sau mốc hiệu lực (áp dụng nghiêm)
    co_vb_2026 = bool(re.search(r"(135/2025/QH15|207/2026/N[ĐD]-CP|217/2026/N[ĐD]-CP|212/2026/N[ĐD]-CP)", ex.full_text(blocks)))
    sau_moc = (ngay is None and dt.date.today() >= moc) or bool(ngay and ngay >= moc) or co_vb_2026 or opts.get("ap_dung_2026", False)

    # --- tiêu chí khung
    res = []
    for c in K["tieu_chi"]:
        r = dict(id=c["id"], nhom=c["nhom"], ten=c["ten"], cap=c["cap"], bang_chung="", trang_thai="Thiếu")
        rule = c.get("rule")
        if rule == "cover":
            have, miss = _cover_info(blocks)
            r["trang_thai"] = "Đạt" if len(miss) == 0 else ("Có, chưa đủ" if len(have) >= 3 else "Thiếu")
            r["bang_chung"] = "Có: " + ", ".join(have) + (("; thiếu: " + ", ".join(miss)) if miss else "")
        elif rule == "approval":
            first = unaccent(ex.full_text(blocks[:80]))
            ok = (bool(re.search(r"phe duyet", first)) and bool(re.search(r"chu dau tu", first)) and bool(re.search(r"(dai dien )?tu van giam sat|texo", first))) \
                or bool(re.search(r"chu dau tu\s{0,40}(dai dien )?(don vi )?tu van giam sat", first))
            r["trang_thai"] = "Đạt" if ok else "Thiếu"
            r["bang_chung"] = "Có ô ký CĐT phê duyệt / TVGS" if ok else "Chưa thấy trang phê duyệt ở phần đầu"
        elif rule == "a4":
            pg = meta.get("page")
            ok = (pg is None) or (abs(pg[0] - 21.0) < 0.6 and abs(pg[1] - 29.7) < 0.6) or (abs(pg[1] - 21.0) < 0.6 and abs(pg[0] - 29.7) < 0.6)
            r["trang_thai"] = "Đạt" if ok else "Thiếu"
            r["bang_chung"] = f"Khổ {pg[0]} × {pg[1]} cm" if pg else "PDF – không kiểm khổ"
        elif rule == "noi_bo":
            hits = re.findall(r"(Trung t[âa]m\s+(?:T[ưu] v[ấa]n\s+)?(?:s[ốo]\s+)?\d{1,2}\b|TRUNG T[ÂA]M\s+(?:T[ƯU] V[ẤA]N\s+)?\d{1,2}\b|V[ăa]n ph[òo]ng đi[ệe]n t[ửu]|VPĐT)", body)
            r["trang_thai"] = "Đạt" if not hits else "Có, chưa đủ"
            r["bang_chung"] = "Không nêu đơn vị nội bộ" if not hits else f"Nêu {len(hits)} lần: " + ", ".join(sorted(set(hits))[:5]) + " – xóa trước khi gửi Chủ đầu tư"
        elif rule == "std_count":
            n = len(re.findall(r"\b(TCVN|QCVN|TCXDVN|TCXD)\s*[\d]", body))
            r["trang_thai"] = "Đạt" if n >= 10 else ("Có, chưa đủ" if n >= 3 else "Thiếu")
            r["bang_chung"] = f"{n} lượt viện dẫn TCVN/QCVN"
        else:
            hit = None
            for p in c["pat"]:
                rx = _rx(p)
                for h, hn in zip(heads, heads_n):
                    if rx.search(hn):
                        hit = h
                        break
                if hit:
                    break
            if hit:
                r["trang_thai"] = "Đạt"
                r["bang_chung"] = "Mục: " + hit[:120]
            else:
                cnt = sum(len(_rx(p).findall(body_n)) for p in c["pat"])
                if cnt:
                    r["trang_thai"] = "Có, chưa thành mục"
                    r["bang_chung"] = f"Nhắc {cnt} lần trong thân bài, chưa có tiêu đề riêng"
        # mức độ
        if r["trang_thai"] == "Đạt":
            r["muc_do"] = "ok"
        elif c["cap"] == "B":
            r["muc_do"] = "high" if r["trang_thai"] == "Thiếu" else "mid"
        else:
            r["muc_do"] = ("mid" if r["trang_thai"] == "Thiếu" else "info") if level == "Nâng cao" else "info"
        res.append(r)

    # --- điểm
    def wt(c):
        return 2 if c["cap"] == "B" else (1 if level == "Nâng cao" else 0)
    earned = maxp = 0.0
    for r in res:
        w = wt(r)
        maxp += w
        earned += w * (1 if r["trang_thai"] == "Đạt" else 0.5 if r["trang_thai"].startswith("Có") else 0)
    bonus = 0
    if level == "Cơ bản":
        bonus = sum(1 for r in res if r["cap"] == "N" and r["trang_thai"] == "Đạt")
    diem = round(100 * earned / maxp) if maxp else 0

    # --- hạng mục công tác
    desc_end = 0
    for i, b in enumerate(blocks):
        if b["k"] == "p" and b.get("lvl", 0) > 0 and re.search(r"giam sat chat luong|co so thuc hien", unaccent(b["t"])) and i > 15:
            desc_end = i
            break
    desc_n = unaccent(ex.full_text(blocks[:desc_end or min(len(blocks), 150)]))
    expected = set(opts.get("hang_muc") or [])
    hm = []
    for m in LIB:
        kws = [_rx(k) for k in m["tu_khoa"]]
        in_head = next((h for h, hn in zip(heads, heads_n) if any(k.search(hn) for k in kws) and re.search(r"giam sat|kiem tra|thi cong|lap dat|cong tac|nghiem thu", hn)), None)
        body_hits = sum(len(k.findall(body_n)) for k in kws)
        in_desc = any(k.search(desc_n) for k in kws)
        if in_head:
            st = "Có mục giám sát chi tiết"
        elif body_hits >= 3:
            st = "Có nhắc, chưa thành mục chi tiết"
        else:
            st = "Không có"
        need = m["id"] in expected or (not expected and in_desc and m["nhom"] not in ("Chung",) and m["id"] not in ("TRACDAC", "KHOANKS"))
        if st == "Không có" and not need:
            continue
        if need and st != "Có mục giám sát chi tiết":
            md = "high" if st == "Không có" else "mid"
        elif st == "Có mục giám sát chi tiết":
            md = "ok"
        else:
            md = "info"
        hm.append(dict(id=m["id"], ten=m["ten"], nhom=m["nhom"], trang_thai=st, can_co=need,
                       bang_chung=(in_head or "")[:110], muc_do=md))

    # --- pháp lý
    het, ra_soat = [], []
    for x in PL["het_hieu_luc"]:
        n = len(re.findall(x["pat"], body, re.I))
        if n:
            het.append(dict(ten=x["ten"], so_lan=n, thay_the=x["thay_the"],
                            muc_do="high" if sau_moc else "mid"))
    for x in PL["can_ra_soat"]:
        n = len(re.findall(x["pat"], body, re.I))
        if n:
            ra_soat.append(dict(ten=x["ten"], so_lan=n, ly_do=x["ly_do"], muc_do="info"))
    co_moi = {k: bool(re.search(p, body)) for k, p in
              {"Luật XD 135/2025": r"135/2025/QH15", "NĐ 207/2026": r"207/2026/N[ĐD]-CP",
               "TT 32/2026": r"32/2026/TT-BXD", "NĐ 217/2026 / 212/2026": r"(217|212)/2026/N[ĐD]-CP"}.items()}

    # --- chất lượng nội dung
    ph_rx = re.compile(r"(…{2,}|\.{5,}|\b[xX]{3,}\b|(?<![=<])<(?!=)\s*[A-Za-zÀ-ỹĐđ][^<>\n=]{0,38}>|\[\s*\.*\s*\]|ng[aà]y\s+/\s+/|ng[aà]y\s*…|\?\?+)")
    placeholders = []
    bm = len(blocks)
    for i, b in enumerate(blocks):
        if i > len(blocks) * 0.4 and b["k"] == "p" and re.search(r"^(PH[ẦA]N\s+\S+\s*[:.\-–]?\s*)?(BI[ỂE]U M[ẪA]U|PH[ỤU] L[ỤU]C|M[ẪA]U\s*(S[ỐO]\s*)?\d+\b)", b["t"].strip(), re.I):
            bm = i
            break
    for b in blocks[:bm]:
        if b.get("toc") or (b["k"] == "p" and re.search(r"(…|\.){3,}\s*\d{1,3}\s*$", b["t"])):
            continue
        t = b["t"] if b["k"] == "p" else " ".join(" ".join(c) for r in b["rows"] for c in r)
        for m in ph_rx.finditer(t):
            s = max(0, m.start() - 40)
            ctx = t[s:m.end() + 30].strip()
            # bỏ qua ô trống trong biểu mẫu biên bản (họ tên, chức vụ, ngày tháng) – đó là mẫu để điền khi dùng
            if re.search(r"(Ông|Bà|Chức vụ|ng[aà]y|th[aá]ng|n[aă]m|Đại diện|Số\s*:|Họ (và )?tên|Ký|Thời gian|Địa điểm|Lúc|giờ|BIÊN BẢN|Kính gửi|Tại\s*:)", ctx, re.I):
                continue
            placeholders.append(ctx)
    du_an = _values(blocks, r"d[ựu] [áa]n|t[êe]n d[ựu] [áa]n")
    cdt = _values(blocks, r"ch[ủu] [đd][ầa]u t[ưu]")
    def distinct(vals):
        out, seen = [], set()
        for v in vals:
            k = _norm_name(v)[:40]
            if k and k not in seen:
                seen.add(k)
                out.append(v)
        return out
    du_an_d, cdt_d = distinct(du_an), distinct(cdt)
    lan_ten = []
    if opts.get("ten_du_an"):
        key = _norm_name(opts["ten_du_an"])[:25]
        lan_ten += [v for v in du_an_d if key and key not in _norm_name(v)]
    elif len(du_an_d) > 1:
        lan_ten += du_an_d[1:]
    if opts.get("chu_dau_tu"):
        key = _norm_name(opts["chu_dau_tu"])[:20]
        lan_ten += [v for v in cdt_d if key and key not in _norm_name(v)]
    elif len(cdt_d) > 1:
        lan_ten += cdt_d[1:]

    chat_luong = dict(so_tu=words, so_bang=sum(1 for b in blocks if b["k"] == "t"), so_hinh=meta.get("images", 0),
                      so_tieu_de=len(heads), cho_trong=placeholders[:30], so_cho_trong=len(placeholders),
                      ten_du_an=du_an_d[:6], chu_dau_tu=cdt_d[:6], nghi_lan_ten=lan_ten[:8])

    # --- tổng hợp
    thieu_B = [r for r in res if r["cap"] == "B" and r["trang_thai"] == "Thiếu"]
    hm_thieu = [h for h in hm if h["muc_do"] == "high"]
    n_high = len(thieu_B) + len(hm_thieu) + sum(1 for h in het if h["muc_do"] == "high") + (1 if lan_ten else 0)
    if diem >= 85 and n_high == 0:
        ket_luan, mau = "Đạt – có thể trình ký", "green"
    elif diem >= 65:
        ket_luan, mau = "Cần chỉnh sửa, bổ sung trước khi trình ký", "orange"
    else:
        ket_luan, mau = "Chưa đạt – cần lập lại theo khung chuẩn", "red"

    from . import version as _v
    _vi = _v.info()
    return dict(phien_ban=_vi["phien_ban"], pl_ngay=_vi["phap_ly_ngay"], muc_mau=level, muc_mau_tu_nhan=auto_level, ngay=ngay.isoformat() if ngay else None, sau_moc=sau_moc,
                diem=diem, diem_cong=bonus, ket_luan=ket_luan, mau=mau, so_viec_phai_xu_ly=n_high,
                tieu_chi=res, nhom=K["nhom"], hang_muc=hm, phap_ly=dict(het=het, ra_soat=ra_soat, co_moi=co_moi),
                chat_luong=chat_luong, meta={k: v for k, v in meta.items() if k != "files"}, files=meta.get("files", []))


def check_files(files, opts=None):
    blocks, meta = ex.read_any(files)
    return check(blocks, meta, opts)
