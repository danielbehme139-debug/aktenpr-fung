"""Interaktive Demonstration der Aktenprüfung – nur fiktive Eingaben."""
from pruefung import Akte, pruefe_akte


def frage(text: str) -> bool:
    while True:
        antwort = input(f"{text} [j/n]: ").strip().lower()
        if antwort in {"j", "ja"}:
            return True
        if antwort in {"n", "nein"}:
            return False
        print("Bitte 'j' oder 'n' eingeben.")


def main() -> None:
    print("Inkasso-Aktenprüfung – Demonstration (nur fiktive Daten)")
    print("Keine Rechtsberatung, keine automatische Maßnahme.\n")
    akte = Akte(
        unterlagen_vollstaendig=frage("Sind die benötigten Unterlagen vollständig?"),
        hauptforderung_offen=frage("Ist die Hauptforderung noch offen?"),
        nebenforderungen_offen=frage("Sind Nebenforderungen noch offen?"),
        verjaehrung_geprueft=frage("Wurde die Verjährung fachlich geprüft?"),
        verjaehrungsrisiko=frage("Wurde ein Verjährungsrisiko festgestellt?"),
        titel_vorhanden=frage("Ist ein Titel vorhanden?"),
        wirtschaftlichkeit_geprueft=frage("Wurde die Wirtschaftlichkeit geprüft?"),
    )
    ergebnis = pruefe_akte(akte)
    print(f"\nPrüfhinweis: {ergebnis.empfehlung}")
    print(f"Begründung: {ergebnis.begruendung}")


if __name__ == "__main__":
    main()
