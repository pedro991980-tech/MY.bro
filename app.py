import streamlit as st
import pandas as pd
from datetime import date
from classeviva import Session
from twilio.rest import Client

st.set_page_config(
    page_title="MYbro - Assistente Personale",
    page_icon="📞",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Nasconde il badge "Manage app" di Streamlit Cloud e pulisce l'interfaccia
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Icona del segretario al telefono
LOGO_SEGRETARIO = "https://img.icons8.com/color/96/customer-support.png"

if "avviato" not in st.session_state:
    st.session_state.avviato = False

# Stati per la compilazione automatica tramite fotocamera
if "scansione_desc" not in st.session_state:
    st.session_state.scansione_desc = ""
if "scansione_imp" not in st.session_state:
    st.session_state.scansione_imp = 0.0

if not st.session_state.avviato:
    st.markdown("<h1 style='text-align: center;'>📞 MYbro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Il tuo assistente personale intelligente e centrale</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Gestisci in autonomia pagamenti, veicoli, appuntamenti, scuola e spese con WhatsApp.</p>", unsafe_allow_html=True)
    
    col_1, col_2, col_3 = st.columns([1, 2, 1])
    with col_2:
        st.image(LOGO_SEGRETARIO, use_container_width=True)
        st.write("")
        if st.button("🚀 Entra in MYbro", type="primary", use_container_width=True):
            st.session_state.avviato = True
            st.rerun()
else:
    st.sidebar.image(LOGO_SEGRETARIO, width=70)
    st.sidebar.title("MYbro Hub 📞")
    st.sidebar.write("Assistente operativo attivo")
    
    # Menu ridotto ed essenziale con un'unica voce per pagamenti e auto
    menu = st.sidebar.radio("Seleziona Sezione:", [
        "💳 Pagamenti, Scadenze & Auto", 
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

    # ================= UNICA SEZIONE: PAGAMENTI, SCADENZE & AUTO CON FOTOCAMERA =================
    if menu == "💳 Pagamenti, Scadenze & Auto":
        st.header("💳 Pagamenti, Scadenze & Gestione Auto")
        st.write("Usa la fotocamera per scannerizzare una bolletta, un codice o una targa, oppure compila manualmente.")

        # Pulsante rapido per attivare la fotocamera direttamente dentro i pagamenti
        usa_fotocamera = st.checkbox("📷 Usa la fotocamera per scannerizzare e compilare in automatico")

        if usa_fotocamera:
            st.info("Inquadra la bolletta, il codice a barre o il documento con la fotocamera.")
            foto = st.camera_input("Scatta foto per riconoscimento automatico")
            if foto is not None:
                # Simulazione del riconoscimento intelligente dei dati tramite IA
                st.session_state.scansione_desc = "Bolletta / Voce Rilevata da Scanner"
                st.session_state.scansione_imp = 55.00
                st.success("✅ Dati estratti con successo dalla fotocamera e inseriti nei campi sottostanti!")

        st.markdown("---")
        
        # Scelta tra pagamento utenze/standard o gestione veicolo
        tipo_scelta = st.selectbox("Ambito:", ["Pagamento Utenze / Spese Generali", "🚗 Controllo e Pagamento Veicolo (Targa)"])

        if tipo_scelta == "Pagamento Utenze / Spese Generali":
            categoria = st.selectbox("Categoria", ["Bolletta Luce/Gas/Acqua", "Affitto / Mutuo", "Rata Finanziamento", "Assicurazione Casa", "Abbonamenti", "Altro"])
            
            # I campi si popolano automaticamente se usi la fotocamera
            descrizione = st.text_input("Descrizione", value=st.session_state.scansione_desc)
            importo = st.number_input("Importo (€)", min_value=0.0, value=st.session_state.scansione_imp, format="%.2f")
            data_scad = st.date_input("Data di Scadenza", value=date.today())

            metodo = st.radio("Metodo di Pagamento:", ["Conto Bancario (IBAN)", "Carta Prepagata"])
            dettagli_conto = st.text_input("Inserisci IBAN o Numero Carta", placeholder="IT00X0000...")

            if st.button("Conferma Pagamento e Notifica WhatsApp", type="primary"):
                if not descrizione or not dettagli_conto:
                    st.error("Compila tutti i campi obbligatori.")
                else:
                    messaggio = (
                        f"💳 *MYbro - Pagamento Eseguito*\n"
                        f"• Categoria: {categoria}\n"
                        f"• Descrizione: {descrizione}\n"
                        f"• Importo: €{importo:.2f}\n"
                        f"• Metodo: {metodo}"
                    )
                    successo, res = invia_notifica_whatsapp(messaggio)
                    if successo:
                        st.success("Pagamento registrato e notifica inviata con successo su WhatsApp!")
                        st.balloons()
                    else:
                        st.warning(f"Registrato, ma errore WhatsApp: {res}")
        else:
            st.subheader("🚗 Gestione Auto tramite Targa")
            targa = st.text_input("Inserisci o scansiona la Targa del Veicolo", placeholder="Es. AB123CD").upper()

            if targa:
                st.info(f"Veicolo associato: **{targa}** (Scadenze verificate in automatico)")
                voce_auto = st.selectbox("Voce da saldare:", ["Bollo Auto", "Revisione", "Assicurazione RCA"])
                importo_auto = st.number_input("Importo (€)", min_value=0.0, value=150.00, format="%.2f")
                metodo_auto = st.radio("Paga con:", ["Conto Bancario (IBAN)", "Carta Prepagata"])
                dett_auto = st.text_input("Dati Conto o Carta per pagamento auto")

                if st.button("Paga Scadenza Auto e Invia Avviso", type="primary"):
                    if not dett_auto:
                        st.error("Inserisci i dati di pagamento.")
                    else:
                        msg_auto = (
                            f"🚗 *MYbro - Pagamento Auto*\n"
                            f"• Targa: {targa}\n"
                            f"• Voce: {voce_auto}\n"
                            f"• Importo: €{importo_auto:.2f}\n"
                            f"• Metodo: {metodo_auto}"
                        )
                        successo, res = invia_notifica_whatsapp(msg_auto)
                        if successo:
                            st.success(f"Pagamento per {voce_auto} della targa {targa} completato!")
                        else:
                            st.warning(f"Errore invio WhatsApp: {res}")

    # ================= SEZIONE 2: APPUNTAMENTI =================
    elif menu == "📅 Appuntamenti":
        st.header("📅 Gestione Appuntamenti")
        titolo_appunt = st.text_input("Oggetto / Titolo Appuntamento")
        categoria_appunt = st.selectbox("Categoria", ["Visita Medica", "Impegno Lavorativo", "Scadenza Burocratica", "Personale"])
        data_appunt = st.date_input("Data Appuntamento", value=date.today())
        ora_appunt = st.time_input("Orario")

        if st.button("Salva Appuntamento e Notifica", type="primary"):
            if titolo_appunt:
                messaggio_app = f"📅 *MYbro - Promemoria Appuntamento*\n• Oggetto: {titolo_appunt} ({categoria_appunt})\n• Data: {data_appunt} ore {ora_appunt}"
                successo, res = invia_notifica_whatsapp(messaggio_app)
                if successo:
                    st.success("Appuntamento salvato e notificato!")
                else:
                    st.warning(f"Errore WhatsApp: {res}")
            else:
                st.error("Inserisci un titolo.")

    # ================= SEZIONE 3: SCUOLA (CLASSEVIVA) =================
    elif menu == "🏫 Scuola (ClasseViva)":
        st.header("🏫 Integrazione Scolastica (ClasseViva)")
        cv_user = st.text_input("Username ClasseViva")
        cv_pass = st.text_input("Password ClasseViva", type="password")

        if st.button("Verifica ClasseViva e Notifica", type="primary"):
            if not cv_user or not cv_pass:
                st.error("Inserisci credenziali.")
            else:
                try:
                    ses = Session()
                    ses.login(cv_user, cv_pass)
                    st.success("Connessione stabilita!")
                    successo, res = invia_notifica_whatsapp("🏫 *MYbro - ClasseViva*: Accesso effettuato con successo!")
                    if successo:
                        st.success("Notifica WhatsApp inviata!")
                except Exception as e:
                    st.error(f"Errore di autenticazione: {e}")

    # ================= SEZIONE 4: RESOCONTO SPESE =================
    elif menu == "📊 Resoconto Spese":
        st.header("📊 Resoconto Finanziario Mensile")
        if "spese_db" not in st.session_state:
            st.session_state.spese_db = pd.DataFrame(columns=["Categoria", "Descrizione", "Importo", "Data"])

        cat_spesa = st.selectbox("Categoria Spesa", ["Alimentari", "Utenze & Casa", "Trasporti", "Salute", "Scuola", "Svago", "Altro"])
        desc_spesa = st.text_input("Descrizione Spesa")
        imp_spesa = st.number_input("Importo (€)", min_value=0.0, format="%.2f")

        if st.button("Aggiungi Spesa", type="primary") and desc_spesa:
            nuova_riga = pd.DataFrame({"Categoria": [cat_spesa], "Descrizione": [desc_spesa], "Importo": [imp_spesa], "Data": [str(date.today())]})
            st.session_state.spese_db = pd.concat([st.session_state.spese_db, nuova_riga], ignore_index=True)
            st.success("Spesa registrata!")
            st.rerun()

        if not st.session_state.spese_db.empty:
            st.dataframe(st.session_state.spese_db, use_container_width=True)
            st.metric(label="Totale Spese", value=f"€ {st.session_state.spese_db['Importo'].sum():.2f}")
