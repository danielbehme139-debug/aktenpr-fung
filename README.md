# Inkasso-Aktenprüfung

Ein erstes, bewusst einfaches Lern- und Entwicklungsprojekt zur strukturierten Prüfung von Forderungsakten.

## Stand 0.1 – Prototyp

- Geführte Prüfung über die Konsole
- Beispielhafte Prüfschritte: Datenlage, Hauptforderung, Nebenforderungen, Verjährungsprüfung, Titel und Wirtschaftlichkeit
- Ausgabe einer **unverbindlichen Prüfempfehlung** mit Begründung
- Automatisierte Tests ohne zusätzliche Bibliotheken

## Start

Voraussetzung: Python 3.10 oder neuer.

```bash
python app.py
```

Unter Windows funktioniert häufig auch `py app.py`.

Tests starten:

```bash
python -m unittest discover -s tests -v
```

## Wichtige Hinweise

**Nur für Entwicklung und Demonstration.** Es werden keine echten Schuldner- oder Kundendaten benötigt oder gespeichert. Bitte ausschließlich frei erfundene Testfälle verwenden.

Die Regeln bilden **keine vollständige rechtliche Prüfung** ab. Insbesondere können Verjährung, Titulierung, Nebenforderungen, Datenschutz, Anspruchsgrundlagen und Wirtschaftlichkeit nur anhand des konkreten Sachverhalts und der geltenden Rechtslage fachlich geprüft werden. Die Anwendung trifft keine Entscheidungen und leitet keine Maßnahmen ein.

Dieses Projekt ist **nicht mit betrieblichen Systemen verbunden**.

## Nächste Schritte

1. Eine übersichtliche Benutzeroberfläche ergänzen.
2. Regelwerk und Prüfschritte fachlich definieren und überprüfen.
3. Weitere Testfälle einschließlich unvollständiger und widersprüchlicher Angaben ergänzen.
4. Datenschutz- und Zugriffskonzept prüfen, bevor jemals reale Daten verarbeitet werden.
