"""Demonstrationslogik für eine unverbindliche Aktenprüfung.

Keine Rechtsberatung und keine automatische Forderungsentscheidung.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Akte:
    unterlagen_vollstaendig: bool
    hauptforderung_offen: bool
    nebenforderungen_offen: bool
    verjaehrung_geprueft: bool
    verjaehrungsrisiko: bool
    titel_vorhanden: bool
    wirtschaftlichkeit_geprueft: bool


@dataclass(frozen=True)
class Ergebnis:
    empfehlung: str
    begruendung: str


def pruefe_akte(akte: Akte) -> Ergebnis:
    """Ermittelt einen PrüfhINWEIS; ersetzt niemals die fachliche Entscheidung."""
    if not akte.unterlagen_vollstaendig:
        return Ergebnis("Manuelle Prüfung", "Unterlagen oder Stammdaten sind unvollständig.")
    if not akte.verjaehrung_geprueft:
        return Ergebnis("Manuelle Prüfung", "Verjährungsprüfung ist noch offen.")
    if akte.verjaehrungsrisiko:
        return Ergebnis("Manuelle Prüfung", "Mögliches Verjährungsrisiko erfordert fachliche Prüfung.")
    if not akte.hauptforderung_offen and not akte.nebenforderungen_offen:
        return Ergebnis("Abschluss prüfen", "Laut Eingabe bestehen keine offenen Forderungspositionen; Buchungen und Abschlussvoraussetzungen kontrollieren.")
    if not akte.hauptforderung_offen and akte.nebenforderungen_offen:
        return Ergebnis("Abrechnung prüfen", "Hauptforderung ist laut Eingabe ausgeglichen; offene Nebenforderungen und Anspruchsgrundlagen prüfen.")
    if not akte.wirtschaftlichkeit_geprueft:
        return Ergebnis("Manuelle Prüfung", "Wirtschaftlichkeitsprüfung ist noch offen.")
    if akte.titel_vorhanden:
        return Ergebnis("Titulierte Forderung prüfen", "Titel, Vollstreckbarkeit, Zahlungen und mögliche Maßnahmen manuell prüfen.")
    return Ergebnis("Weiteres Vorgehen prüfen", "Offene Hauptforderung ohne angegebenen Titel; Anspruch, Verjährung und Voraussetzungen weiterer Schritte fachlich prüfen.")
