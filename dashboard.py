"""
Streamlit Dashboard
Real-time visualization of FI-Forum social listening data
Event: FI-Forum Social Listening Pipeline
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Optional
import json
import os
import base64
from io import BytesIO
from PIL import Image

# Check if we have real data or use demo
try:
    from storage import StorageManager
    from config import event_config, system_config
    HAS_STORAGE = True
except:
    HAS_STORAGE = False

# Demo data fallback
from demo_data import get_demo_data

# Page configuration
st.set_page_config(
    page_title="FI-Forum Social Listening",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sparkassen Logo (embedded as Base64)
SPARKASSEN_LOGO_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAyAAAAMgCAYAAADbcAZoAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAg..."  # Truncated for space

# Initialize session state
if 'refresh_count' not in st.session_state:
    st.session_state.refresh_count = 0


def load_data() -> tuple:
    """Load latest data from storage or demo"""
    if HAS_STORAGE:
        try:
            storage = StorageManager()
            analyzed_df, summary = storage.get_data_for_dashboard()
            if analyzed_df is not None and summary is not None:
                return analyzed_df, summary
        except:
            pass

    # Fallback to demo data
    return get_demo_data()


def render_header():
    """Render dashboard header with Sparkassen branding"""
    col1, col2, col3 = st.columns([1, 3, 1])

    # Logo
    with col1:
        try:
            st.image("sparkassen_logo.png", width=80)
        except:
            st.markdown("🏦")

    # Title & Info
    with col2:
        st.markdown("""
        <h1 style='color: #E31E24; margin: 0;'>FI-Forum Social Listening</h1>
        """, unsafe_allow_html=True)
        event_name = "FI-Forum 2026" if not HAS_STORAGE else event_config.EVENT_NAME
        date_range = "3-5 November 2026" if not HAS_STORAGE else f"{event_config.EVENT_START_DATE} bis {event_config.EVENT_END_DATE}"
        st.markdown(f"**Event:** {event_name} | **Zeitraum:** {date_range}")

    # Refresh button
    with col3:
        if st.button("🔄 Aktualisieren"):
            st.session_state.refresh_count += 1
            st.rerun()

        last_update = datetime.utcnow().strftime("%H:%M:%S UTC")
        st.markdown(f"**Aktualisiert:** {last_update}")


def render_kpi_cards(summary: Optional[dict]):
    """Render KPI cards"""
    if not summary:
        st.warning("⚠️  Keine Daten verfügbar")
        return

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "📊 Gesamt Mentions",
            summary.get('total_mentions', 0)
        )

    with col2:
        sentiment = summary.get('sentiment', {})
        positive = sentiment.get('positive', 0)
        st.metric(
            "😊 Positiv",
            positive,
            delta=None
        )

    with col3:
        neutral = sentiment.get('neutral', 0)
        st.metric(
            "😐 Neutral",
            neutral
        )

    with col4:
        negative = sentiment.get('negative', 0)
        st.metric(
            "😞 Negativ",
            negative,
            delta_color="inverse"
        )

    with col5:
        critical = summary.get('severity', {}).get('critical', 0)
        st.metric(
            "🚨 Kritisch",
            critical,
            delta_color="inverse"
        )


def render_sentiment_chart(summary: Optional[dict]):
    """Render sentiment distribution chart with Sparkassen branding"""
    if not summary:
        return

    sentiment = summary.get('sentiment', {})

    fig = go.Figure(data=[
        go.Pie(
            labels=['Positiv', 'Neutral', 'Negativ'],
            values=[
                sentiment.get('positive', 0),
                sentiment.get('neutral', 0),
                sentiment.get('negative', 0)
            ],
            marker=dict(
                colors=['#E31E24', '#FFB81C', '#6B7280']  # Sparkassenrot, Sparkassen-Gold, Gray
            ),
            textposition='inside',
            textinfo='label+percent'
        )
    ])

    fig.update_layout(
        title="Sentiment-Verteilung",
        height=400,
        showlegend=True,
        font=dict(color='#333')
    )

    st.plotly_chart(fig, use_container_width=True)


def render_categories_chart(summary: Optional[dict]):
    """Render category distribution chart"""
    if not summary:
        return

    categories = summary.get('categories', {})

    if not categories:
        st.info("Keine Kategorie-Daten verfügbar")
        return

    # Sort by count
    sorted_cats = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))

    fig = px.bar(
        x=list(sorted_cats.values()),
        y=list(sorted_cats.keys()),
        orientation='h',
        title="Erwähnungen nach Kategorie",
        labels={'x': 'Anzahl', 'y': 'Kategorie'},
        color=list(sorted_cats.values()),
        color_continuous_scale='viridis'
    )

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_severity_chart(summary: Optional[dict]):
    """Render severity distribution chart with Sparkassen branding"""
    if not summary:
        return

    severity = summary.get('severity', {})

    fig = go.Figure(data=[
        go.Bar(
            x=['Info', 'Warning', 'Critical'],
            y=[
                severity.get('info', 0),
                severity.get('warning', 0),
                severity.get('critical', 0)
            ],
            marker=dict(
                color=['#00B0F0', '#FFB81C', '#E31E24']  # Blue, Sparkassen-Gold, Sparkassenrot
            ),
            text=[
                severity.get('info', 0),
                severity.get('warning', 0),
                severity.get('critical', 0)
            ],
            textposition='outside'
        )
    ])

    fig.update_layout(
        title="Schweregrad-Verteilung",
        height=400,
        xaxis_title="Schweregrad",
        yaxis_title="Anzahl",
        font=dict(color='#333')
    )

    st.plotly_chart(fig, use_container_width=True)


def render_sources_chart(summary: Optional[dict]):
    """Render source distribution chart"""
    if not summary:
        return

    sources = summary.get('sources', {})

    if not sources:
        st.info("Keine Quellen-Daten verfügbar")
        return

    fig = px.pie(
        values=list(sources.values()),
        names=list(sources.keys()),
        title="Mentions nach Quelle",
    )

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_themes(summary: Optional[dict]):
    """Render top themes"""
    if not summary:
        return

    themes = summary.get('top_themes', [])

    st.subheader("🏷️  Top Themen")

    if themes:
        for i, theme in enumerate(themes[:10], 1):
            st.markdown(f"{i}. **{theme}**")
    else:
        st.info("Keine Themen identifiziert")


def render_critical_mentions(summary: Optional[dict]):
    """Render critical mentions"""
    if not summary:
        return

    critical = summary.get('critical_mentions', [])

    st.subheader("🚨 Kritische Mentions")

    if critical:
        for mention in critical[:10]:  # Top 10
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**{mention.get('author', 'Unknown')}**")
                    st.markdown(mention.get('summary', ''))

                with col2:
                    st.markdown(f"📂 {mention.get('category', 'N/A')}")

                if mention.get('url'):
                    st.markdown(f"🔗 [Link]({mention.get('url')})")

                st.divider()
    else:
        st.success("✅ Keine kritischen Mentions")


def render_mentions_table(analyzed_df: Optional[pd.DataFrame]):
    """Render detailed mentions table with clickable links"""
    if analyzed_df is None or analyzed_df.empty:
        st.info("⚠️  Keine Mentions vorhanden")
        return

    st.subheader("📋 Detaillierte Mentions")

    # Prepare display data
    display_cols = [
        'author', 'text', 'source', 'sentiment', 'summary', 'url'
    ]

    available_cols = [col for col in display_cols if col in analyzed_df.columns]
    display_df = analyzed_df[available_cols].copy()

    # Filter options
    col1, col2, col3 = st.columns(3)

    with col1:
        filter_sentiment = st.multiselect(
            "Sentiment filtern",
            options=['positive', 'neutral', 'negative'],
            default=['positive', 'neutral', 'negative']
        )

    with col2:
        filter_severity = st.multiselect(
            "Schweregrad filtern",
            options=['info', 'warning', 'critical'],
            default=['info', 'warning', 'critical']
        )

    with col3:
        filter_source = st.multiselect(
            "Quelle filtern",
            options=display_df['source'].unique().tolist() if 'source' in display_df else [],
            default=display_df['source'].unique().tolist() if 'source' in display_df else []
        )

    # Apply filters
    filtered_df = display_df.copy()

    if 'sentiment' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['sentiment'].isin(filter_sentiment)]

    if 'severity' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['severity'].isin(filter_severity)]

    if 'source' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['source'].isin(filter_source)]

    # Display mentions with clickable links
    st.markdown(f"**Angezeigt:** {len(filtered_df)} von {len(display_df)} Mentions")

    for idx, row in filtered_df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"**{row.get('author', 'Unknown')}** • {row.get('source', 'Unknown')}")
                st.markdown(row.get('text', '')[:150] + "...")
                if row.get('summary'):
                    st.caption(f"📝 {row.get('summary', '')}")

            with col2:
                sentiment = row.get('sentiment', 'unknown')
                sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'negative': '😞'}.get(sentiment, '❓')
                st.markdown(f"{sentiment_emoji} **{sentiment}**")

            with col3:
                if row.get('url') and str(row.get('url')).startswith('http'):
                    st.markdown(f"[🔗 Link ↗]({row.get('url')})")
                else:
                    st.markdown("❌ N/A")

            st.divider()


def render_sidebar():
    """Render sidebar with controls and info"""
    st.sidebar.title("⚙️  Einstellungen")

    # Auto-refresh toggle
    if st.sidebar.checkbox("🔄 Auto-Refresh (alle 5 Min)", value=False):
        st.session_state.auto_refresh = True

    st.sidebar.divider()

    st.sidebar.title("📊 Pipeline Status")

    # Check if data exists
    latest_data = None
    if HAS_STORAGE:
        try:
            storage = StorageManager()
            latest_data = storage.load_latest_analyzed_data()
        except:
            pass

    # Use demo data if storage not available
    if latest_data is None:
        _, summary = get_demo_data()
        latest_data = summary.get('total_mentions', 'Demo')

    if latest_data is not None:
        st.sidebar.success("✅ Demo-Daten verfügbar")
        st.sidebar.markdown(f"**Anzahl Mentions:** {latest_data if isinstance(latest_data, int) else '325 (Demo)'}")
    else:
        st.sidebar.warning("⚠️  Keine Daten vorhanden")

    st.sidebar.divider()

    st.sidebar.title("📅 Event Info")
    if HAS_STORAGE:
        st.sidebar.markdown(f"**Event:** {event_config.EVENT_NAME}")
        st.sidebar.markdown(f"**Datum:** {event_config.EVENT_START_DATE} bis {event_config.EVENT_END_DATE}")
        st.sidebar.markdown(f"**Ort:** {event_config.LOCATION}")
    else:
        st.sidebar.markdown("**Event:** FI-Forum 2026")
        st.sidebar.markdown("**Datum:** 3-5 November 2026")
        st.sidebar.markdown("**Ort:** München, Germany")

    st.sidebar.divider()

    st.sidebar.title("🎯 Keywords monitored")
    demo_keywords = ["FI-Forum", "Networking", "Speakers", "Catering", "Organization"]
    keywords = demo_keywords if not HAS_STORAGE else event_config.KEYWORDS

    for keyword in keywords[:5]:
        st.sidebar.markdown(f"- {keyword}")

    if len(keywords) > 5:
        st.sidebar.markdown(f"- ... und {len(keywords) - 5} mehr")

    st.sidebar.divider()

    st.sidebar.title("ℹ️  Info")
    st.sidebar.markdown("""
    Dieses Dashboard zeigt Echtzeit-Monitoring von Social Media Mentions
    zum FI-Forum mit KI-gestützter Sentiment-Analyse.

    **Aktualisiert:** Täglich um 12:00 und 18:00 CET

    Powered by **Claude API**
    """)


def main():
    """Main dashboard function"""

    # Render sidebar
    render_sidebar()

    # Load data
    analyzed_df, summary = load_data()

    # Render header
    render_header()

    if summary is None:
        st.warning("⚠️  Keine Daten verfügbar. Bitte führen Sie zuerst die Data Ingestion Pipeline aus.")
        return

    # KPI Cards
    st.markdown("---")
    render_kpi_cards(summary)

    # Charts row 1
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        render_sentiment_chart(summary)

    with col2:
        render_severity_chart(summary)

    # Charts row 2
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        render_categories_chart(summary)

    with col2:
        render_sources_chart(summary)

    # Themes and critical mentions
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        render_themes(summary)

    with col2:
        render_critical_mentions(summary)

    # Detailed table
    st.markdown("---")
    render_mentions_table(analyzed_df)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 12px;">
    🤖 Social Listening Pipeline | FI-Forum 2026 | Powered by Claude API & Streamlit
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
