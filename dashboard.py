"""
FI-Forum 2026 · Social Listening Dashboard
"""

from datetime import datetime, timezone, date
from html import escape
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import base64
from pathlib import Path

import importlib
import demo_data
demo_data = importlib.reload(demo_data)  # always pick up freshly pushed data
get_demo_data, VERIFIED_AT = demo_data.get_demo_data, demo_data.VERIFIED_AT

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
  display: flex; justify-content: space-between; align-items: stretch; gap: 24px; flex-wrap: wrap;
  box-shadow: 0 10px 30px rgba(227,6,19,.18);
}}
.logo-pill {{ display:inline-flex; background:#fff; border-radius:10px; padding:8px 14px; }}
.logo-pill img {{ height:26px; display:block; }}
.hero .eyebrow {{ font-size: 12px; letter-spacing: .14em; text-transform: uppercase; opacity: .85; font-weight: 600; }}
.hero h1 {{ font-size: 34px; font-weight: 800; margin: 6px 0 6px; line-height: 1.1; color: #fff; }}
.hero .sub {{ font-size: 15px; opacity: .92; }}
.hero .right {{ text-align: right; display:flex; flex-direction:column; align-items:flex-end; gap:12px; }}
.hero .right .logo-pill {{ margin-bottom:6px; }}
.hero .right .countdown {{ margin-top:0; }}
.badge-live {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,.16);
  padding: 6px 12px; border-radius: 999px; font-size: 13px; font-weight: 600; }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; background: #7CFFB2; box-shadow: 0 0 0 4px rgba(124,255,178,.25); }}
.countdown {{ font-size: 42px; font-weight: 800; line-height: 1; margin-top: 10px; }}
.countdown small {{ font-size: 14px; font-weight: 500; opacity: .9; }}

.kpis {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin: 18px 0 8px; }}
@media (max-width: 900px) {{ .kpis {{ grid-template-columns: repeat(2, 1fr); }} .hero .right {{ text-align: left; }} }}
.kpi {{ background: #fff; border: 1px solid {LINE}; border-radius: 14px; padding: 16px 18px; }}
.kpi .label {{ font-size: 12px; color: {MUTED}; font-weight: 600; text-transform: uppercase; letter-spacing: .06em; }}
.info {{ position: relative; display: inline-flex; align-items: center; justify-content: center; width: 12px; height: 12px; margin-left: 4px; border-radius: 50%; border: 1px solid {MUTED}; color: {MUTED}; font-size: 8px; font-weight: 700; text-transform: none; letter-spacing: 0; cursor: help; vertical-align: 1px; }}
.info .tip {{ visibility: hidden; opacity: 0; position: absolute; top: 18px; left: 50%; transform: translateX(-50%); width: 230px; background: {INK}; color: #fff; font-size: 12px; font-weight: 400; line-height: 1.45; padding: 9px 11px; border-radius: 8px; z-index: 20; transition: opacity .15s; box-shadow: 0 6px 18px rgba(0,0,0,.18); }}
.info:hover .tip {{ visibility: visible; opacity: 1; }}
.kpi:last-child .info .tip {{ left: auto; right: -8px; transform: none; }}
.kpi:first-child .info .tip {{ left: -8px; transform: none; }}
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

.post .role {{ padding-left: 36px; }}
.post .role {{ color: {MUTED}; font-size: 13px; margin-top: 1px; }}
.post .when {{ color: {MUTED}; font-size: 12px; white-space: nowrap; }}
.post .txt {{ color: #2B2B2B; font-size: 14.5px; line-height: 1.55; margin: 12px 0 12px; }}
.post .meta {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
.pill {{ border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 600; }}
.chtable {{ background:#fff; border:1px solid {LINE}; border-radius:14px; padding:6px 18px; margin: 4px 0 14px; }}
.chrow {{ display:grid; grid-template-columns: 1.3fr .9fr .9fr 1.8fr; gap:10px; align-items:center; padding:8px 0; border-bottom:1px solid {LINE}; font-size:14px; }}
.chrow:last-child {{ border-bottom:none; }}
.chrow.off {{ opacity:.5; }}
.chhead {{ font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:{MUTED}; font-weight:700; }}
.chname {{ display:flex; align-items:center; gap:10px; font-weight:600; }}
.chnum {{ text-align:center; font-weight:800; font-size:16px; }}
.chhead .chnum {{ font-size:11px; font-weight:700; }}
.chnote {{ color:{MUTED}; font-size:13px; }}
.pill.own {{ background:#FDECEE; color:#B00510; }}
.srcbar {{ display:flex; flex-wrap:wrap; gap:10px; margin: 4px 0 14px; }}
.srcitem {{ display:flex; align-items:center; gap:8px; background:#fff; border:1px solid {LINE}; border-radius:999px; padding:5px 14px 5px 6px; font-size:13px; font-weight:600; color:{INK}; }}
.srcitem.off {{ opacity:.45; }}
.srcitem b {{ font-weight:800; }}
.plat {{ display:inline-flex; border-radius:7px; box-sizing:border-box; flex-shrink:0; }}
.post .who {{ display:flex; align-items:center; gap:10px; }}
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


PLATFORM = {
    "LinkedIn": ("#0A66C2", '<path fill="#fff" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.064 2.064 0 1 1 0-4.128 2.064 2.064 0 0 1 0 4.128zm1.782 13.019H3.555V9h3.564v11.452z"/>'),
    "Instagram": ("linear-gradient(45deg,#F58529,#DD2A7B 50%,#8134AF 75%,#515BD4)", '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="#fff" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.3" fill="#fff"/>'),
    "Facebook": ("#1877F2", '<path fill="#fff" d="M15.12 5.32H17V2.14A26.11 26.11 0 0 0 14.26 2c-2.72 0-4.58 1.66-4.58 4.7v2.62H6.61v3.56h3.07V22h3.68v-9.12h3.06l.46-3.56h-3.52V7.05c0-1.03.28-1.73 1.76-1.73Z"/>'),
    "TikTok": ("#000", '<path fill="#fff" d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/>'),
    "X": ("#000", '<path fill="#fff" d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/>'),
    "News": ("#44474D", '<rect x="3" y="4" width="18" height="16" rx="2" fill="none" stroke="#fff" stroke-width="2"/><path stroke="#fff" stroke-width="2" d="M7 9h10M7 13h10M7 17h6"/>'),
}


def platform_badge(src: str, size: int = 26) -> str:
    bg, svg = PLATFORM.get(src, PLATFORM["News"])
    pad = round(size * 0.22)
    return (f'<span class="plat" title="{escape(src)}" style="background:{bg};width:{size}px;height:{size}px;padding:{pad}px">'
            f'<svg viewBox="0 0 24 24" width="100%" height="100%">{svg}</svg></span>')

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

# Official channels of the organiser (Finanz Informatik) vs. external voices
OWN_AUTHORS = {"Finanz Informatik", "finanz_informatik", "FI-Magazin Plus", "FI-Magazin"}
df["own"] = df["author"].isin(OWN_AUTHORS)
CHANNEL_NOTES = {
    "LinkedIn": "FI-Unternehmensseite",
    "Instagram": "@finanz_informatik",
    "Facebook": "facebook.com/Finanz.Informatik",
    "TikTok": "kein offizieller FI-Kanal",
    "X": "@FI_FFM – seit 03/2025 inaktiv",
    "News": "Presse &amp; Online-Medien",
}

n = len(df)
reactions = int(df["likes"].sum())
comments = int(df["comments"].sum())
pos_share = round(100 * (df["sentiment"] == "positive").mean()) if n else 0
critical = int(df["severity"].isin(["warning", "critical"]).sum())
authors = df["author"].nunique()
days_left = (EVENT_START - datetime.now(TZ).date()).days
verified = pd.Timestamp(VERIFIED_AT)

_logo = Path(__file__).with_name("fi_logo.png")
LOGO_IMG = (f'<img src="data:image/png;base64,{base64.b64encode(_logo.read_bytes()).decode()}" alt="Finanz Informatik">'
            if _logo.exists() else "")
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
    <div class="logo-pill">{LOGO_IMG}</div>
    <div class="badge-live"><span class="dot"></span>Zuletzt geprüft: {fmt_dt(verified)}</div>
    <div class="countdown">{countdown}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- KPIs ----------
st.markdown(f"""
<div class="kpis">
  <div class="kpi"><div class="label">Beiträge<span class="info">i<span class="tip">Alle öffentlichen Beiträge zum FI-Forum 2026, die einzeln geöffnet und geprüft wurden. Jeder Eintrag hat einen anklickbaren Originallink.</span></span></div><div class="value">{n}</div><div class="hint">verifiziert, mit Link</div></div>
  <div class="kpi"><div class="label">Reaktionen<span class="info">i<span class="tip">Summe aller Likes und sonstigen Reaktionen (z. B. Applaus, Herz) unter den erfassten Beiträgen. Reposts und Aufrufe sind nicht enthalten.</span></span></div><div class="value">{reactions:,}</div><div class="hint">Summe aller Beiträge</div></div>
  <div class="kpi"><div class="label">Kommentare<span class="info">i<span class="tip">Summe aller öffentlichen Kommentare unter den erfassten Beiträgen. Antworten auf Kommentare zählen mit.</span></span></div><div class="value">{comments}</div><div class="hint">Summe aller Beiträge</div></div>
  <div class="kpi"><div class="label">Stimmung positiv<span class="info">i<span class="tip">Anteil der Beiträge, deren Tonalität positiv eingeordnet ist (Vorfreude, Lob, Empfehlung). Neutral = rein informativ oder abwägend.</span></span></div><div class="value" style="color:{POS}">{pos_share}%</div><div class="hint">Anteil der Beiträge</div></div>
  <div class="kpi"><div class="label">Kritische Hinweise<span class="info">i<span class="tip">Beiträge mit negativer Stimmung oder Kritik am Event bzw. an der FI. Sie werden als Frühwarnung sofort markiert.</span></span></div><div class="value" style="color:{NEG if critical else INK}">{critical}</div><div class="hint">{authors} verschiedene Absender</div></div>
</div>
""".replace(",", "."), unsafe_allow_html=True)

own_c = df[df["own"]]["source"].value_counts()
ext_c = df[~df["own"]]["source"].value_counts()
rows = ""
for p in ["LinkedIn", "Instagram", "Facebook", "TikTok", "X", "News"]:
    o, e = int(own_c.get(p, 0)), int(ext_c.get(p, 0))
    rows += (f'<div class="chrow{"" if o + e else " off"}"><div class="chname">{platform_badge(p, 24)}<span>{p}</span></div>'
             f'<div class="chnum">{o if p != "News" else "–"}</div><div class="chnum">{e}</div><div class="chnote">{CHANNEL_NOTES[p]}</div></div>')
st.markdown(f'''<div class="chtable">
  <div class="chrow chhead"><div>Plattform</div><div class="chnum">Eigene FI-Kanäle</div><div class="chnum">Externe Stimmen</div><div>Offizieller FI-Kanal</div></div>
  {rows}
</div>''', unsafe_allow_html=True)

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
    CHART_START = date(2026, 10, 1)
    days_local = df["created_at"].dt.tz_convert(TZ).dt.date
    earlier = int((days_local < CHART_START).sum())
    per_day = days_local[days_local >= CHART_START].value_counts().sort_index()
    rng = pd.date_range(CHART_START, max(datetime.now(TZ).date(), max(per_day.index, default=CHART_START)))
    per_day = per_day.reindex(rng.date, fill_value=0)
    chart_mode = st.segmented_control("Darstellung", ["Balken", "Linie", "Kumuliert", "Kanal", "Stimmung"], default="Balken",
                                      key="day_chart_mode", label_visibility="collapsed") or "Balken"
    xs = pd.to_datetime(list(per_day.index))
    ys = per_day.values
    if chart_mode in ("Kanal", "Stimmung"):
        sub = df.assign(day=days_local)
        sub = sub[sub["day"] >= CHART_START]
        if chart_mode == "Kanal":
            col = "source"
            groups = [g for g in ["LinkedIn", "Instagram", "Facebook", "TikTok", "X", "News"] if g in set(sub[col])]
            colors = {"LinkedIn": "#0A66C2", "Instagram": "#DD2A7B", "Facebook": "#1877F2", "TikTok": "#111111", "X": "#555555", "News": "#9AA0A6"}
            labels = {g: g for g in groups}
        else:
            col = "sentiment"
            groups = [g for g in ["positive", "neutral", "negative"] if g in set(sub[col])]
            colors = {"positive": POS, "neutral": NEU, "negative": NEG}
            labels = {"positive": "Positiv", "neutral": "Neutral", "negative": "Negativ"}
        fig = go.Figure()
        for g in groups:
            cnt = sub[sub[col] == g]["day"].value_counts().reindex(rng.date, fill_value=0)
            fig.add_trace(go.Bar(x=xs, y=cnt.values, name=labels[g], marker_color=colors[g], marker_line_width=0,
                                 hovertemplate="%{x|%d.%m.}: %{y} " + labels[g] + "<extra></extra>"))
        fig.update_layout(barmode="stack", bargap=0.15)
    elif chart_mode == "Balken":
        fig = go.Figure(go.Bar(x=xs, y=ys, marker_color=RED, marker_line_width=0,
                               hovertemplate="%{x|%d.%m.}: %{y} Beiträge<extra></extra>"))
        fig.update_layout(bargap=0.15)
    else:
        yv = ys.cumsum() + earlier if chart_mode == "Kumuliert" else ys
        label = "Beiträge gesamt" if chart_mode == "Kumuliert" else "Beiträge"
        fig = go.Figure(go.Scatter(x=xs, y=yv, mode="lines+markers", line=dict(color=RED, width=2.5, shape="spline", smoothing=0.6),
                                   marker=dict(size=5, color=RED), fill="tozeroy", fillcolor="rgba(227,6,19,0.08)",
                                   hovertemplate="%{x|%d.%m.}: %{y} " + label + "<extra></extra>"))
    fig.add_vrect(x0=pd.Timestamp(EVENT_START) - pd.Timedelta(hours=12), x1=pd.Timestamp(EVENT_START) + pd.Timedelta(days=2, hours=12),
                  fillcolor="rgba(227,6,19,0.06)", line_width=0, annotation_text="FI-Forum", annotation_position="top left",
                  annotation_font=dict(size=11, color=MUTED))
    fig.update_yaxes(gridcolor=LINE, nticks=6, zeroline=False, rangemode="tozero")
    fig.update_xaxes(showgrid=False, tickformat="%d.%m.", dtick=7 * 24 * 3600 * 1000, tick0="2026-10-01",
                     range=[pd.Timestamp(CHART_START) - pd.Timedelta(hours=12), pd.Timestamp(max(rng[-1].date(), date(2026, 11, 10))) + pd.Timedelta(hours=12)])
    if earlier:
        st.caption(f"Ab 1. Oktober · {earlier} ältere Beiträge ausgeblendet")
    fig = plot_base(fig)
    if chart_mode in ("Kanal", "Stimmung"):
        fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=11)), margin=dict(b=40))
    st.plotly_chart(fig, use_container_width=True, config=cfg)

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
f0, f1, f2, f3 = st.columns([1, 1, 1, 1])
with f0:
    own_sel = st.selectbox("Absender", ["Alle", "Eigene FI-Kanäle", "Externe Stimmen"])
with f1:
    sent_map = {"Alle": None, "Positiv": "positive", "Neutral": "neutral", "Negativ": "negative"}
    sent_sel = st.selectbox("Stimmung", list(sent_map.keys()))
with f2:
    cat_sel = st.selectbox("Art des Beitrags", ["Alle"] + sorted(df["category"].unique().tolist()))
with f3:
    sort_sel = st.selectbox("Sortierung", ["Neueste zuerst", "Meiste Reaktionen"])

view = df.copy()
if own_sel != "Alle":
    view = view[view["own"] == (own_sel == "Eigene FI-Kanäle")]
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
    <div><div class="who">{platform_badge(r['source'])}{escape(r['author'])}</div><div class="role">{escape(r.get('author_title', '') or '')}</div></div>
    <div class="when" title="{fmt_dt(r['created_at'])}">{rel_time(r['created_at'])}</div>
  </div>
  <div class="txt">{text}</div>
  <div class="meta">
    <span class="pill sent">{label} · {r['confidence']:.0%}</span>
    {'<span class="pill own">FI-Kanal</span>' if r['own'] else ''}<span class="pill cat">{escape(r['category'])}</span>
    <span class="stat">👍 {int(r['likes'])} &nbsp; 💬 {int(r['comments'])}</span>
    <a class="open" href="{escape(r['url'])}" target="_blank" rel="noopener">Beitrag öffnen ↗</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="foot">Alle Beiträge wurden einzeln geöffnet und geprüft. Reaktionen: Stand der letzten Prüfung ({fmt_dt(verified)}). '
    f'Stimmung = redaktionelle Einordnung mit Konfidenzwert. · Pinien Art &amp; Media</div>',
    unsafe_allow_html=True)
