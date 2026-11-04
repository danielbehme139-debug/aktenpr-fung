import unittest
from streamlit.testing.v1 import AppTest


class OberflaecheTest(unittest.TestCase):
    def app(self):
        app = AppTest.from_file("streamlit_app.py").run()
        self.assertFalse(app.exception)
        return app

    def test_fehlende_eingaben_und_unbekannt(self):
        app = self.app()
        app.button[3].click().run()
        self.assertTrue(app.warning)
        self.assertEqual(app.session_state.phase, 0)
        for radio in app.radio:
            radio.set_value("Unbekannt")
        app.run()
        app.button[3].click().run()
        self.assertEqual(app.session_state.phase, 1)
        app.button[2].click().run()
        self.assertTrue(all(r.value == "Unbekannt" for r in app.radio))

    def test_beispiel_navigation_korrektur_neustart(self):
        app = self.app()
        app.button[1].click().run()
        for phase in range(4):
            self.assertEqual(app.session_state.phase, phase)
            app.button[3].click().run()
        self.assertEqual(app.session_state.phase, 4)
        self.assertFalse(app.exception)
        self.assertIn("Gerichtliches Mahnverfahren prüfen", [h.value for h in app.subheader])
        app.button[2].click().run()
        app.radio[0].set_value("Nein").run()
        for _ in range(4):
            app.button[3].click().run()
        self.assertIn("Manuelle Sachbearbeiterprüfung erforderlich", [h.value for h in app.subheader])
        app.button[0].click().run()
        self.assertEqual(app.session_state.phase, 0)
        self.assertTrue(all(r.value is None for r in app.radio))
        self.assertFalse(app.exception)
