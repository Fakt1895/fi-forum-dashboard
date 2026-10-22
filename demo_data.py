"""
FI-Forum 2026 Social Listening - verifizierte Beiträge

Jeder Eintrag wurde am 22.10.2026 im Browser geöffnet und geprüft.
- url:        echte öffentliche LinkedIn-Post-URL (vom Kunden anklickbar)
- created_at: exakter Zeitstempel, aus der LinkedIn-Post-ID berechnet
- likes:      Reaktionen zum Zeitpunkt der Prüfung (22.10.2026, ca. 21 Uhr)
- comments:   Kommentare zum Zeitpunkt der Prüfung
- sentiment / confidence / severity: Einordnung der Analyse (keine LinkedIn-Daten)
"""

import pandas as pd
from collections import Counter

VERIFIED_AT = "2026-10-22T19:20:00Z"

DEMO_MENTIONS = [
    {
        'id': 'li_7519089658115461120',
        'author': 'Claudia Theisen',
        'author_title': 'Geschäftsführerin, PROSERV!CE Dienstleistungsgesellschaft mbH',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/posts/claudia-theisen-19a114373_ich-bin-dabei-fi-forum-2026-in-frankfurt-share-7519089658115461120-hjSH/',
        'text': 'Ich bin dabei – FI-Forum 2026 in Frankfurt 📢. Vom 3. bis 5. November findet Ihr mich am Gemeinschaftsstand 45 des S-Dienstleister-Netzwerks.',
        'created_at': '2026-10-22T17:37:52Z',
        'likes': 8, 'comments': 2,
        'category': 'Aussteller / Teilnahme',
        'sentiment': 'positive', 'confidence': 0.95, 'severity': 'low',
        'summary': 'Kündigt Präsenz am Gemeinschaftsstand 45 des S-Dienstleister-Netzwerks an.',
        'themes': ['Teilnahme', 'Aussteller', 'S-Dienstleister-Netzwerk'],
        'verified': True,
    },
    {
        'id': 'li_7519072404950814720',
        'author': 'Dr. André Krapat',
        'author_title': 'Partner/Gesellschafter, Berg Lund & Company',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/posts/dr-andr%C3%A9-krapat_in-weniger-als-zwei-wochen-ist-es-so-weit-share-7519072404950814720-ugJh/',
        'text': 'In weniger als zwei Wochen ist es so weit: Ich freue mich auf zahlreiche Gespräche, spannende Vorträge und das eine oder andere Wiedersehen beim FI-Forum in Frankfurt!',
        'created_at': '2026-10-22T16:29:18Z',
        'likes': 20, 'comments': 0,
        'category': 'Vorfreude / Networking',
        'sentiment': 'positive', 'confidence': 0.97, 'severity': 'low',
        'summary': 'Vorfreude auf Gespräche, Vorträge und Wiedersehen.',
        'themes': ['Networking', 'Vorträge'],
        'verified': True,
    },
    {
        'id': 'li_7519060567702241280',
        'author': 'Igor Tolo',
        'author_title': 'Regionaldirektor, FORUM Direktfinanz GmbH & Co. KG',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/posts/igor-tolo-976622277_wer-ist-beim-fi-forum-dabei-ich-freue-share-7519060567702241280-lv2n/',
        'text': 'Wer ist beim FI-Forum dabei? 👋 Ich freue mich auf persönliche Gespräche rund um die Baufinanzierung – und auf bekannte wie neue Gesichter! 📍 3.–5. November | Frankfurt | Halle 5.1, Stand 4',
        'created_at': '2026-10-22T15:42:16Z',
        'likes': 9, 'comments': 1,
        'category': 'Aussteller / Teilnahme',
        'sentiment': 'positive', 'confidence': 0.94, 'severity': 'low',
        'summary': 'Lädt zu Gesprächen über Baufinanzierung ein (Halle 5.1, Stand 4).',
        'themes': ['Baufinanzierung', 'Aussteller', 'Networking'],
        'verified': True,
    },
    {
        'id': 'li_7519060275392786432',
        'author': 'Daniel Bromberger',
        'author_title': 'Regionaldirektor, FORUM Direktfinanz GmbH & Co. KG',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/posts/daniel-bromberger-650032259_fiforum2026-sparkassen-baufinanzierung-share-7519060275392786432-IXFK/',
        'text': 'Sehen wir uns auf dem FI-Forum 2026 in Frankfurt? 🤝 Das FI-Forum ist einer der wichtigsten Treffpunkte der Sparkassen-Finanzgruppe: Über 10.000 Kolleginnen und Kollegen kommen zusammen, um sich über Digitalisierung, Innovation und neue Projekte auszutauschen.',
        'created_at': '2026-10-22T15:41:07Z',
        'likes': 5, 'comments': 1,
        'category': 'Aussteller / Teilnahme',
        'sentiment': 'positive', 'confidence': 0.96, 'severity': 'low',
        'summary': 'Betont Bedeutung des FI-Forums für die Sparkassen-Finanzgruppe; freut sich auf Keynotes und Masterclasses.',
        'themes': ['Digitalisierung', 'Sparkassen-Finanzgruppe', 'Baufinanzierung'],
        'verified': True,
    },
    {
        'id': 'li_7519006085400408064',
        'author': 'Finanz Informatik',
        'author_title': 'Unternehmensseite (Veranstalter)',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/posts/die-neue-ausgabe-des-fi-magazins-ist-da-ugcPost-7519006085400408064-hM7e/',
        'text': 'Die neue Ausgabe des FI-Magazins ist da! Alles zum FI-Forum 2026 und natürlich viele weitere News, Lösungen und Praxisbeispiele. – FI-Magazin 3/2026 mit Schwerpunkt FI-Forum 2026, Interview zur Baufinanzierungsberatung, App Sparkasse 9.0',
        'created_at': '2026-10-22T12:05:47Z',
        'likes': 21, 'comments': 0,
        'category': 'Veranstalter-Kommunikation',
        'sentiment': 'positive', 'confidence': 0.93, 'severity': 'low',
        'summary': 'Veranstalter bewirbt FI-Magazin 3/2026 mit Schwerpunkt FI-Forum.',
        'themes': ['FI-Magazin', 'App Sparkasse 9.0', 'Baufinanzierung'],
        'verified': True,
    },
    {
        'id': 'li_7518584339824214016',
        'author': 'Finanz Informatik',
        'author_title': 'Unternehmensseite (Veranstalter)',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/posts/heimvorteil-share-7518584339824214016-zF60/',
        'text': 'Die FI-Forum Event-App ist startklar! Jetzt downloaden 🚀 Lade dir die App zum FI-Forum 2026 jetzt auf dein Smartphone. Die Event-App hilft dir bei der Orientierung … #Heimvorteil',
        'created_at': '2026-10-21T08:09:55Z',
        'likes': 72, 'comments': 0,
        'category': 'Veranstalter-Kommunikation',
        'sentiment': 'positive', 'confidence': 0.95, 'severity': 'low',
        'summary': 'Launch der offiziellen FI-Forum-Event-App (Agenda, Orientierung).',
        'themes': ['Event-App', 'Heimvorteil', 'Orientierung'],
        'verified': True,
    },
    {
        'id': 'li_7517958910897614848',
        'author': 'Tobias Mallmann',
        'author_title': 'Business Unit Manager, Fincon Reply GmbH',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/posts/tobias-mallmann-0318451b7_finconreply-fiforum2026-sparkassen-share-7517958910897614848-_PiS/',
        'text': 'Ich bin beim FI-Forum 2026 dabei! Gemeinsam mit meinen Kollegen von Fincon Reply GmbH freue ich mich auf den persönlichen Austausch darüber, wie wir die Digitalisierung in der Sparkassen-Finanzgruppe konkret voranbringen. Besuchen Sie uns an Stand 18.',
        'created_at': '2026-10-19T14:44:41Z',
        'likes': 45, 'comments': 4,
        'category': 'Aussteller / Teilnahme',
        'sentiment': 'positive', 'confidence': 0.96, 'severity': 'low',
        'summary': 'Fincon Reply an Stand 18 – Fokus Prozessdigitalisierung in Sparkassen.',
        'themes': ['Digitalisierung', 'Prozessoptimierung', 'Aussteller'],
        'verified': True,
    },
    {
        'id': 'li_7514312655428345857',
        'author': 'Finanz Informatik',
        'author_title': 'Unternehmensseite (Veranstalter)',
        'source': 'LinkedIn',
        'url': 'https://www.linkedin.com/posts/anmeldung-masterclasses-workshops-und-side-ugcPost-7514312655428345857-NRHD/',
        'text': 'Wissen vertiefen. Perspektiven erweitern. Heimvorteil nutzen. 🚀 Es geht einen Schritt weiter Richtung FI-Forum 2026: Die Anmeldung für unsere Masterclasses, Workshops und Side Events ist ab sofort geöffnet!',
        'created_at': '2026-10-09T13:15:46Z',
        'likes': 7, 'comments': 0,
        'category': 'Veranstalter-Kommunikation',
        'sentiment': 'positive', 'confidence': 0.92, 'severity': 'low',
        'summary': 'Anmeldung für Masterclasses, Workshops und Side Events geöffnet.',
        'themes': ['Masterclasses', 'Workshops', 'Heimvorteil'],
        'verified': True,
    },
]


def _build_summary(mentions):
    sent = Counter(m['sentiment'] for m in mentions)
    sev = Counter(m['severity'] for m in mentions)
    themes = Counter(t for m in mentions for t in m['themes'])
    return {
        'total_mentions': len(mentions),
        'event_name': 'FI-Forum 2026',
        'event_location': 'Messe Frankfurt',
        'event_date': '2026-11-03 bis 2026-11-05',
        'verified_at': VERIFIED_AT,
        'sentiment': {
            'positive': sent.get('positive', 0),
            'neutral': sent.get('neutral', 0),
            'negative': sent.get('negative', 0),
        },
        'severity': {
            'info': sev.get('low', 0),
            'warning': sev.get('warning', 0),
            'critical': sev.get('critical', 0),
        },
        'sources': dict(Counter(m['source'] for m in mentions)),
        'categories': dict(Counter(m['category'] for m in mentions)),
        'top_themes': [t for t, _ in themes.most_common(10)],
        'critical_mentions': [m for m in mentions if m['severity'] == 'critical'],
        'total_reactions': sum(m['likes'] for m in mentions),
        'total_comments': sum(m['comments'] for m in mentions),
    }


DEMO_SUMMARY = _build_summary(DEMO_MENTIONS)


def get_demo_data():
    """Return verified data for dashboard"""
    return pd.DataFrame(DEMO_MENTIONS), DEMO_SUMMARY
