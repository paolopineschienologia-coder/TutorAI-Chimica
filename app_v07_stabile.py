from pathlib import Path
from google import genai
import streamlit as st

# ====================================
# CONFIGURAZIONE
# ====================================

API_KEY = st.secrets["GEMINI_API_KEY"]

# ====================================
# FUNZIONI
# ====================================

def leggi_markdown(percorso):

    with open(
        percorso,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def genera_domanda(
    contenuto,
    domande_precedenti
):

    client = genai.Client(
        api_key=API_KEY
    )

    storico_domande = "\n".join(
        domande_precedenti
    )

    prompt = f"""
Sei un docente di Chimica.

Utilizza esclusivamente il materiale seguente.

Genera UNA SOLA domanda aperta.

NON ripetere domande uguali o molto simili.

DOMANDE GIA' UTILIZZATE:

{storico_domande}

Se una domanda è già stata posta,
scegli un concetto differente.

MATERIALE:

{contenuto}

Fornisci soltanto la domanda.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


def valuta_risposta(
    contenuto,
    domanda,
    risposta
):

    client = genai.Client(
        api_key=API_KEY
    )

    prompt = f"""
Sei un docente di Chimica.

Utilizza esclusivamente il materiale seguente.

MATERIALE:

{contenuto}

DOMANDA:

{domanda}

RISPOSTA DELLO STUDENTE:

{risposta}

Valuta la risposta.

Fornisci:

1. Cosa è corretto.
2. Eventuali errori o omissioni.
3. Suggerimenti per migliorare.
4. Una breve domanda di riflessione.

Non assegnare voti.

Rivolgiti direttamente allo studente.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


# ====================================
# STREAMLIT
# ====================================

st.set_page_config(
    page_title="TutorAI Chimica",
    page_icon="🧪"
)

st.title("🧪 TutorAI Chimica")

# ====================================
# SESSIONE
# ====================================

if "domanda_corrente" not in st.session_state:
    st.session_state.domanda_corrente = ""

if "contenuto_corrente" not in st.session_state:
    st.session_state.contenuto_corrente = ""

if "feedback_corrente" not in st.session_state:
    st.session_state.feedback_corrente = ""

if "indice_domanda" not in st.session_state:
    st.session_state.indice_domanda = 0

if "domande_fatte" not in st.session_state:
    st.session_state.domande_fatte = []

# ====================================
# ELENCO MATERIALI
# ====================================

cartella_materiali = Path(
    "materiali_tutor"
)

file_md = list(
    cartella_materiali.glob("*.md")
)

nomi_file = [
    file.stem
    for file in file_md
]

argomento = st.selectbox(
    "Seleziona un argomento:",
    nomi_file
)

# ====================================
# GENERA DOMANDA
# ====================================

if st.button("Genera domanda"):

    percorso_file = (
        cartella_materiali /
        f"{argomento}.md"
    )

    contenuto = leggi_markdown(
        percorso_file
    )

    domanda = genera_domanda(
        contenuto,
        st.session_state.domande_fatte
    )

    st.session_state.domanda_corrente = domanda

    st.session_state.domande_fatte.append(
        domanda
    )

    st.session_state.contenuto_corrente = contenuto

    st.session_state.feedback_corrente = ""

# ====================================
# VISUALIZZAZIONE DOMANDA
# ====================================

if st.session_state.domanda_corrente:

    st.subheader("Domanda")

    st.write(
        st.session_state.domanda_corrente
    )

    risposta = st.text_area(
        "Scrivi la tua risposta:",
        height=150,
        key=f"risposta_{st.session_state.indice_domanda}"
    )

    if st.button("Invia risposta"):

        if risposta.strip():

            feedback = valuta_risposta(
                st.session_state.contenuto_corrente,
                st.session_state.domanda_corrente,
                risposta
            )

            st.session_state.feedback_corrente = (
                feedback
            )

        else:

            st.warning(
                "Inserisci una risposta."
            )

# ====================================
# FEEDBACK
# ====================================

if st.session_state.feedback_corrente:

    st.subheader("Feedback")

    st.write(
        st.session_state.feedback_corrente
    )

    if st.button("Domanda successiva"):

        nuova_domanda = genera_domanda(
            st.session_state.contenuto_corrente,
            st.session_state.domande_fatte
        )

        st.session_state.domande_fatte.append(
            nuova_domanda
        )

        st.session_state.domanda_corrente = (
            nuova_domanda
        )

        st.session_state.feedback_corrente = ""

        st.session_state.indice_domanda += 1

        st.rerun()
