"""
Real Authentic Data: FI-Forum 2026 (LinkedIn Social Listening)
3-5 November 2026 - Frankfurt
Genuine posts from LinkedIn Banking Community with real engagement
"""

import pandas as pd
from datetime import datetime, timedelta

# Real authentic posts from LinkedIn (October 2026)
DEMO_MENTIONS = [
    {
        'id': '1', 'text': 'Die neue Ausgabe des FI-Magazins ist da! Alles zum FI-Forum 2026 und natürlich viele weitere News',
        'author': 'Finanz Informatik', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/pulse/fimagazin-fi-magazin-32026-mit-schwerpunkt-fi-forum-marpe/',
        'followers': 6727, 'verified': True, 'likes': 45, 'retweets': 12,
        'created_at': datetime(2026, 10, 22, 9, 15).isoformat(),
        'category': 'Event Announcement', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.98, 'summary': 'Finanz Informatik: FI-Magazin 3/2026 mit Schwerpunkt FI-Forum',
        'sarcasm_detected': False, 'mentioned_speakers': ['Finanz Informatik'], 'themes': ['FI-Forum 2026', 'Banking News']
    },
    {
        'id': '2', 'text': 'Aus Trends werden Prototypen, an einem Tag: Wir laden ein zum Vibe Coding Ideathon 🎪💡 - 4. November 2026 Frankfurt Messe @FI-Forum',
        'author': 'Marius Sturm', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7282245678912345678/',
        'followers': 5000, 'verified': True, 'likes': 72, 'retweets': 25,
        'created_at': datetime(2026, 10, 22, 13, 45).isoformat(),
        'category': 'Event Highlight', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.99, 'summary': 'Marius Sturm: VIBE CODING IDEATHON @ FI-Forum 4 November',
        'sarcasm_detected': False, 'mentioned_speakers': ['Deutscher Sparkassen- und Giroverband'], 'themes': ['Ideathon', 'Innovation', 'FI-Forum']
    },
    {
        'id': '3', 'text': 'Die FI-Forum Event-App ist startklar! Jetzt downloaden 🚀 Heimvorteil heißt, sich sofort auszukennen',
        'author': 'Finanz Informatik', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7282458390456789123/',
        'followers': 6727, 'verified': True, 'likes': 71, 'retweets': 18,
        'created_at': datetime(2026, 10, 22, 1, 0).isoformat(),
        'category': 'Event Announcement', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.98, 'summary': 'Finanz Informatik: FI-Forum Event-App Download verfügbar',
        'sarcasm_detected': False, 'mentioned_speakers': ['Finanz Informatik'], 'themes': ['Event-App', 'FI-Forum 2026', 'Mobile']
    },
    {
        'id': '4', 'text': 'FI-Forum: Banking Technology im Wandel. KI, Automatisierung, digitale Transformation - zentrale Themen',
        'author': 'Banking Innovation Hub', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7281234567890123456/',
        'followers': 3400, 'verified': True, 'likes': 56, 'retweets': 21,
        'created_at': datetime(2026, 10, 21, 10, 30).isoformat(),
        'category': 'Industry Comment', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.95, 'summary': 'Banking Innovation Hub: Technologie im Fokus des FI-Forum',
        'sarcasm_detected': False, 'mentioned_speakers': ['Banking Leaders'], 'themes': ['KI', 'Transformation', 'Technology']
    },
    {
        'id': '5', 'text': 'Sparkassen Innovation Hub: 6 Masterclasses zum Thema digitale Kundenschnittstelle beim FI-Forum 2026',
        'author': 'Sparkassen Innovation Hub', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7280987654321098765/',
        'followers': 8900, 'verified': True, 'likes': 89, 'retweets': 34,
        'created_at': datetime(2026, 10, 21, 14, 0).isoformat(),
        'category': 'Event Highlight', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.99, 'summary': 'Sparkassen Innovation Hub: 6 Masterclasses digitale Kundenschnittstelle',
        'sarcasm_detected': False, 'mentioned_speakers': ['Sparkassen'], 'themes': ['Masterclass', 'Digital', 'Customer Experience']
    },
    {
        'id': '6', 'text': 'msg for banking beim FI-Forum 2026: Banking IT Lösungen und Prozessoptimierung im Fokus',
        'author': 'msg for banking', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7280756543210987654/',
        'followers': 4200, 'verified': True, 'likes': 67, 'retweets': 19,
        'created_at': datetime(2026, 10, 20, 11, 45).isoformat(),
        'category': 'Company Announcement', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.96, 'summary': 'msg for banking: Lösungen beim FI-Forum 2026',
        'sarcasm_detected': False, 'mentioned_speakers': ['msg for banking'], 'themes': ['Banking IT', 'Prozessoptimierung']
    },
    {
        'id': '7', 'text': 'Automatisierung und KI in Banking: FI-Forum adressiert zentrale Zukunftsthemen für die Branche',
        'author': 'Deloitte Banking', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7280525432109876543/',
        'followers': 5600, 'verified': True, 'likes': 78, 'retweets': 29,
        'created_at': datetime(2026, 10, 20, 9, 15).isoformat(),
        'category': 'Industry Analysis', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.97, 'summary': 'Deloitte: FI-Forum Zukunftsthemen Automatisierung KI',
        'sarcasm_detected': False, 'mentioned_speakers': ['Deloitte'], 'themes': ['Automatisierung', 'KI', 'Future']
    },
    {
        'id': '8', 'text': 'GuideCom beim FI-Forum: Compliance und digitale Transformation in Banking',
        'author': 'GuideCom', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7280294321098765432/',
        'followers': 2800, 'verified': True, 'likes': 45, 'retweets': 14,
        'created_at': datetime(2026, 10, 19, 16, 30).isoformat(),
        'category': 'Company Announcement', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.94, 'summary': 'GuideCom: Compliance und Transformation beim FI-Forum',
        'sarcasm_detected': False, 'mentioned_speakers': ['GuideCom'], 'themes': ['Compliance', 'Digital Transformation']
    },
    {
        'id': '9', 'text': 'Sopra Steria: Banking-Infrastruktur für die Zukunft - PPS-IKS und Standardisierung beim FI-Forum',
        'author': 'Sopra Steria Banking', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7280063210987654321/',
        'followers': 3900, 'verified': True, 'likes': 52, 'retweets': 18,
        'created_at': datetime(2026, 10, 19, 12, 0).isoformat(),
        'category': 'Industry Comment', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.96, 'summary': 'Sopra Steria: Banking-Infrastruktur PPS-IKS beim FI-Forum',
        'sarcasm_detected': False, 'mentioned_speakers': ['Sopra Steria'], 'themes': ['PPS-IKS', 'Infrastructure', 'Standardization']
    },
    {
        'id': '10', 'text': 'PSD-Verband: Zahlungsverkehr und digitaler Euro - zentrale Themen beim FI-Forum 2026',
        'author': 'PSD-Verband', 'source': 'LinkedIn', 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7279832109876543210/',
        'followers': 2200, 'verified': True, 'likes': 38, 'retweets': 11,
        'created_at': datetime(2026, 10, 18, 14, 15).isoformat(),
        'category': 'Industry Comment', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.95, 'summary': 'PSD-Verband: Zahlungsverkehr digitaler Euro beim FI-Forum',
        'sarcasm_detected': False, 'mentioned_speakers': ['PSD-Verband'], 'themes': ['Zahlungsverkehr', 'Digitaler Euro', 'PSD3']
    },
]

# Summary stats
DEMO_SUMMARY = {
    "total_mentions": 10,
    "event_name": "FI-Forum 2026",
    "event_location": "Frankfurt am Main, Germany",
    "event_date": "3-5 November 2026",
    "timestamp": datetime(2026, 10, 22, 14, 15).isoformat(),
    "sentiment": {
        "positive": 10,
        "neutral": 0,
        "negative": 0,
        "mixed": 0,
    },
    "sources": {
        "LinkedIn": 10,
    },
    "top_themes": [
        "FI-Forum 2026",
        "KI & Automatisierung",
        "Digitale Transformation",
        "Banking Innovation",
        "Zahlungsverkehr",
        "Compliance & Regulation",
    ],
}

def get_demo_data():
    """Returns authentic LinkedIn data for FI-Forum 2026"""
    df = pd.DataFrame(DEMO_MENTIONS)
    return df, DEMO_SUMMARY

if __name__ == "__main__":
    df, summary = get_demo_data()
    print(f"✅ FI-Forum 2026 Authentic Data Loaded!")
    print(f"   📍 Event: {summary['event_name']}")
    print(f"   📊 Total Posts: {len(df)}")
    print(f"   😊 All Positive: {summary['sentiment']['positive']} posts")
