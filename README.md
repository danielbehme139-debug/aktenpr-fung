# Inkasso-Aktenprüfung

Lokale Demonstration einer geführten Inkasso-Aktenprüfung mit Python und Streamlit.
Nur erfundene Daten verwenden. Keine Rechtsberatung und keine automatische Entscheidung.

## Installation für Einsteiger

Voraussetzung: Python 3.10 oder neuer. Laden Sie das Repository herunter und öffnen
Sie ein Terminal im Projektordner (dort, wo `requirements.txt` liegt).

```bash
python -m venv .venv
```

Virtuelle Umgebung aktivieren:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows Eingabeaufforderung: `.venv\Scripts\activate.bat`
- macOS / Linux: `source .venv/bin/activate`

Falls Windows `python` nicht erkennt, verwenden Sie zum Anlegen der Umgebung `py`.
Falls PowerShell die Aktivierung blockiert, verwenden Sie die Eingabeaufforderung.

Danach installieren und starten:

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Öffnen Sie im eigenen Browser `http://127.0.0.1:8501`. Zum Beenden im Terminal
`Strg+C` drücken. Die Konfiguration bindet den Server ausschließlich an den lokalen
Rechner und schaltet Streamlit-Nutzungsstatistiken aus. Für die Installation wird
Internet benötigt; die Anwendung benötigt weder externe API noch Datenbank.

## Bedienung

1. Eine neue Aktenprüfung beginnen oder die vollständig erfundene Beispielakte laden.
2. Vier Eingabephasen mit jeweils fünf Fragen durchlaufen. „Nein“ bei der offenen
   Hauptforderung bedeutet vollständig ausgeglichen. Ohne Zahlungseingänge erst
   deren Fehlen fachlich bestätigen, bevor die letzte Zahlung als geprüft gilt.
3. „Ja“, „Nein“ oder ausdrücklich „Unbekannt“ auswählen. Fehlende Antworten werden
   angezeigt; unbekannte Antworten erlauben das Weitergehen und bleiben offen.
4. Phase fünf zeigt Ergebnis, Gründe, offene Punkte und mögliche nächste Schritte.
5. Unter „Alle Eingaben prüfen und korrigieren“ einzelne Phasen erneut bearbeiten.
   „Neue Aktenprüfung“ verwirft die bisherigen Angaben dieser Sitzung.

Die fünf möglichen Prüfhinweise sind Aktenabschluss, Abrechnung, gerichtliches
Mahnverfahren, bestehender Titel/Vollstreckungsmöglichkeiten und manuelle Prüfung.
Unbekannte, fehlende oder kritische Angaben haben Vorrang und führen zur manuellen
Prüfung. Ohne geklärte Verjährung erscheint kein Mahnverfahrenshinweis. Bei offener
Hauptforderung berücksichtigt die Anwendung einen vorhandenen Titel.

## Konsole und Tests

Die bisherige Konsolenanwendung bleibt unverändert verfügbar:

```bash
python app.py
python -m unittest discover -s tests -v
```

`pruefung.py` enthält die ursprüngliche boolesche Konsolenlogik. `workflow.py`
enthält die erweiterte, dreistufige Prüfstruktur unabhängig von Streamlit.
`streamlit_app.py` ist ausschließlich für die Oberfläche zuständig. Tests decken
alle Ergebnispfade, unbekannte/kritische Angaben sowie Navigation und Korrekturen ab.

## Bekannte Einschränkungen

- Demonstrationsregeln, keine vollständige rechtliche oder wirtschaftliche Prüfung.
  Es werden weder Fristen berechnet noch Titel, Belege oder Anspruchsgrundlagen geprüft.
- Die ursprüngliche Konsole unterstützt weiterhin nur Ja/Nein und weniger Fragen.
- Bewusst konservativ: Auch bei ausgeglichener Forderung führen offene Fragen in
  anderen Phasen zunächst zur manuellen Prüfung.
- Keine dauerhafte Speicherung, Anmeldung, Aktenverwaltung, Dateiimporte oder Exporte.
  Angaben liegen nur im flüchtigen Streamlit-Sitzungsspeicher; ein Neuladen oder
  Verbindungsabbruch kann sie verwerfen. Es werden keine personenbezogenen Felder erhoben.
- Keine Buchungen, kein Versand, keine Einleitung rechtlicher Maßnahmen.
- Responsive Standardkomponenten; reale Tablet- und Barrierefreiheitstests stehen aus.
- Vor produktiver Nutzung sind fachliche, rechtliche, sicherheitstechnische und
  datenschutzrechtliche Prüfung sowie ein Zugriffskonzept erforderlich.
