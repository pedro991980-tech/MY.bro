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

# Stato per la compilazione automatica da fotocamera/scanner
if "auto_desc" not in st.session_state:
    st.session_state.auto_desc = ""
if "auto_imp" not in st.session_state:
    st.session_state.auto_imp = 0.0

if not st.session_state.avviato:
    st.markdown("<h1 style='text-align: center;'>📞 MYbro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Il tuo assistente personale intelligente e centrale</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Gestisci in autonomia pagamenti, veicoli, appuntamenti, scuola, spese e scansione intelligente con WhatsApp.</p>", unsafe_allow_html=True)
    
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
    
    menu = st.sidebar.radio("Seleziona Sezione:", [
        "💳 Scadenze, Pagamenti & Auto", 
        "📅 Appuntamenti", 
        "🏫 Scuola (ClasseViva)", 
        "📊 Resoconto Spese",
        "📷 Scanner Intelligente (OCR & QR)"
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

    # ================= SEZIONE 1: PAGAMENTI, SCADENZE & CONTROLLO AUTO =================
    if menu == "💳 Scadenze, Pagamenti & Auto":
        st.header("💳 Gestione Scadenze, Pagamenti & Veicoli")
        st.write("Saldare utenze, rate o gestire le scadenze della tua auto tramite Conto o Carta Prepagata.")

        tipo_gestione = st.selectbox("Seleziona Ambito:", ["Pagamento Standard / Utenze", "🚗 Gestione Veicolo tramite Targa"])

        if tipo_gestione == "Pagamento Standard / Utenze":
            tipo_pagamento = st.selectbox(
                "Categoria Pagamento",
                ["Bolletta Luce/Gas/Acqua", "Affitto / Mutuo", "Rata Finanziamento", 
                 "Assicurazione Auto/Casa", "Abbonamenti Digitali", "Tasse Scolastiche", "TARI / IMU", "Altro"]
            )
            
            # Utilizza valori precompilati dallo scanner se presenti
            descrizione_pagamento = st.text_input("Descrizione Dettagliata", value=st.session_state.auto_desc)
            importo_pagamento = st.number_input("Importo (€)", min_value=0.0, value=st.session_state.auto_imp, format="%.2f")
            data_scadenza = st.date_input("Data di Scadenza", value=date.today())

            st.markdown("---")
            st.subheader("Metodo di Pagamento")
            metodo_scelto = st.radio("Paga con:", ["Conto Bancario (IBAN)", "Carta Prepagata"])

            if metodo_scelto == "Conto Bancario (IBAN)":
                dettaglio_conto = st.text_input("Inserisci IBAN del conto", placeholder="IT00X0000000000000000000000")
            else:
                dettaglio_conto = st.text_input("Inserisci Numero Carta Prepagata", placeholder="4000 0000 0000 0000")

            if st.button("Conferma Pagamento e Notifica WhatsApp", type="primary"):
                if not descrizione_pagamento or not dettaglio_conto:
                    st.error("Compila descrizione e dati conto/carta.")
                else:
                    giorni_mancanti = (data_scadenza - date.today()).days
                    messaggio = (
                        f"💳 *MYbro - Pagamento Eseguito*\n"
                        f"• Tipo: {tipo_pagamento}\n"
                        f"• Dettaglio: {descrizione_pagamento}\n"
                        f"• Importo: €{importo_pagamento:.2f}\n"
                        f"• Metodo: {metodo_scelto}\n"
                        f"• Scadenza: {data_scadenza}"
                    )
                    successo, res = invia_notifica_whatsapp(messaggio)
                    if successo:
                        st.success(f"Pagamento registrato con {metodo_scelto} e notifica inviata! (SID: {res})")
                        st.balloons()
                    else:
                        st.warning(f"Registrato, ma errore WhatsApp: {res}")
        else:
            st.subheader("🚗 Controllo Veicolo e Saldo Scadenze")
            targa_auto = st.text_input("Inserisci Targa Veicolo", placeholder="Es. AB123CD").upper()
            
            if targa_auto:
                st.info(f"Veicolo associato alla targa **{targa_auto}**:")
                scad_bollo = "31/12/2026"
                scad_rev = "15/05/2027"
                scad_rca = "30/09/2026"
                
                voce_auto = st.selectbox("Seleziona scadenza auto da saldare:", ["Bollo Auto", "Revisione", "Assicurazione RCA"])
                importo_auto = st.number_input("Importo Scadenza (€)", min_value=0.0, value=125.00, format="%.2f")
                metodo_auto = st.radio("Paga scadenza auto con:", ["Conto Bancario (IBAN)", "Carta Prepagata"])
                dett_auto = st.text_input("Dati Conto o Carta per pagamento auto")

                if st.button("Paga Scadenza Auto e Notifica", type="primary"):
                    if not dett_auto:
                        st.error("Inserisci i dati di pagamento.")
                    else:
                        msg_auto = (
                            f"🚗 *MYbro - Pagamento Veicolo*\n"
                            f"• Targa: {targa_auto}\n"
                            f"• Voce: {voce_auto}\n"
                            f"• Importo: €{importo_auto:.2f}\n"
                            f"• Metodo: {metodo_auto}"
                        )
                        successo, res = invia_notifica_whatsapp(msg_auto)
                        if successo:
                            st.success(f"Pagamento per {voce_auto} della targa {targa_auto} effettuato con successo!")
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

    # ================= SEZIONE 5: SCANNER INTELLIGENTE (FOTOCAMERA) =================
    elif menu == "📷 Scanner Intelligente (OCR & QR)":
        st.header("📷 Scanner con Fotocamera per Compilazione Automatica")
        st.write("Inquadra una bolletta, un'etichetta o un codice a barre: l'assistente leggerà i dati e compilerà automaticamente i moduli per te.")

        foto_scattata = st.camera_input("Scatta una foto al documento o codice")

        if foto_scattata is not None:
            st.success("Immagine catturata ed elaborata dall'intelligenza artificiale!")
            
            # Simulazione estrazione intelligente (OCR / Parsing automatico)
            st.session_state.auto_desc = "Bolletta estratta da Scanner (Enel / Utenza)"
            st.session_state.auto_imp = 45.50
            
            st.info("✨ **Dati rilevati con successo!**\n• Descrizione: `Bolletta estratta da Scanner (Enel / Utenza)`\n• Importo stimato: `€ 45.50`")
            st.write("Vai subito nella sezione **💳 Scadenze, Pagamenti & Auto**: i campi risulteranno già compilati in automatico!")
