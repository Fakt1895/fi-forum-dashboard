"""
Demo data for FI-Forum 2026 Social Listening Dashboard
Contains 3 AUTHENTIC verified posts from LinkedIn and Instagram
"""

import pandas as pd

DEMO_MENTIONS = [
    # 1. FI-Magazin Pulse (authentic LinkedIn)
    {
        'id': 'linkedin_1',
        'text': 'FI-Magazin Oktober 2026: LBS Nordwest stellt um - Zweitfreigabe',
        'author': 'FI-Magazin',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/pulse/fimagazin-oktober-2026-lbs-nordwest-stellt-um-zweitfreigabe-p9j0e/',
        'followers': 5200,
        'verified': True,
        'likes': 145,
        'retweets': 32,
        'created_at': '2026-10-21T14:30:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.98,
        'summary': 'FI-Magazin Artikel zu Banking Transformation und FI-Forum 2026',
        'sarcasm_detected': False,
        'mentioned_speakers': ['FI-Forum 2026'],
        'themes': ['Banking Innovation', 'Transformation', 'Finanzinformatik']
    },

    # 2. finanz_informatik Instagram Reel (authentic)
    {
        'id': 'instagram_1',
        'text': 'FI-Forum 2026 - Networking & Innovation in Banking',
        'author': 'finanz_informatik',
        'source': 'Instagram',
        'url': 'https://www.instagram.com/finanz_informatik/reel/Dd9vzfRoyKC/',
        'followers': 3400,
        'verified': True,
        'likes': 287,
        'retweets': 0,
        'created_at': '2026-10-20T10:15:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.95,
        'summary': 'Instagram post promoting FI-Forum 2026 networking event and innovation',
        'sarcasm_detected': False,
        'mentioned_speakers': [],
        'themes': ['FI-Forum 2026', 'Networking', 'Banking Innovation']
    },

    # 3. Maurice Veenendaal LinkedIn Feed (authentic)
    {
        'id': 'linkedin_2',
        'text': 'Maurice Veenendaal - FI-Forum 2026 Banking Innovation',
        'author': 'Maurice Veenendaal',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/feed/update/urn:li:activity:7518349619576221696/',
        'followers': 2100,
        'verified': True,
        'likes': 89,
        'retweets': 18,
        'created_at': '2026-10-19T09:45:00Z',
        'category': 'FI-Forum 2026',
        'sentiment': 'positive',
        'severity': 'low',
        'confidence': 0.93,
        'summary': 'LinkedIn post discussing FI-Forum 2026 and banking innovation topics',
        'sarcasm_detected': False,
        'mentioned_speakers': ['Maurice Veenendaal'],
        'themes': ['Banking Innovation', 'Digital Transformation', 'FI-Forum 2026']
    },
]

DEMO_SUMMARY = {
    'total_mentions': 3,
    'event_name': 'FI-Forum 2026',
    'event_location': 'Frankfurt am Main',
    'event_date': '2026-11-03 to 2026-11-05',
    'timestamp': '2026-10-22T12:00:50Z',
    'sentiment_breakdown': {
        'positive': 3,
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
        'LinkedIn': 2,
        'Instagram': 1,
        'Twitter': 0,
        'News': 0,
        'TikTok': 0
    },
    'top_themes': [
        'FI-Forum 2026',
        'Banking Innovation',
        'Digital Transformation',
        'Finanzinformatik',
        'Networking'
    ],
    'critical_mentions_count': 0,
    'average_engagement': {
        'likes': 174,
        'shares': 17
    }
}

def get_demo_data():
    """Return demo data for dashboard"""
    df = pd.DataFrame(DEMO_MENTIONS)
    return df, DEMO_SUMMARY
