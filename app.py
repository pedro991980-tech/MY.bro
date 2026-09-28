import streamlit as st
import pandas as pd
from datetime import date
from classeviva import Session
from twilio.rest import Client

st.set_page_config(
    page_title="MYbro - Assistente Personale",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

if "avviato" not in st.session_state:
    st.session_state.avviato = False

if not st.session_state.avviato:
    st.markdown("<h1 style='text-align: center;'>🤖 MYbro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Il tuo assistente personale intelligente e centrale</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Gestisci in autonomia pagamenti, appuntamenti, scuola e spese con notifiche automatiche su WhatsApp.</p>", unsafe_allow_html=True)
    
    col_1, col_2, col_3 = st.columns([1, 2, 1])
    with col_2:
        st.image("https://img.icons8.com/color/96/chatbot.png", use_container_width=True)
        st.write("")
        if st.button("🚀 Entra in MYbro", type="primary", use_container_width=True):
            st.session_state.avviato = True
            st.rerun()
else:
    st.sidebar.image("https://img.icons8.com/color/96/chatbot.png", width=70)
    st.sidebar.title("MYbro Hub 🤖")
    st.sidebar.write("Assistente operativo attivo")
    
    menu = st.sidebar.radio("Seleziona Sezione:", [
        "💳 Scadenze Pagamenti", 
        "📅 Appuntamenti", 
        "🏫 Scuola (ClasseViva)", 
        "📊 Resoconto Spese"
    ])

    if st.sidebar.button("🏠 Torna alla Home"):
        st.session_state.avviato = False
        st.rerun()

    TWILIO_ACCOUNT_SID = "IL_TUO_SID_QUI"
    TWILIO_AUTH_TOKEN = "IL_TUO_TOKEN_QUI"
    TWILIO_FROM_PHONE = "whatsapp:+14155238886"
    TWILIO_TO_PHONE = "+393331234567"

    def invia_notifica_whatsapp(testo):
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=testo,
                from_=TWILIO_FROM_PHONE,
                to=TWILIO_TO_PHONE
            )
            return True, message.sid
        except Exception as e:
            return False, str(e)

    if menu == "💳 Scadenze Pagamenti":
        st.header("💳 Gestione Scadenze Pagamenti")
        st.write("Monitoraggio preventivo per bollette, affitti, mutui, rate, assicurazioni, bollo auto, tasse e abbonamenti.")

        tipo_pagamento = st.selectbox(
            "Categoria Pagamento",
            ["Bolletta Luce/Gas/Acqua", "Affitto / Mutuo", "Rata Finanziamento", 
             "Assicurazione Auto/Casa", "Bollo Auto", "Abbonamenti Digitali", 
             "Tasse Scolastiche", "TARI / IMU", "Spese Condominiali", "Altro"]
        )
        descrizione_pagamento = st.text_input("Descrizione Dettagliata (es. Bolletta Enel)")
        importo_pagamento = st.number_input("Importo (€)", min_value=0.0, format="%.2f")
        data_scadenza = st.date_input("Data di Scadenza", value=date.today())

        if st.button("Registra Scadenza e Avvisa via WhatsApp", type="primary"):
            giorni_mancanti = (data_scadenza - date.today()).days
            messaggio = (
                f"🔔 *MYbro - Scadenza Pagamento*\n"
                f"• Tipo: {tipo_pagamento}\n"
                f"• Dettaglio: {descrizione_pagamento}\n"
                f"• Importo: €{importo_pagamento:.2f}\n"
                f"• Scadenza: {data_scadenza} (Tra {giorni_mancanti} giorni)"
            )
            successo, res = invia_notifica_whatsapp(messaggio)
            if successo:
                st.success(f"Scadenza registrata e notifica inviata con successo! (SID: {res})")
            else:
                st.warning(f"Registrato, ma errore nell'invio WhatsApp: {res}")

    elif menu == "📅 Appuntamenti":
        st.header("📅 Gestione Appuntamenti")
        st.write("Organizzazione autonoma di visite mediche, impegni di lavoro, scadenze legali e promemoria.")

        titolo_appunt = st.text_input("Oggetto / Titolo Appuntamento")
        categoria_appunt = st.selectbox("Categoria", ["Visita Medica", "Impegno Lavorativo", "Scadenza Burocratica", "Personale"])
        data_appunt = st.date_input("Data Appuntamento", value=date.today())
        ora_appunt = st.time_input("Orario")

        if st.button("Salva Appuntamento e Notifica", type="primary"):
            messaggio_app = (
                f"📅 *MYbro - Promemoria Appuntamento*\n"
                f"• Oggetto: {titolo_appunt} ({categoria_appunt})\n"
                f"• Data: {data_appunt} alle ore {ora_appunt}"
            )
            successo, res = invia_notifica_whatsapp(messaggio_app)
            if successo:
                st.success("Appuntamento salvato e notifica WhatsApp inviata!")
            else:
                st.warning(f"Salvato, ma errore invio WhatsApp: {res}")

    elif menu == "🏫 Scuola (ClasseViva)":
        st.header("🏫 Integrazione Scolastica (ClasseViva)")
        st.write("Verifica in tempo reale voti, note e circolari scolastiche.")

        cv_user = st.text_input("Username ClasseViva")
        cv_pass = st.text_input("Password ClasseViva", type="password")

        if st.button("Verifica ClasseViva e Notifica", type="primary"):
            if not cv_user or not cv_pass:
                st.error("Inserisci username e password.")
            else:
                try:
                    ses = Session()
                    ses.login(cv_user, cv_pass)
                    st.success("Connessione a ClasseViva stabilita con successo!")
                    try:
                        voti = ses.grades()
                        testo_scuola = "🏫 *MYbro - ClasseViva*: Accesso effettuato e registrato con successo!"
                    except:
                        testo_scuola = "🏫 *MYbro - ClasseViva*: Accesso al registro effettuato con successo."
                    
                    successo, res = invia_notifica_whatsapp(testo_scuola)
                    if successo:
                        st.success("Notifica scolastica inviata via WhatsApp!")
                    else:
                        st.warning(f"Connesso, ma errore invio WhatsApp: {res}")
                except Exception as e:
                    st.error(f"Errore di autenticazione: {e}")

    elif menu == "📊 Resoconto Spese":
        st.header("📊 Resoconto Finanziario Mensile")
        st.write("Registra e tieni traccia delle spese mensili suddivise per categoria.")

        if "spese_db" not in st.session_state:
            st.session_state.spese_db = pd.DataFrame(columns=["Categoria", "Descrizione", "Importo", "Data"])

        cat_spesa = st.selectbox("Categoria Spesa", ["Alimentari", "Utenze & Casa", "Trasporti", "Salute", "Scuola", "Svago", "Altro"])
        desc_spesa = st.text_input("Descrizione Spesa")
        imp_spesa = st.number_input("Importo (€)", min_value=0.0, format="%.2f")

        if st.button("Aggiungi Spesa al Resoconto", type="primary") and desc_spesa:
            nuova_riga = pd.DataFrame({"Categoria": [cat_spesa], "Descrizione": [desc_spesa], "Importo": [imp_spesa], "Data": [str(date.today())]})
            st.session_state.spese_db = pd.concat([st.session_state.spese_db, nuova_riga], ignore_index=True)
            st.success("Spesa registrata correttamente!")

        if not st.session_state.spese_db.empty:
            st.subheader("Elenco Spese Registrate")
            st.dataframe(st.session_state.spese_db, use_container_width=True)
            
            totale_mensile = st.session_state.spese_db["Importo"].sum()
            st.metric(label="Totale Spese del Mese", value=f"€ {totale_mensile:.2f}")

            st.subheader("Riepilogo Grafico per Categoria")
            riepilogo_cat = st.session_state.spese_db.groupby("Categoria")["Importo"].sum().reset_index()
            st.bar_chart(riepilogo_cat.set_index("Categoria"))
        else:
            st.info("Nessuna spesa inserita per il momento.")
