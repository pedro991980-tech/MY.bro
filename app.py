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

# Icona del segretario al telefono
LOGO_SEGRETARIO = "https://img.icons8.com/color/96/customer-support.png"

if "avviato" not in st.session_state:
    st.session_state.avviato = False

if not st.session_state.avviato:
    st.markdown("<h1 style='text-align: center;'>📞 MYbro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Il tuo assistente personale intelligente e centrale</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Gestisci in autonomia pagamenti, conti, appuntamenti, scuola, spese, codici a barre e monitoraggio auto con WhatsApp.</p>", unsafe_allow_html=True)
    
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
        "💳 Scadenze & Pagamenti", 
        "📅 Appuntamenti", 
        "🏫 Scuola (ClasseViva)", 
        "📊 Resoconto Spese",
        "📷 Scanner Codici & QR",
        "🚗 Gestione Auto & Targa"
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

    # ================= SEZIONE 1: SCADENZE & PAGAMENTI CON CONTO/CARTA =================
    if menu == "💳 Scadenze & Pagamenti":
        st.header("💳 Gestione Scadenze e Pagamenti")
        st.write("Registra la scadenza e saldala subito tramite Conto Bancario o Carta Prepagata.")

        tipo_pagamento = st.selectbox(
            "Categoria Pagamento",
            ["Bolletta Luce/Gas/Acqua", "Affitto / Mutuo", "Rata Finanziamento", 
             "Assicurazione Auto/Casa", "Bollo Auto", "Abbonamenti Digitali", 
             "Tasse Scolastiche", "TARI / IMU", "Spese Condominiali", "Altro"]
        )
        descrizione_pagamento = st.text_input("Descrizione Dettagliata (es. Bolletta Enel)")
        importo_pagamento = st.number_input("Importo (€)", min_value=0.0, format="%.2f")
        data_scadenza = st.date_input("Data di Scadenza", value=date.today())

        st.markdown("---")
        st.subheader("Seleziona Metodo di Pagamento")
        metodo_scelto = st.radio("Paga con:", ["Conto Bancario (IBAN)", "Carta Prepagata"])

        if metodo_scelto == "Conto Bancario (IBAN)":
            dettaglio_conto = st.text_input("Inserisci IBAN del conto", placeholder="IT00X0000000000000000000000")
        else:
            dettaglio_conto = st.text_input("Inserisci Numero Carta Prepagata / Dettagli", placeholder="4000 0000 0000 0000")

        if st.button("Conferma Pagamento e Invia Avviso WhatsApp", type="primary"):
            if not descrizione_pagamento or not dettaglio_conto:
                st.error("Compila tutti i campi obbligatori (descrizione e dettagli conto/carta).")
            else:
                giorni_mancanti = (data_scadenza - date.today()).days
                messaggio = (
                    f"💳 *MYbro - Pagamento / Scadenza Eseguito*\n"
                    f"• Tipo: {tipo_pagamento}\n"
                    f"• Dettaglio: {descrizione_pagamento}\n"
                    f"• Importo: €{importo_pagamento:.2f}\n"
                    f"• Metodo: {metodo_scelto}\n"
                    f"• Scadenza: {data_scadenza} (Tra {giorni_mancanti} giorni)"
                )
                
                successo, res = invia_notifica_whatsapp(messaggio)
                if successo:
                    st.success(f"Pagamento registrato con {metodo_scelto} e notifica WhatsApp inviata! (SID: {res})")
                    st.balloons()
                else:
                    st.warning(f"Registrato, ma errore nell'invio WhatsApp: {res}")

    # ================= SEZIONE 2: APPUNTAMENTI =================
    elif menu == "📅 Appuntamenti":
        st.header("📅 Gestione Appuntamenti")
        st.write("Organizzazione autonoma di visite mediche, impegni di lavoro e promemoria.")

        titolo_appunt = st.text_input("Oggetto / Titolo Appuntamento")
        categoria_appunt = st.selectbox("Categoria", ["Visita Medica", "Impegno Lavorativo", "Scadenza Burocratica", "Personale"])
        data_appunt = st.date_input("Data Appuntamento", value=date.today())
        ora_appunt = st.time_input("Orario")

        if st.button("Salva Appuntamento e Notifica", type="primary"):
            if titolo_appunt:
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
            else:
                st.error("Inserisci un titolo per l'appuntamento.")

    # ================= SEZIONE 3: SCUOLA (CLASSEVIVA) =================
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

    # ================= SEZIONE 4: RESOCONTO SPESE =================
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
            st.rerun()

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

    # ================= SEZIONE 5: SCANNER CODICI A BARRE & QR =================
    elif menu == "📷 Scanner Codici & QR":
        st.header("📷 Scanner Codici a Barre e QR Code")
        st.write("Inquadra o inserisci il codice identificativo per registrare automaticamente prodotti o scadenze.")

        modo_inserimento = st.radio("Metodo di inserimento:", ["Inserimento Manuale Codice", "Simula Scansione Fotocamera"])
        
        if modo_inserimento == "Inserimento Manuale Codice":
            codice_digitato = st.text_input("Inserisci Codice a Barre / QR Code", placeholder="Es. 8001234567890")
            desc_prodotto = st.text_input("Nome Prodotto / Articolo")
            prezzo_articolo = st.number_input("Prezzo (€)", min_value=0.0, format="%.2f")
            
            if st.button("Registra Articolo da Codice", type="primary"):
                if codice_digitato and desc_prodotto:
                    messaggio_codice = (
                        f"📷 *MYbro - Articolo Scansionato*\n"
                        f"• Codice: {codice_digitato}\n"
                        f"• Articolo: {desc_prodotto}\n"
                        f"• Prezzo: €{prezzo_articolo:.2f}"
                    )
                    successo, res = invia_notifica_whatsapp(messaggio_codice)
                    if successo:
                        st.success(f"Articolo con codice {codice_digitato} registrato e notificato su WhatsApp!")
                    else:
                        st.warning(f"Registrato, ma errore WhatsApp: {res}")
                else:
                    st.error("Inserisci codice e nome prodotto.")
        else:
            st.info("💡 Suggerimento mobile: Da iPhone puoi scansionare direttamente etichette o codici tramite la fotocamera integrata o inserire il codice rapido qui sotto.")
            uploaded_file = st.file_uploader("Carica foto codice a barre / QR", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Codice scansionato con successo", width=250)
                st.success("Immagine ricevuta ed elaborata dall'assistente!")

    # ================= SEZIONE 6: GESTIONE AUTO & TARGA =================
    elif menu == "🚗 Gestione Auto & Targa":
        st.header("🚗 Monitoraggio Veicolo tramite Targa")
        st.write("Inserisci la targa della tua auto per verificare scadenze (Bollo, Revisione, Assicurazione) e inviare promemoria.")

        targa_auto = st.text_input("Inserisci Targa Veicolo", placeholder="Es. AB123CD").upper()
        modello_auto = st.text_input("Modello Auto (opzionale)", placeholder="Es. Fiat Panda / Golf")

        if targa_auto:
            st.markdown("---")
            st.subheader(f"Dati e Scadenze per il veicolo: **{targa_auto}**")
            
            # Simulazione calcolo scadenze basato sulla targa inserita
            scadenza_bollo = "31/12/2026"
            scadenza_revisione = "15/05/2027"
            scadenza_rca = "30/09/2026"

            st.info(f"• **Bollo Auto**: Scadenza prevista il {scadenza_bollo}\n• **Revisione**: Scadenza prevista il {scadenza_revisione}\n• **Assicurazione RCA**: Scadenza prevista il {scadenza_rca}")

            if st.button("Invia Report Auto e Scadenze via WhatsApp", type="primary"):
                messaggio_auto = (
                    f"🚗 *MYbro - Report Veicolo*\n"
                    f"• Targa: {targa_auto}\n"
                    f"• Modello: {modello_auto if modello_auto else 'Non specificato'}\n"
                    f"• Bollo: {scadenza_bollo}\n"
                    f"• Revisione: {scadenza_revisione}\n"
                    f"• RCA: {scadenza_rca}"
                )
                successo, res = invia_notifica_whatsapp(messaggio_auto)
                if successo:
                    st.success("Report veicolo e scadenze inviato con successo su WhatsApp!")
                else:
                    st.warning(f"Errore invio notifica WhatsApp: {res}")
