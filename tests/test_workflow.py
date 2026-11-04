import unittest
from workflow import FRAGEN, beispielakte, pruefe


class WorkflowTest(unittest.TestCase):
    def test_fuenf_ergebnisse(self):
        for daten, erwartet in [
            ({}, "Gerichtliches Mahnverfahren prüfen"),
            ({"titel": "Ja"}, "Bestehenden Titel und Vollstreckungsmöglichkeiten prüfen"),
            ({"hauptforderung": "Nein", "nebenforderungen": "Ja"}, "Abrechnung prüfen"),
            ({"hauptforderung": "Nein"}, "Aktenabschluss prüfen"),
            ({"unterlagen": "Nein"}, "Manuelle Sachbearbeiterprüfung erforderlich"),
        ]:
            with self.subTest(daten=daten):
                r = pruefe(beispielakte() | daten)
                self.assertEqual(r.ergebnis, erwartet)
                self.assertTrue(r.begruendung)
                self.assertTrue(r.schritte)

    def test_jede_unbekannte_oder_fehlende_antwort_blockiert(self):
        for f in FRAGEN:
            for wert in [None, "Unbekannt", "ungültig", False]:
                with self.subTest(frage=f.key, wert=wert):
                    r = pruefe(beispielakte() | {f.key: wert})
                    self.assertEqual(r.ergebnis, "Manuelle Sachbearbeiterprüfung erforderlich")
                    self.assertTrue(any(f.text in p for p in r.offene_punkte))

    def test_alle_kritischen_antworten(self):
        for f in FRAGEN:
            if f.erwartet is not None:
                with self.subTest(frage=f.key):
                    falsch = "Nein" if f.erwartet == "Ja" else "Ja"
                    self.assertEqual(pruefe(beispielakte() | {f.key: falsch}).ergebnis,
                                     "Manuelle Sachbearbeiterprüfung erforderlich")

    def test_leere_akte(self):
        self.assertEqual(len(pruefe({}).offene_punkte), 20)

    def test_vereinbarung_ist_keine_automatische_massnahme(self):
        self.assertTrue(any("freiwilligen" in s for s in pruefe(beispielakte()).schritte))
        self.assertFalse(any("freiwilligen" in s for s in pruefe(beispielakte() | {"vereinbarung": "Nein"}).schritte))
