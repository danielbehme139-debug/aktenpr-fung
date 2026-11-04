"""Lokale Oberfläche – keine Speicherung oder externen Dienste."""
import streamlit as st
from workflow import Antwort, FRAGEN, PHASEN, beispielakte, pruefe

st.set_page_config(page_title="Aktenprüfung", page_icon="📋", layout="centered")
st.markdown("""<style>
.stApp {background: #f5f8fc; color: #172b4d;}
.block-container {max-width: 960px; padding-top: 2rem;}
h1, h2, h3 {color: #173b65;}
.stButton button {min-height: 3rem; border-radius: 9px;}
[data-testid="stVerticalBlockBorderWrapper"] {background: white; border-radius: 12px;}
</style>""", unsafe_allow_html=True)


def initialisieren(beispiel=False):
    st.session_state.phase = 0
    st.session_state.angaben = beispielakte() if beispiel else {}
    for f in FRAGEN:
        st.session_state.pop("frage_" + f.key, None)
    st.session_state.pop("validierung", None)


if "angaben" not in st.session_state:
    initialisieren()

st.caption("DEMONSTRATION · NUR ERFUNDENE DATEN")
st.title("Inkasso-Aktenprüfung")
st.write("Schritt für Schritt zu einer nachvollziehbaren Entscheidungshilfe.")
st.info("Unverbindliche Prüfhinweise, keine Rechtsberatung. Es werden keine Maßnahmen eingeleitet. Bitte ausschließlich erfundene Angaben verwenden.")
a, b = st.columns(2)
a.button("Neue Aktenprüfung", on_click=initialisieren, use_container_width=True)
b.button("Beispielakte laden", on_click=initialisieren, args=(True,), use_container_width=True)
phase = st.session_state.phase
st.progress((phase + 1) / 5, text=f"Phase {phase + 1} von 5")
beantwortet = sum(v in ("Ja", "Nein", "Unbekannt") for v in st.session_state.angaben.values())
st.caption(f"{beantwortet} von {len(FRAGEN)} Fragen beantwortet · Unbekannte Angaben bleiben offene Prüfpunkte.")

if phase < 4:
    name, fragen = PHASEN[phase]
    st.header(f"{phase + 1}. {name}")
    if phase == 1 and st.session_state.angaben.get("hauptforderung") == "Nein":
        st.info("Die Hauptforderung ist ausgeglichen. Prüfen Sie gezielt, ob Nebenforderungen verbleiben und ob die Abrechnung vollständig ist.")
    if phase == 2:
        st.caption("Einzelne Antworten erlauben keine rechtliche Schlussfolgerung. Unsicherheiten müssen fachlich geklärt werden.")
    with st.container(border=True):
        for f in fragen:
            key = "frage_" + f.key
            if key not in st.session_state:
                st.session_state[key] = st.session_state.angaben.get(f.key)
            wert = st.radio(f.text, [a.value for a in Antwort], index=None, key=key, horizontal=True)
            if wert is not None:
                st.session_state.angaben[f.key] = wert
            if wert == "Unbekannt":
                st.caption("🟠 Offen: Bitte im weiteren Verlauf fachlich klären.")
    if phase == 2 and st.session_state.angaben.get("titel") == "Ja":
        st.info("Ein Titel ist angegeben. Bei offenen Forderungen wird die bestehende Titulierung berücksichtigt.")
    if phase == 2 and st.session_state.angaben.get("verjaehrung") != "Ja":
        st.warning("Verjährung ist ungeklärt: keine abschließende Empfehlung für ein gerichtliches Mahnverfahren.")
    if st.session_state.get("validierung"):
        st.warning("Bitte beantworten Sie jede Frage. Wenn eine Angabe fehlt, wählen Sie ausdrücklich ‚Unbekannt‘.")
    links, rechts = st.columns(2)
    def navigieren(ziel):
        if ziel > phase and any(f.key not in st.session_state.angaben for f in fragen):
            st.session_state.validierung = True
        else:
            st.session_state.phase = ziel
            st.session_state.validierung = False

    links.button("Zurück", disabled=phase == 0, use_container_width=True,
                 on_click=navigieren, args=(phase - 1,))
    rechts.button("Ergebnis ansehen" if phase == 3 else "Weiter", type="primary",
                  use_container_width=True, on_click=navigieren, args=(phase + 1,))

else:
    st.header("5. Ergebnis und Handlungsempfehlung")
    ergebnis = pruefe(st.session_state.angaben)
    with st.container(border=True):
        st.subheader(ergebnis.ergebnis)
        st.caption("Entscheidungshilfe – abschließende Beurteilung durch eine fachkundige Person erforderlich.")
        st.markdown("**Begründung anhand Ihrer Eingaben**")
        for grund in ergebnis.begruendung:
            st.write("• " + grund)
        st.markdown("**Noch offene Prüfpunkte**")
        if ergebnis.offene_punkte:
            for punkt in ergebnis.offene_punkte:
                st.warning(punkt)
        else:
            st.write("Keine offenen Punkte nach diesen Demonstrationsregeln. Das bestätigt keine rechtliche Zulässigkeit.")
        st.markdown("**Mögliche nächste Arbeitsschritte**")
        for schritt in ergebnis.schritte:
            st.write("• " + schritt)
    st.subheader("Alle Eingaben prüfen und korrigieren")
    for i, (name, fragen) in enumerate(PHASEN):
        with st.expander(name):
            for f in fragen:
                st.write(f"{f.text} **{st.session_state.angaben.get(f.key, 'Nicht beantwortet')}**")
            if st.button("Diese Phase korrigieren", key=f"edit_{i}"):
                st.session_state.phase = i
                st.rerun()
    if st.button("Zurück"):
        st.session_state.phase = 3
        st.rerun()
st.caption("Angaben verbleiben nur im flüchtigen Sitzungsspeicher. Keine Datenbank, kein Versand, keine Buchungen. Vor produktiver Nutzung ist eine fachliche, rechtliche und datenschutzrechtliche Prüfung erforderlich.")
