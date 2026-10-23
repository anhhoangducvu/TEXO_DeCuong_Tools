# -*- coding: utf-8 -*-
"""Giao diện dùng chung cho 2 app Streamlit: màn hình đăng nhập gọn, thanh bên (người ký kiểm, AI), CSS."""
import base64
import hmac
import json
import os

import streamlit as st

from . import llm
from . import version as V

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOGO = os.path.join(HERE, "assets", "logo_texo.png")
SECRETS = os.path.join(ROOT, ".secrets_ai.json")
CSS = """
<style>
.block-container {padding-top: 3.6rem !important; max-width: 1250px;}
.texo-head {display:flex; align-items:center; gap:16px; border-bottom:3px solid #2E5496; padding-bottom:8px; margin-bottom:14px;}
.texo-head img {height:42px;}
.texo-head .t1 {font-size:1.45rem; font-weight:700; color:#0C0150; line-height:1.2;}
.texo-head .t2 {font-size:.9rem; color:#595959;}
.kpi {border-top:4px solid #2E5496; background:#EAF0F7; padding:10px 12px; border-radius:4px; text-align:center;}
.kpi .v {font-size:1.9rem; font-weight:700;} .kpi .l {font-weight:600; color:#1F3864;} .kpi .s {font-size:.8rem; color:#595959;}
.ket-luan {border-left:6px solid; padding:10px 14px; border-radius:4px; margin:8px 0 14px 0;}
</style>
"""
COLORS = {"red": ("#C00000", "#FDE4E1"), "orange": ("#C45911", "#FFF1DE"), "green": ("#2E7D32", "#E4F3E6"), "blue": ("#2E5496", "#EAF0F7")}


def _password():
    try:
        return st.secrets.get("APP_PASSWORD", None) or os.environ.get("APP_PASSWORD", "texo2026")
    except Exception:
        return os.environ.get("APP_PASSWORD", "texo2026")


def setup(title, icon="📘"):
    st.set_page_config(page_title=title, page_icon=icon, layout="wide",
                       initial_sidebar_state="expanded" if st.session_state.get("_ok") else "collapsed")


def gate(title):
    """Màn hình đăng nhập đơn giản: logo, tên app, mật khẩu. Chưa đăng nhập thì không hiện thanh bên."""
    if st.session_state.get("_ok"):
        return True
    st.markdown("<style>.block-container{padding-top:4rem !important;}</style>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if os.path.exists(LOGO):
            st.image(LOGO, width=170)
        st.markdown(f"## {title}")
        st.caption("Phòng Kỹ thuật · Công ty CP TEXO Tư vấn và Đầu tư")
        with st.form("login"):
            pw = st.text_input("Mật khẩu", type="password")
            try:
                ok = st.form_submit_button("Đăng nhập", type="primary", width="stretch")
            except TypeError:
                ok = st.form_submit_button("Đăng nhập", type="primary", use_container_width=True)
            if ok:
                if hmac.compare_digest(pw, _password()):
                    st.session_state["_ok"] = True
                    st.rerun()
                else:
                    st.error("Mật khẩu chưa đúng.")
    st.stop()


def header(title, subtitle):
    st.markdown(CSS, unsafe_allow_html=True)
    logo = ""
    if os.path.exists(LOGO):
        logo = f'<img src="data:image/png;base64,{base64.b64encode(open(LOGO, "rb").read()).decode()}"/>'
    st.markdown(f'<div class="texo-head">{logo}<div><div class="t1">{title}</div><div class="t2">{subtitle}</div></div></div>',
                unsafe_allow_html=True)


# --------------------------------------------------------------------------- thanh bên
def _load_saved():
    try:
        return json.load(open(SECRETS, encoding="utf-8"))
    except Exception:
        return {}


def sidebar(kiem_tra=True):
    """Thanh bên sau đăng nhập: người ký kiểm + cấu hình AI. Trả dict cấu hình."""
    vi = V.info()
    out = {}
    with st.sidebar:
        st.markdown("### ✍️ Người ký kiểm")
        if kiem_tra:
            out["nguoi_kiem_tra"] = st.text_input("Người kiểm tra", key="nguoi_kiem_tra")
            out["chuc_danh_duyet"] = st.text_input("Chức danh người duyệt", "Trưởng phòng Kỹ thuật", key="cd_duyet")
            out["nguoi_duyet"] = st.text_input("Người duyệt", "Hoàng Đức Vũ", key="nguoi_duyet")
        else:
            out["nguoi_ky_tvgs"] = st.text_input("Đại diện TVGS ký tờ lót", key="nguoi_ky_tvgs",
                                                 help="In ở ô ký 'Đại diện Tư vấn giám sát' trên tờ lót. Để trống nếu ký tay.")
            out["nguoi_lap"] = st.text_input("Người lập (nội bộ, không in)", key="nguoi_lap")

        st.markdown("### 🤖 Trợ lý AI (tùy chọn)")
        saved = _load_saved()
        names = {k: v["label"] for k, v in llm.PROVIDERS.items()}
        keys = list(names)
        pv = st.selectbox("Nhà cung cấp", ["(Không dùng AI)"] + keys,
                          index=(keys.index(saved["provider"]) + 1) if saved.get("provider") in keys else 0,
                          format_func=lambda k: names.get(k, k))
        if pv == "(Không dùng AI)":
            st.caption("Đang chạy bằng bộ quy tắc – miễn phí, dữ liệu không rời máy.")
            out["ai"] = None
        else:
            key = st.text_input("API key", saved.get("key", "") if saved.get("provider") == pv else "", type="password")
            base = ""
            if llm.PROVIDERS[pv]["needs_base_url"]:
                base = st.text_input("Base URL", saved.get("base_url", ""), placeholder="https://openrouter.ai/api/v1")
            mk = f"_models_{pv}"
            if st.button("Lấy danh sách model", disabled=not key):
                ok, res = llm.list_models(pv, key, base or None)
                if ok:
                    st.session_state[mk] = res
                else:
                    st.error(res)
            models = st.session_state.get(mk) or ([saved["model"]] if saved.get("provider") == pv and saved.get("model") else [])
            model = None
            if models:
                pref = next((i for i, m in enumerate(models) if any(t in m for t in ("sonnet", "gpt-4o", "flash-latest", "flash"))), 0)
                if saved.get("model") in models:
                    pref = models.index(saved["model"])
                model = st.selectbox("Model", models, index=pref)
                if st.button("Kiểm tra kết nối"):
                    ok, msg = llm.test_connection(pv, model, key, base or None)
                    (st.success if ok else st.error)(("Kết nối được: " if ok else "") + msg)
            st.caption(llm.PROVIDERS[pv]["note"])
            luu = st.checkbox("Lưu key trên máy này", value=bool(saved.get("key")))
            if luu and key and model:
                if saved != {"provider": pv, "key": key, "model": model, "base_url": base}:
                    json.dump({"provider": pv, "key": key, "model": model, "base_url": base}, open(SECRETS, "w", encoding="utf-8"))
            elif not luu and os.path.exists(SECRETS):
                os.remove(SECRETS)
            st.caption("⚠️ Bật AI thì nội dung tài liệu được gửi tới nhà cung cấp đã chọn. Chỉ lưu key trên máy cá nhân.")
            out["ai"] = {"provider": pv, "key": key, "model": model, "base_url": base} if key and model else None
            if not out["ai"]:
                st.info("Nhập key và chọn model để bật AI.")
        st.divider()
        st.caption("⚖️ Rà soát văn bản pháp luật, tiêu chuẩn bằng TEXO Legal Reviewer trước khi trình ký.")
        st.caption(f"Dữ liệu v{vi['phien_ban']} · pháp lý cập nhật {vi['phap_ly_ngay']} · Xây dựng: Hoàng Đức Vũ")
    return out


def kpi(col, value, label, sub="", color="blue"):
    fg, bg = COLORS.get(color, COLORS["blue"])
    col.markdown(f'<div class="kpi" style="border-top-color:{fg}; background:{bg}"><div class="v" style="color:{fg}">{value}</div>'
                 f'<div class="l">{label}</div><div class="s">{sub}</div></div>', unsafe_allow_html=True)


def callout(text, color="blue"):
    fg, bg = COLORS.get(color, COLORS["blue"])
    st.markdown(f'<div class="ket-luan" style="border-color:{fg}; background:{bg}">{text}</div>', unsafe_allow_html=True)
