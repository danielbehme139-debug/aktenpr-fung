"""Automatisierte Tests mit fiktiven Fallkonstellationen."""
import unittest

from pruefung import Akte, pruefe_akte


def beispiel(**aenderungen):
    daten = dict(
        unterlagen_vollstaendig=True,
        hauptforderung_offen=True,
        nebenforderungen_offen=False,
        verjaehrung_geprueft=True,
        verjaehrungsrisiko=False,
        titel_vorhanden=False,
        wirtschaftlichkeit_geprueft=True,
    )
    daten.update(aenderungen)
    return Akte(**daten)


class PruefungTest(unittest.TestCase):
    def test_unvollstaendige_unterlagen(self):
        self.assertEqual(pruefe_akte(beispiel(unterlagen_vollstaendig=False)).empfehlung, "Manuelle Prüfung")

    def test_ungepruefte_verjaehrung(self):
        self.assertEqual(pruefe_akte(beispiel(verjaehrung_geprueft=False)).empfehlung, "Manuelle Prüfung")

    def test_verjaehrungsrisiko(self):
        self.assertEqual(pruefe_akte(beispiel(verjaehrungsrisiko=True)).empfehlung, "Manuelle Prüfung")

    def test_keine_offenen_positionen(self):
        self.assertEqual(pruefe_akte(beispiel(hauptforderung_offen=False)).empfehlung, "Abschluss prüfen")

    def test_nebenforderungen_offen(self):
        self.assertEqual(pruefe_akte(beispiel(hauptforderung_offen=False, nebenforderungen_offen=True)).empfehlung, "Abrechnung prüfen")

    def test_wirtschaftlichkeit_ungeprueft(self):
        self.assertEqual(pruefe_akte(beispiel(wirtschaftlichkeit_geprueft=False)).empfehlung, "Manuelle Prüfung")

    def test_titel(self):
        self.assertEqual(pruefe_akte(beispiel(titel_vorhanden=True)).empfehlung, "Titulierte Forderung prüfen")

    def test_offene_hauptforderung(self):
        self.assertEqual(pruefe_akte(beispiel()).empfehlung, "Weiteres Vorgehen prüfen")


if __name__ == "__main__":
    unittest.main()
