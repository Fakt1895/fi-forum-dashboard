"""
FI-Forum 2026 · Social Listening Dashboard
"""

from datetime import datetime, timezone, date
from html import escape
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from demo_data import get_demo_data, VERIFIED_AT

TZ = ZoneInfo("Europe/Berlin")
EVENT_START = date(2026, 11, 3)

RED = "#E30613"
RED_DARK = "#B00510"
INK = "#1A1A1A"
MUTED = "#6B6F76"
LINE = "#E8E8EA"
BG = "#F6F6F7"
POS = "#1F9D55"
NEU = "#9AA0A6"
NEG = "#E30613"

st.set_page_config(
    page_title="FI-Forum 2026 · Social Listening",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: {BG}; }}
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none; }}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1280px; }}

.hero {{
  background: linear-gradient(120deg, {RED} 0%, {RED_DARK} 100%);
  border-radius: 18px; padding: 28px 32px; color: #fff;
  display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; flex-wrap: wrap;
  box-shadow: 0 10px 30px rgba(227,6,19,.18);
}}
.hero .eyebrow {{ font-size: 12px; letter-spacing: .14em; text-transform: uppercase; opacity: .85; font-weight: 600; }}
.hero h1 {{ font-size: 34px; font-weight: 800; margin: 6px 0 6px; line-height: 1.1; color: #fff; }}
.hero .sub {{ font-size: 15px; opacity: .92; }}
.hero .right {{ text-align: right; }}
.badge-live {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,.16);
  padding: 6px 12px; border-radius: 999px; font-size: 13px; font-weight: 600; }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; background: #7CFFB2; box-shadow: 0 0 0 4px rgba(124,255,178,.25); }}
.countdown {{ font-size: 42px; font-weight: 800; line-height: 1; margin-top: 10px; }}
.countdown small {{ font-size: 14px; font-weight: 500; opacity: .9; }}

.kpis {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin: 18px 0 8px; }}
@media (max-width: 900px) {{ .kpis {{ grid-template-columns: repeat(2, 1fr); }} .hero .right {{ text-align: left; }} }}
.kpi {{ background: #fff; border: 1px solid {LINE}; border-radius: 14px; padding: 16px 18px; }}
.kpi .label {{ font-size: 12px; color: {MUTED}; font-weight: 600; text-transform: uppercase; letter-spacing: .06em; }}
.kpi .value {{ font-size: 30px; font-weight: 800; color: {INK}; margin-top: 6px; }}
.kpi .hint {{ font-size: 12px; color: {MUTED}; margin-top: 2px; }}

.card {{ background: #fff; border: 1px solid {LINE}; border-radius: 14px; padding: 18px 20px; height: 100%; }}
.card h3 {{ font-size: 15px; font-weight: 700; color: {INK}; margin: 0 0 4px; }}
.card .cap {{ font-size: 12px; color: {MUTED}; margin-bottom: 6px; }}

.chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }}
.chip {{ background: #FDECEE; color: {RED_DARK}; border-radius: 999px; padding: 6px 12px; font-size: 13px; font-weight: 600; }}
.chip span {{ opacity: .6; margin-left: 4px; }}

.alert-ok {{ background: #EAF7EF; border: 1px solid #BFE6CD; color: #145C33; border-radius: 12px; padding: 12px 16px; font-size: 14px; font-weight: 500; }}
.alert-bad {{ background: #FDECEE; border: 1px solid #F6B8BE; color: {RED_DARK}; border-radius: 12px; padding: 12px 16px; font-size: 14px; font-weight: 600; }}

.section {{ font-size: 20px; font-weight: 800; color: {INK}; margin: 28px 0 10px; }}

.post {{ background: #fff; border: 1px solid {LINE}; border-radius: 14px; padding: 18px 20px; margin-bottom: 12px;
  border-left: 4px solid var(--accent); }}
.post .top {{ display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }}
.post .who {{ font-weight: 700; color: {INK}; font-size: 15px; }}
.post .role {{ color: {MUTED}; font-size: 13px; margin-top: 1px; }}
.post .when {{ color: {MUTED}; font-size: 12px; white-space: nowrap; }}
.post .txt {{ color: #2B2B2B; font-size: 14.5px; line-height: 1.55; margin: 12px 0 12px; }}
.post .meta {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
.pill {{ border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 600; }}
.pill.src {{ background: #EEF3FB; color: #0A66C2; }}
.pill.cat {{ background: #F1F1F3; color: #44474D; }}
.pill.sent {{ color: #fff; background: var(--accent); }}
.stat {{ color: {MUTED}; font-size: 13px; margin-left: 4px; }}
.open {{ margin-left: auto; font-size: 13px; font-weight: 700; color: {RED} !important; text-decoration: none; }}
.open:hover {{ text-decoration: underline; }}

.foot {{ text-align: center; color: {MUTED}; font-size: 12px; margin-top: 28px; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ background:#fff; border:1px solid {LINE} !important; border-radius:14px; }}
h3.ct {{ font-size: 15px !important; font-weight: 700 !important; color: {INK}; margin: 0 !important; padding: 0 !important; }}
.cap {{ font-size: 12px; color: {MUTED}; margin-bottom: 4px; }}
</style>
""", unsafe_allow_html=True)


def fmt_dt(ts: pd.Timestamp) -> str:
    return ts.tz_convert(TZ).strftime("%d.%m.%Y · %H:%M Uhr")


def rel_time(ts: pd.Timestamp) -> str:
    delta = datetime.now(timezone.utc) - ts.to_pydatetime()
    h = int(delta.total_seconds() // 3600)
    if h < 1:
        return "vor wenigen Minuten"
    if h < 24:
        return f"vor {h} Std."
    d = h // 24
    return "vor 1 Tag" if d == 1 else f"vor {d} Tagen"


def plot_base(fig, height=260):
    fig.update_layout(
        height=height, margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, sans-serif", color=INK, size=12),
        showlegend=False,
    )
    return fig


df, summary = get_demo_data()
df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
df = df.sort_values("created_at", ascending=False).reset_index(drop=True)

n = len(df)
reactions = int(df["likes"].sum())
comments = int(df["comments"].sum())
pos_share = round(100 * (df["sentiment"] == "positive").mean()) if n else 0
critical = int(df["severity"].isin(["warning", "critical"]).sum())
authors = df["author"].nunique()
days_left = (EVENT_START - datetime.now(TZ).date()).days
verified = pd.Timestamp(VERIFIED_AT)

# ---------- Hero ----------
if days_left > 0:
    countdown = f'{days_left}<small> Tage bis Eventstart</small>'
elif days_left > -3:
    countdown = 'LIVE<small> · Event läuft</small>'
else:
    countdown = 'Rückblick<small> · Event beendet</small>'

st.markdown(f"""
<div class="hero">
  <div>
    <div class="eyebrow">Social Listening · Sparkassen-Finanzgruppe</div>
    <h1>FI-Forum 2026</h1>
    <div class="sub">3.–5. November 2026 · Messe Frankfurt</div>
  </div>
  <div class="right">
    <div class="badge-live"><span class="dot"></span>Zuletzt geprüft: {fmt_dt(verified)}</div>
    <div class="countdown">{countdown}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- KPIs ----------
st.markdown(f"""
<div class="kpis">
  <div class="kpi"><div class="label">Beiträge</div><div class="value">{n}</div><div class="hint">verifiziert, mit Link</div></div>
  <div class="kpi"><div class="label">Reaktionen</div><div class="value">{reactions:,}</div><div class="hint">Summe aller Beiträge</div></div>
  <div class="kpi"><div class="label">Kommentare</div><div class="value">{comments}</div><div class="hint">Summe aller Beiträge</div></div>
  <div class="kpi"><div class="label">Stimmung positiv</div><div class="value" style="color:{POS}">{pos_share}%</div><div class="hint">Anteil der Beiträge</div></div>
  <div class="kpi"><div class="label">Kritische Hinweise</div><div class="value" style="color:{NEG if critical else INK}">{critical}</div><div class="hint">{authors} verschiedene Absender</div></div>
</div>
""".replace(",", "."), unsafe_allow_html=True)

if critical:
    st.markdown(f'<div class="alert-bad">⚠ {critical} Beitrag/Beiträge mit Kritik oder Problemen – bitte unten prüfen.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="alert-ok">✓ Keine kritischen Beiträge. Die Resonanz ist durchweg positiv.</div>', unsafe_allow_html=True)

# ---------- Charts ----------
st.markdown('<div class="section">Überblick</div>', unsafe_allow_html=True)
cfg = {"displayModeBar": False}
c1, c2, c3 = st.columns([1.5, 1, 1.2], gap="medium")

with c1.container(border=True):
    st.markdown('<h3 class="ct">Beiträge pro Tag</h3><div class="cap">nach Veröffentlichungsdatum</div>', unsafe_allow_html=True)
    per_day = df.assign(day=df["created_at"].dt.tz_convert(TZ).dt.date).groupby("day").agg(
        posts=("id", "count"), reac=("likes", "sum")).reset_index()
    full = pd.DataFrame({"day": pd.date_range(per_day["day"].min(), max(per_day["day"].max(), datetime.now(TZ).date())).date})
    per_day = full.merge(per_day, on="day", how="left").fillna(0)
    fig = go.Figure(go.Bar(
        x=[d.strftime("%d.%m.") for d in per_day["day"]], y=per_day["posts"],
        marker_color=RED, marker_line_width=0,
        hovertemplate="%{x}: %{y} Beiträge<extra></extra>"))
    fig.update_yaxes(gridcolor=LINE, dtick=1, zeroline=False)
    fig.update_xaxes(showgrid=False, tickangle=0, nticks=8)
    st.plotly_chart(plot_base(fig), use_container_width=True, config=cfg)

with c2.container(border=True):
    st.markdown('<h3 class="ct">Stimmung</h3><div class="cap">Einordnung je Beitrag</div>', unsafe_allow_html=True)
    s = df["sentiment"].value_counts()
    vals = [int(s.get("positive", 0)), int(s.get("neutral", 0)), int(s.get("negative", 0))]
    fig = go.Figure(go.Pie(
        labels=["Positiv", "Neutral", "Negativ"], values=vals, hole=.68,
        marker=dict(colors=[POS, NEU, NEG], line=dict(color="#fff", width=2)),
        textinfo="none", sort=False, hovertemplate="%{label}: %{value}<extra></extra>"))
    fig.add_annotation(text=f"<b>{pos_share}%</b><br><span style='font-size:12px;color:{MUTED}'>positiv</span>",
                       showarrow=False, font=dict(size=26, color=INK))
    st.plotly_chart(plot_base(fig), use_container_width=True, config=cfg)

with c3.container(border=True):
    st.markdown('<h3 class="ct">Reichweite nach Absender</h3><div class="cap">Reaktionen je Absender</div>', unsafe_allow_html=True)
    by_author = df.groupby("author")["likes"].sum().sort_values().tail(8)
    fig = go.Figure(go.Bar(
        x=by_author.values, y=by_author.index, orientation="h",
        marker_color=[RED if v == by_author.max() else "#F3A0A6" for v in by_author.values],
        text=by_author.values, textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: %{x} Reaktionen<extra></extra>"))
    fig.update_xaxes(visible=False, range=[0, by_author.max()*1.25])
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(plot_base(fig), use_container_width=True, config=cfg)

# ---------- Themes & categories ----------
t1, t2 = st.columns([1.4, 1], gap="medium")
with t1:
    theme_counts = pd.Series([t for ts in df["themes"] for t in ts]).value_counts().head(12)
    chips = "".join(f'<div class="chip">{escape(t)}<span>{c}</span></div>' for t, c in theme_counts.items())
    st.markdown(f'<div class="card"><h3>Top-Themen</h3><div class="cap">Wie oft ein Thema in den Beiträgen vorkommt</div><div class="chips">{chips}</div></div>', unsafe_allow_html=True)
with t2:
    cats = df["category"].value_counts()
    rows = "".join(
        f'<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid {LINE};font-size:14px">'
        f'<span>{escape(k)}</span><b>{v}</b></div>' for k, v in cats.items())
    st.markdown(f'<div class="card"><h3>Wer spricht über das FI-Forum?</h3><div class="cap">nach Art des Beitrags</div>{rows}</div>', unsafe_allow_html=True)

# ---------- Feed ----------
st.markdown('<div class="section">Alle Beiträge</div>', unsafe_allow_html=True)
f1, f2, f3 = st.columns([1, 1, 1])
with f1:
    sent_map = {"Alle": None, "Positiv": "positive", "Neutral": "neutral", "Negativ": "negative"}
    sent_sel = st.selectbox("Stimmung", list(sent_map.keys()))
with f2:
    cat_sel = st.selectbox("Art des Beitrags", ["Alle"] + sorted(df["category"].unique().tolist()))
with f3:
    sort_sel = st.selectbox("Sortierung", ["Neueste zuerst", "Meiste Reaktionen"])

view = df.copy()
if sent_map[sent_sel]:
    view = view[view["sentiment"] == sent_map[sent_sel]]
if cat_sel != "Alle":
    view = view[view["category"] == cat_sel]
view = view.sort_values("likes" if sort_sel == "Meiste Reaktionen" else "created_at", ascending=False)

st.caption(f"{len(view)} von {n} Beiträgen")

SENT_LABEL = {"positive": ("Positiv", POS), "neutral": ("Neutral", NEU), "negative": ("Negativ", NEG)}
for _, r in view.iterrows():
    label, color = SENT_LABEL.get(r["sentiment"], ("–", NEU))
    if r["severity"] == "critical":
        color, label = NEG, "Kritisch"
    text = escape(r["text"])
    if len(text) > 420:
        text = text[:420].rsplit(" ", 1)[0] + " …"
    st.markdown(f"""
<div class="post" style="--accent:{color}">
  <div class="top">
    <div><div class="who">{escape(r['author'])}</div><div class="role">{escape(r.get('author_title', '') or '')}</div></div>
    <div class="when" title="{fmt_dt(r['created_at'])}">{rel_time(r['created_at'])}</div>
  </div>
  <div class="txt">{text}</div>
  <div class="meta">
    <span class="pill sent">{label} · {r['confidence']:.0%}</span>
    <span class="pill src">{escape(r['source'])}</span>
    <span class="pill cat">{escape(r['category'])}</span>
    <span class="stat">👍 {int(r['likes'])} &nbsp; 💬 {int(r['comments'])}</span>
    <a class="open" href="{escape(r['url'])}" target="_blank" rel="noopener">Beitrag öffnen ↗</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="foot">Alle Beiträge wurden einzeln geöffnet und geprüft. Reaktionen: Stand der letzten Prüfung ({fmt_dt(verified)}). '
    f'Stimmung = redaktionelle Einordnung mit Konfidenzwert. · Pinien Art &amp; Media</div>',
    unsafe_allow_html=True)
