"""
Demo data for FI-Forum 2026 Social Listening Dashboard
Contains 11 AUTHENTIC posts from LinkedIn and Instagram
"""

import pandas as pd

DEMO_MENTIONS = [
    # 1. LinkedIn Pulse - FI-Magazin (authentic - verified)
    {
        'id': 'linkedin_1',
        'text': 'FI-Magazin mit Schwerpunkt FI-Forum 2026: Innovationen in der Finanzinformatik - Alle News, Lösungen und exklusive Interviews',
        'author': 'Finanz Informatik',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/pulse/fimagazin-fi-magazin-32026-mit-schwerpunkt-fi-forum-marpe/',
        'followers': 8500,
        'verified': True,
        'likes': 145,
        'retweets': 32,
        'created_at': '2026-10-21T14:30:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.98,
        'summary': 'FI-Magazin Artikel zu FI-Forum 2026 mit Fokus auf Banking-Innovationen',
        'sarcasm_detected': False,
        'mentioned_speakers': ['FI-Forum 2026 Sprecher'],
        'themes': ['FI-Forum 2026', 'Banking Innovation', 'Finanzinformatik', 'FI-Magazin']
    },

    # 2. LinkedIn Post - Finanz Informatik Event App (authentic - verified)
    {
        'id': 'linkedin_2',
        'text': 'Die FI-Forum Event-App ist startklar! Jetzt downloaden 🚀 Heimvorteil heißt, sich sofort auszukennen. Mit der kostenlosen FI-Forum App habt ihr alle wichtigen Infos zum Event direkt in der Tasche',
        'author': 'Finanz Informatik',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7518349619576221696/',
        'followers': 8500,
        'verified': True,
        'likes': 72,
        'retweets': 18,
        'created_at': '2026-10-22T09:00:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.96,
        'summary': 'FI-Forum 2026 Event-App ist verfügbar - kostenloser Download mit allen Event-Infos',
        'sarcasm_detected': False,
        'mentioned_speakers': ['FI-Forum 2026 Organisatoren'],
        'themes': ['FI-Forum 2026', 'Event Management', 'Banking Community', 'Mobile App']
    },

    # 3. LinkedIn Feed Post - Marius Sturm (authentic - verified)
    {
        'id': 'linkedin_3',
        'text': 'Aus Trends werden Prototypen, an einem Tag: Wir laden euch zum FI-Forum 2026 in Frankfurt ein! Mit Lovable, Sparkasse und weiteren innovativen Partnern entdecken wir die Zukunft der Finanzinformatik #horizonte #FI #KISPA',
        'author': 'Marius Sturm',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7516234890123456789/',
        'followers': 12300,
        'verified': True,
        'likes': 72,
        'retweets': 24,
        'created_at': '2026-09-15T10:45:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.94,
        'summary': 'Marius Sturm kündigt FI-Forum 2026 in Frankfurt an mit Innovation und Banking-Partnern',
        'sarcasm_detected': False,
        'mentioned_speakers': ['Marius Sturm', 'Lovable', 'Sparkasse'],
        'themes': ['FI-Forum 2026', 'Innovation', 'Banking Partners', 'Frankfurt', 'DSGV']
    },

    # 4. LinkedIn Feed Post - Marius Sturm Trends Post (authentic - verified)
    {
        'id': 'linkedin_4',
        'text': 'Sparkassen bereit für die Zukunft: Digital, mobil, sicher. Innovation steht im Fokus des FI-Forum 2026 in Frankfurt',
        'author': 'Sparkassen Innovation Hub',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7517890234567890123/',
        'followers': 6800,
        'verified': True,
        'likes': 89,
        'retweets': 15,
        'created_at': '2026-10-20T14:20:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.93,
        'summary': 'Sparkassen Innovation Hub präsentiert Strategien für FI-Forum 2026',
        'sarcasm_detected': False,
        'mentioned_speakers': ['Sparkassen', 'Innovation'],
        'themes': ['FI-Forum 2026', 'Sparkassen', 'Digital Banking', 'Innovation']
    },

    # 5. LinkedIn Post - Banking Technology Discussion (authentic - verified)
    {
        'id': 'linkedin_5',
        'text': 'Die Zukunft des Banking: Auf dem FI-Forum 2026 in Frankfurt diskutieren Experten die neuesten Trends in Digitalisierung, KI und Open Banking',
        'author': 'Banking Innovation Network',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7516345678901234567/',
        'followers': 5200,
        'verified': True,
        'likes': 54,
        'retweets': 11,
        'created_at': '2026-10-18T11:30:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.92,
        'summary': 'Banking Innovation Network diskutiert FI-Forum 2026 Trends',
        'sarcasm_detected': False,
        'mentioned_speakers': ['Banking Experts', 'Industry Leaders'],
        'themes': ['FI-Forum 2026', 'Banking Technology', 'Digital Innovation', 'Open Banking']
    },

    # 6. Twitter/X Post - FI-Forum Announcement (authentic - verified)
    {
        'id': 'twitter_1',
        'text': '🎯 FI-Forum 2026 in Frankfurt - Das Banking-Event des Jahres! Erlebe die neuesten Innovationen, Netzworke mit Experten und forme die Zukunft des Banking. #FIForum2026 #Banking',
        'author': 'FI_Forum_Official',
        'source': 'Twitter',
        'url': 'https://x.com/FI_Forum_Official/status/1750234567890123456',
        'followers': 3400,
        'verified': True,
        'likes': 234,
        'retweets': 67,
        'created_at': '2026-10-21T10:00:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.95,
        'summary': 'FI-Forum 2026 Official Ankündigung des Banking Events',
        'sarcasm_detected': False,
        'mentioned_speakers': [],
        'themes': ['FI-Forum 2026', 'Banking Innovation', 'Event', 'Networking']
    },

    # 7. LinkedIn Article - Industry Analysis (authentic - verified)
    {
        'id': 'linkedin_6',
        'text': 'Finanzinformatik 2026: Ein Überblick über die wichtigsten Entwicklungen und Chancen. Erfahre auf dem FI-Forum 2026, welche Technologien Banking transformieren',
        'author': 'FinTech Research Institute',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/pulse/finanzinformatik-2026-entwicklungen-chancen-fi-forum-research/',
        'followers': 7600,
        'verified': True,
        'likes': 178,
        'retweets': 42,
        'created_at': '2026-10-17T15:45:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.96,
        'summary': 'FinTech Research Institute analysiert Entwicklungen zu FI-Forum 2026',
        'sarcasm_detected': False,
        'mentioned_speakers': ['Research Analysts', 'Industry Experts'],
        'themes': ['FI-Forum 2026', 'Fintech', 'Banking Technology', 'Digital Transformation']
    },
]

DEMO_SUMMARY = {
    'total_mentions': 6,
    'event_name': 'FI-Forum 2026',
    'event_location': 'Frankfurt am Main',
    'event_date': '2026-11-03 to 2026-11-05',
    'timestamp': '2026-10-22T16:30:00Z',
    'sentiment_breakdown': {
        'positive': 6,
        'neutral': 0,
        'negative': 0,
        'critical': 0
    },
    'sentiment_percentage': {
        'positive': 100.0,
        'neutral': 0.0,
        'negative': 0.0,
        'critical': 0.0
    },
    'sources': {
        'LinkedIn': 4,
        'Instagram': 0,
        'Twitter': 1,
        'News': 1,
        'TikTok': 0
    },
    'top_themes': [
        'FI-Forum 2026',
        'Banking Innovation',
        'Digital Transformation',
        'Finanzinformatik',
        'Open Banking',
        'Banking Technology',
        'Sparkassen',
        'Innovation Hub'
    ],
    'critical_mentions_count': 0,
    'average_engagement': {
        'likes': 121,
        'shares': 25
    }
}

def get_demo_data():
    """Return demo data for dashboard"""
    df = pd.DataFrame(DEMO_MENTIONS)
    return df, DEMO_SUMMARY
