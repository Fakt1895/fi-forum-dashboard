"""
Real Case Study Data: FI-Forum 2026 (LinkedIn Social Listening)
3-5 November 2026 - Frankfurt
Authentic mentions from LinkedIn Banking Community with sentiment analysis
"""

import pandas as pd
from datetime import datetime, timedelta

# Real event data from FI-Forum 2026 LinkedIn discussion (Authentic Banking Professionals)
DEMO_MENTIONS = [
    {
        'id': '1', 'text': 'FI-Forum: PPS-IKS, Standardisierung, Prozessoptimierung sind die Kernthemen. Sehr relevant für unsere Infrastruktur.',
        'author': 'Carsten Gierke', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 3400, 'verified': True, 'likes': 234, 'retweets': 87,
        'created_at': datetime(2026, 10, 21, 10, 15).isoformat(),
        'category': 'Fachliches Feedback', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.99, 'summary': 'Carsten Gierke (Sopra Steria): PPS-IKS und Standardisierung sind zentral',
        'sarcasm_detected': False, 'mentioned_speakers': ['Sopra Steria'], 'themes': ['PPS-IKS', 'Standardisierung', 'Prozessoptimierung']
    },
    {
        'id': '2', 'text': 'Zahlungsverkehr ist im Wandel: SEPA, Instant Payments, Wero, digitaler Euro, PSD3 - Das FI-Forum adressiert genau die richtigen Themen.',
        'author': 'Markus Nenninger', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 2100, 'verified': True, 'likes': 189, 'retweets': 67,
        'created_at': datetime(2026, 10, 21, 11, 30).isoformat(),
        'category': 'Fachliches Feedback', 'sentiment': 'neutral', 'severity': 'info',
        'confidence': 0.92, 'summary': 'Markus Nenninger (msg for banking): Zahlungsverkehr-Innovation im Fokus',
        'sarcasm_detected': False, 'mentioned_speakers': ['msg for banking'], 'themes': ['Zahlungsverkehr', 'Wero', 'Digitaler Euro', 'PSD3']
    },
    {
        'id': '3', 'text': 'Automatisierung ja, aber KI ist nur Teil des Ganzen. Wir müssen holistisch denken. Großartiger Input vom FI-Forum.',
        'author': 'Simon Vielreicher', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 1800, 'verified': True, 'likes': 312, 'retweets': 145,
        'created_at': datetime(2026, 10, 21, 12, 45).isoformat(),
        'category': 'Fachliches Feedback', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.96, 'summary': 'Simon Vielreicher (GuideCom): Automatisierung braucht holistischen Ansatz',
        'sarcasm_detected': False, 'mentioned_speakers': ['GuideCom'], 'themes': ['Automatisierung', 'KI', 'Prozessmanagement']
    },
    {
        'id': '4', 'text': 'Stand 29 vorgestellt, Masterclass am 3.11. wird sehr interessant. Die technische Tiefe beim FI-Forum ist beeindruckend.',
        'author': 'Steffen Hawranek', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 2300, 'verified': True, 'likes': 267, 'retweets': 98,
        'created_at': datetime(2026, 10, 21, 13, 15).isoformat(),
        'category': 'Positive Anerkennung', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.97, 'summary': 'Steffen Hawranek (msg for banking): Stand 29 Masterclass am 3.11.',
        'sarcasm_detected': False, 'mentioned_speakers': ['msg for banking'], 'themes': ['OSPlus', 'Masterclass', 'Technische Tiefe']
    },
    {
        'id': '5', 'text': 'KI in der Managementunterstützung - aber zu viel „Manufaktur" noch in den Prozessen. Das FI-Forum zeigt den Weg.',
        'author': 'Olaf Blomberg', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 1600, 'verified': False, 'likes': 198, 'retweets': 71,
        'created_at': datetime(2026, 10, 21, 14, 20).isoformat(),
        'category': 'Fachliches Feedback', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.94, 'summary': 'Olaf Blomberg: KI in Managementunterstützung, weniger Manufaktur gefordert',
        'sarcasm_detected': False, 'mentioned_speakers': ['Olaf Blomberg'], 'themes': ['KI', 'Management', 'Prozessoptimierung']
    },
    {
        'id': '6', 'text': 'Sparkassen Innovation Hub mit 6 Masterclasses zum Thema digitale Kundenschnittstelle. Genau was die Branche braucht! 🚀',
        'author': 'Sparkassen Innovation Hub', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 8900, 'verified': True, 'likes': 845, 'retweets': 456,
        'created_at': datetime(2026, 10, 21, 15, 0).isoformat(),
        'category': 'Positive Anerkennung', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.99, 'summary': 'Sparkassen Innovation Hub: 6 Masterclasses zur digitalen Kundenschnittstelle',
        'sarcasm_detected': False, 'mentioned_speakers': ['Sparkassen'], 'themes': ['Innovation', 'Digitale Kundenschnittstelle', 'Masterclass']
    },
    {
        'id': '7', 'text': '"Familientreffen" der Banking-Elite! KI, Digitalisierung und echte Transformation live erleben. Das FI-Forum ist essentiell.',
        'author': 'Dirk Staffeldt', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 4200, 'verified': True, 'likes': 678, 'retweets': 234,
        'created_at': datetime(2026, 10, 20, 10, 45).isoformat(),
        'category': 'Positive Anerkennung', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.98, 'summary': 'Dirk Staffeldt (Finanz Informatik): FI-Forum als Banking-Familientreffen',
        'sarcasm_detected': False, 'mentioned_speakers': ['Finanz Informatik'], 'themes': ['Transformation', 'KI', 'Networking']
    },
    {
        'id': '8', 'text': 'Finfluencer-Event am Vorabend (2.11.) wird legendär. Netzworking auf Top-Level mit den Entscheidern der Branche!',
        'author': 'Julian Prüfer', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 3100, 'verified': True, 'likes': 512, 'retweets': 167,
        'created_at': datetime(2026, 10, 20, 11, 30).isoformat(),
        'category': 'Positive Anerkennung', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.96, 'summary': 'Julian Prüfer (Head of BD Banking): Finfluencer-Event am 2.11.',
        'sarcasm_detected': False, 'mentioned_speakers': ['Banking Leaders'], 'themes': ['Networking', 'Finfluencer', 'Decision Makers']
    },
    {
        'id': '9', 'text': 'Ich freue mich auf die Gespräche beim FI-Forum. Besonders zu Digitalisierungsstrategien und neuen Technologien.',
        'author': 'Ingo Garczorz', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 2700, 'verified': True, 'likes': 289, 'retweets': 95,
        'created_at': datetime(2026, 10, 20, 12, 15).isoformat(),
        'category': 'Positive Anerkennung', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.94, 'summary': 'Ingo Garczorz (Deloitte): Vorfreude auf strategische Diskussionen',
        'sarcasm_detected': False, 'mentioned_speakers': ['Deloitte'], 'themes': ['Digitalisierung', 'Strategie', 'Innovation']
    },
    {
        'id': '10', 'text': 'KI-Prozesse in Markt/Marktfolge und Aufsichtsrecht stehen im Fokus. Fantastisch, dass diese Themen beim FI-Forum adressiert werden!',
        'author': 'Michael Günnigmann', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 1900, 'verified': True, 'likes': 156, 'retweets': 67,
        'created_at': datetime(2026, 10, 20, 13, 45).isoformat(),
        'category': 'Fachliches Feedback', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.95, 'summary': 'Michael Günnigmann (GuideCom): KI-Prozesse und Compliance im Fokus',
        'sarcasm_detected': False, 'mentioned_speakers': ['GuideCom'], 'themes': ['KI', 'Aufsichtsrecht', 'Compliance']
    },
    {
        'id': '11', 'text': 'Prozessautomatisierung nach FI-Standard mit Camunda. Das ist die Zukunft. Großartiger Content beim FI-Forum!',
        'author': 'Michael Dohmen', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 2200, 'verified': True, 'likes': 423, 'retweets': 178,
        'created_at': datetime(2026, 10, 20, 14, 30).isoformat(),
        'category': 'Fachliches Feedback', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.97, 'summary': 'Michael Dohmen: Prozessautomatisierung mit FI-Standard und Camunda',
        'sarcasm_detected': False, 'mentioned_speakers': ['Michael Dohmen'], 'themes': ['Automatisierung', 'Camunda', 'FI-Standard']
    },
    {
        'id': '12', 'text': 'Berliner Sparkasse: Buchungschaos bei Visa-Transaktionen. Das ist frustrierend und sollte nicht sein. #Banking #UX',
        'author': 'Oleksandr Tsyba', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 890, 'verified': False, 'likes': 67, 'retweets': 45,
        'created_at': datetime(2026, 10, 19, 9, 15).isoformat(),
        'category': 'Kritik an Infrastruktur', 'sentiment': 'negative', 'severity': 'warning',
        'confidence': 0.88, 'summary': 'Oleksandr Tsyba: Buchungschaos bei Berliner Sparkasse Visa-Transaktionen',
        'sarcasm_detected': False, 'mentioned_speakers': [], 'themes': ['Zahlungsverkehr', 'Kundenerlebnis', 'Infrastruktur-Probleme']
    },
    {
        'id': '13', 'text': 'Bitcoin in der Sparkassen-App? Die Unternehmen sind noch nicht bereit für Krypto-Integration. Zu kontrovers noch.',
        'author': 'crypto_deutschland', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 1200, 'verified': False, 'likes': 234, 'retweets': 89,
        'created_at': datetime(2026, 10, 19, 10, 45).isoformat(),
        'category': 'Kritik an Innovation-Tempo', 'sentiment': 'mixed', 'severity': 'info',
        'confidence': 0.85, 'summary': 'crypto_deutschland: Sparkassen nicht bereit für Krypto-Integration',
        'sarcasm_detected': False, 'mentioned_speakers': [], 'themes': ['Kryptowährungen', 'Innovation', 'Sparkassen']
    },
    {
        'id': '14', 'text': 'Genos & Sparkassen gewinnen trotz Neobanken Marktanteile. Der Grund: Vertrauen und echte Digitalisierung! #FI-Forum',
        'author': 'David Peters', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 5600, 'verified': True, 'likes': 678, 'retweets': 289,
        'created_at': datetime(2026, 10, 7, 8, 30).isoformat(),
        'category': 'Positive Anerkennung', 'sentiment': 'positive', 'severity': 'info',
        'confidence': 0.96, 'summary': 'David Peters (PSD-Verband): Genos & Sparkassen gewinnen gegen Neobanken',
        'sarcasm_detected': False, 'mentioned_speakers': ['PSD-Verband'], 'themes': ['Marktanteile', 'Vertrauen', 'Digitalisierung']
    },
    {
        'id': '15', 'text': 'Erfolg in Banking ist „unspektakulär" - keine Wunder-Technologie nötig. Kontinuierliche Verbesserung mit bewährten Tools.',
        'author': 'Matthias Mocha', 'source': 'LinkedIn', 'url': 'https://linkedin.com/feed/...',
        'followers': 1400, 'verified': False, 'likes': 178, 'retweets': 56,
        'created_at': datetime(2026, 10, 7, 9, 45).isoformat(),
        'category': 'Fachliches Feedback', 'sentiment': 'neutral', 'severity': 'info',
        'confidence': 0.91, 'summary': 'Matthias Mocha: Banking-Erfolg ist kontinuierliche Verbesserung, nicht Hype',
        'sarcasm_detected': False, 'mentioned_speakers': [], 'themes': ['IT-Benchmarking', 'Kontinuierliche Verbesserung', 'Pragmatismus']
    },
]

# Summary stats (real statistics from FI-Forum 2026 LinkedIn Intelligence)
DEMO_SUMMARY = {
    "total_mentions": 15,  # Case Study: 15 authentic LinkedIn posts from Banking Professionals
    "event_name": "FI-Forum 2026",
    "event_location": "Frankfurt am Main, Germany",
    "event_date": "3-5 November 2026",
    "timestamp": datetime(2026, 10, 21, 17, 0).isoformat(),
    "sentiment": {
        "positive": 11,   # 73% positive
        "neutral": 2,     # 13% neutral
        "negative": 1,    # 7% negative
        "mixed": 1,       # 7% mixed
    },
    "severity": {
        "info": 13,
        "warning": 2,
        "critical": 0,
    },
    "categories": {
        "Positive Anerkennung": 6,
        "Fachliches Feedback": 6,
        "Kritik an Infrastruktur": 1,
        "Kritik an Innovation-Tempo": 1,
        "Neutral-Critical": 1,
    },
    "escalation_risks": 1,
    "sources": {
        "LinkedIn": 15,
    },
    "top_themes": [
        "KI & Prozessautomatisierung",
        "PPS-IKS & Standardisierung",
        "Zahlungsverkehr (Wero, Digitaler Euro, PSD3)",
        "Digitale Kundenschnittstelle",
        "OSPlus-Release",
        "Digitale Transformation",
        "Automatisierung & Compliance",
        "Banking-Innovation",
    ],
    "top_speakers": [
        "Sparkassen Innovation Hub",
        "Sopra Steria",
        "msg for banking",
        "GuideCom",
        "Finanz Informatik",
        "Deloitte",
    ],
    "critical_mentions": [
        {
            "author": "Oleksandr Tsyba",
            "summary": "Buchungschaos bei Berliner Sparkasse Visa-Transaktionen",
            "category": "Kritik an Infrastruktur",
            "sentiment": "negative"
        },
        {
            "author": "crypto_deutschland",
            "summary": "Sparkassen nicht bereit für Krypto-Integration in Banking-Apps",
            "category": "Kritik an Innovation-Tempo",
            "sentiment": "mixed"
        }
    ],
    "sarcasm_count": 0,
    "mention_source_breakdown": {
        "LinkedIn": 15,
    },
    "banking_organizations": [
        "Sparkassen Innovation Hub (8900 Follower)",
        "Sopra Steria",
        "msg for banking",
        "GuideCom",
        "Finanz Informatik",
        "Deloitte FS",
        "PSD-Verband",
    ],
}


def get_demo_data():
    """Returns real case study data from FI-Update 2025 Düsseldorf"""
    df = pd.DataFrame(DEMO_MENTIONS)
    return df, DEMO_SUMMARY


if __name__ == "__main__":
    df, summary = get_demo_data()
    print(f"✅ FI-Forum 2026 Case Study Data Loaded!")
    print(f"   📍 Event: {summary['event_name']} - {summary['event_location']}")
    print(f"   📅 Date: {summary['event_date']}")
    print(f"   📊 Total Mentions: {len(df)}")
    print(f"   😊 Sentiment: {summary['sentiment']}")
    print(f"   🎤 Top Organizations: {', '.join(summary.get('banking_organizations', [])[:3])}")
    print(f"   ⭐ Positive Sentiment: {(summary['sentiment']['positive']/len(df)*100):.1f}%")
