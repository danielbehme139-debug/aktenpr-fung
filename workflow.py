"""Nachvollziehbare Demonstrationsregeln; keine rechtliche Entscheidung."""
from dataclasses import dataclass
from enum import Enum


class Antwort(str, Enum):
    JA = "Ja"
    NEIN = "Nein"
    UNBEKANNT = "Unbekannt"


@dataclass(frozen=True)
class Frage:
    key: str
    text: str
    erwartet: Antwort | None = None


PHASEN = (
    ("Akteneinsicht und Datenprüfung", (
        Frage("unterlagen", "Sind alle notwendigen Unterlagen vorhanden?", Antwort.JA),
        Frage("stammdaten", "Sind die Stammdaten vollständig?", Antwort.JA),
        Frage("identitaet", "Ist die Identität bzw. Zuordnung des Schuldners ausreichend geprüft?", Antwort.JA),
        Frage("datenschutz", "Liegen datenschutzrechtliche Bedenken vor?", Antwort.NEIN),
        Frage("widersprueche", "Bestehen Unklarheiten oder Widersprüche?", Antwort.NEIN),
    )),
    ("Forderungs- und Zahlungsprüfung", (
        Frage("hauptforderung", "Ist die Hauptforderung noch offen?"),
        Frage("nebenforderungen", "Sind Nebenforderungen offen?"),
        Frage("zahlungen", "Sind Zahlungseingänge vollständig geprüft und korrekt verbucht?", Antwort.JA),
        Frage("letzte_zahlung", "Wurde die letzte Zahlung geprüft (bzw. das Fehlen von Zahlungen bestätigt)?", Antwort.JA),
        Frage("differenzen", "Bestehen ungeklärte Differenzen im Forderungskonto?", Antwort.NEIN),
    )),
    ("Rechtliche Prüfung", (
        Frage("titel", "Ist ein Vollstreckungstitel vorhanden?"),
        Frage("verjaehrung", "Ist die Verjährungsprüfung erfolgt?", Antwort.JA),
        Frage("risiko", "Besteht ein mögliches Verjährungsrisiko?", Antwort.NEIN),
        Frage("einwendungen", "Sind Einwendungen oder Einreden bekannt?", Antwort.NEIN),
        Frage("insolvenz", "Gibt es Hinweise auf ein Insolvenzverfahren?", Antwort.NEIN),
    )),
    ("Wirtschaftlichkeit", (
        Frage("wirtschaftlichkeit", "Wurde die Wirtschaftlichkeit geprüft?", Antwort.JA),
        Frage("bonitaet", "Ist eine Bonitätsprüfung erfolgt?", Antwort.JA),
        Frage("zahlungsfaehigkeit", "Liegen verwertbare Informationen über die Zahlungsfähigkeit vor?", Antwort.JA),
        Frage("vereinbarung", "Ist eine freiwillige Zahlungsvereinbarung denkbar?"),
        Frage("massnahmen", "Sind weitere Maßnahmen wirtschaftlich sinnvoll?", Antwort.JA),
    )),
)
FRAGEN = tuple(f for _, fragen in PHASEN for f in fragen)


@dataclass(frozen=True)
class Pruefhinweis:
    ergebnis: str
    begruendung: tuple[str, ...]
    offene_punkte: tuple[str, ...]
    schritte: tuple[str, ...]


def pruefe(angaben: dict[str, str]) -> Pruefhinweis:
    """Fehlende, unbekannte und ungültige Antworten bleiben offen."""
    gruende, offen = [], []
    for f in FRAGEN:
        wert = angaben.get(f.key)
        if wert not in (Antwort.JA, Antwort.NEIN):
            offen.append(f"{f.text} — noch zu klären")
        elif f.erwartet is not None and wert != f.erwartet:
            offen.append(f"{f.text} — {wert}; fachliche Klärung erforderlich")
        if wert in (Antwort.JA, Antwort.NEIN):
            gruende.append(f"{f.text} — {wert}")
    if offen:
        return Pruefhinweis("Manuelle Sachbearbeiterprüfung erforderlich", tuple(gruende), tuple(offen), (
            "Offene Punkte und Belege fachlich klären und dokumentieren.",
            "Angaben anschließend korrigieren und die Prüfung erneut ansehen.",
            "Bis zur Klärung keine abschließende Empfehlung für ein gerichtliches Mahnverfahren ableiten.",
        ))
    if angaben["hauptforderung"] == Antwort.NEIN:
        if angaben["nebenforderungen"] == Antwort.JA:
            titel, schritte = "Abrechnung prüfen", ("Nebenforderungen, Anspruchsgrundlagen und Kostenaufstellung fachlich prüfen.", "Zahlungen und Saldo abgleichen.")
        else:
            titel, schritte = "Aktenabschluss prüfen", ("Nullsaldo, Buchungen und Abschlussvoraussetzungen kontrollieren.", "Aufbewahrungs- und Dokumentationspflichten fachlich klären.")
    elif angaben["titel"] == Antwort.JA:
        titel, schritte = "Bestehenden Titel und Vollstreckungsmöglichkeiten prüfen", ("Titelumfang, Zustellung und Vollstreckbarkeit fachlich prüfen.", "Zahlungen, Insolvenzlage und Verhältnismäßigkeit möglicher Schritte erneut prüfen.")
    else:
        titel, schritte = "Gerichtliches Mahnverfahren prüfen", ("Anspruch und sämtliche Verfahrensvoraussetzungen fachlich prüfen.", "Zuständige Person entscheidet über das weitere Vorgehen; keine automatische Einleitung.")
    if angaben["vereinbarung"] == Antwort.JA:
        schritte += ("Möglichkeit einer freiwilligen Zahlungsvereinbarung fachlich besprechen.",)
    return Pruefhinweis(titel, tuple(gruende), (), schritte)


def beispielakte() -> dict[str, str]:
    """Ausschließlich erfundener Fall: offene Hauptforderung ohne Titel."""
    return {f.key: (f.erwartet or Antwort.NEIN).value for f in FRAGEN} | {
        "hauptforderung": "Ja", "vereinbarung": "Ja"
    }
