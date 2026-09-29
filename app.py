<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MYPOOL quotation</title>
    <!-- Favicon e Icona per schermata Home iOS -->
    <link rel="icon" type="image/png" href="logo-piscina.png">
    <link rel="apple-touch-icon" href="logo-piscina.png">
    
    <!-- PWA manifest -->
    <link rel="manifest" href="manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="MYPOOL quote">

    <!-- jsPDF libreria ufficiale per esportare in PDF -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

    <style>
        :root {
            --bg-color: #07090e;
            --card-bg: rgba(30, 41, 59, 0.7);
            --border-color: rgba(56, 189, 248, 0.35);
            --border-hover: rgba(56, 189, 248, 0.8);
            --text-color: #f8fafc;
            --accent-color: #0ea5e9;
            --accent-gradient: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            word-break: break-word;
            overflow-wrap: break-word;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--bg-color);
            background-image: radial-gradient(circle at 50% 0%, #1e1b4b 0%, var(--bg-color) 70%);
            color: var(--text-color);
            min-height: 100vh;
            padding: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-x: hidden;
        }

        /* Schermata di Apertura (Splash Screen) */
        #splashScreen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(145deg, #07090e 0%, #0f172a 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            padding: 24px;
            text-align: center;
        }

        .splash-logo {
            width: 130px;
            height: 130px;
            object-fit: contain;
            border-radius: 28px;
            background: rgba(15, 23, 42, 0.8);
            border: 2px solid var(--border-color);
            padding: 12px;
            margin-bottom: 24px;
            box-shadow: 0 12px 30px rgba(14, 165, 233, 0.25);
        }

        .splash-title {
            font-size: 38px;
            font-weight: 800;
            color: #38bdf8;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }

        .splash-subtitle {
            font-size: 16px;
            color: #94a3b8;
            margin-bottom: 40px;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 1px;
        }

        .splash-buttons {
            display: flex;
            flex-direction: column;
            gap: 14px;
            width: 100%;
            max-width: 300px;
        }

        .splash-btn {
            width: 100%;
            padding: 16px;
            background: var(--accent-gradient);
            color: #ffffff;
            border: none;
            border-radius: 14px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .splash-btn:active {
            transform: scale(0.97);
        }

        .splash-btn.lite {
            background: rgba(30, 41, 59, 0.9);
            border: 2px solid var(--border-color);
            color: #38bdf8;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        /* App principale */
        #mainAppContainer {
            display: none;
            width: 100%;
            max-width: 100%;
            flex-direction: column;
            align-items: center;
        }

        header {
            text-align: center;
            margin-bottom: 12px;
            width: 100%;
        }

        .app-logo {
            width: 60px;
            height: 60px;
            object-fit: contain;
            border-radius: 12px;
            margin-bottom: 4px;
            background: #0f172a;
            border: 1px solid var(--border-color);
            padding: 3px;
        }

        header h1 {
            font-size: 26px;
            font-weight: 800;
            color: #38bdf8;
            margin-bottom: 2px;
            letter-spacing: 0.5px;
        }

        header p {
            font-size: 14px;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Carosello & Pagine Orizzontali (Swipe) */
        .carousel-nav {
            display: flex;
            gap: 6px;
            width: 100%;
            margin-bottom: 12px;
            background: rgba(15, 23, 42, 0.6);
            padding: 4px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }

        .nav-step-btn {
            flex: 1;
            padding: 10px 4px;
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 14px;
            font-weight: 700;
            border-radius: 9px;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s ease;
        }

        .nav-step-btn.active {
            background: var(--accent-gradient);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        }

        .carousel-container {
            width: 100%;
            overflow: hidden;
            position: relative;
        }

        .carousel-track {
            display: flex;
            width: 300%;
            transition: transform 0.35s cubic-bezier(0.25, 1, 0.5, 1);
        }

        .carousel-page {
            width: 33.333%;
            flex-shrink: 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 2px;
        }

        /* Card in stile Glassmorphism moderno */
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            width: 100%;
        }

        .card h2 {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 12px;
            color: #38bdf8;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .input-group {
            margin-bottom: 12px;
            width: 100%;
        }

        .input-group label {
            display: block;
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 5px;
            color: #cbd5e1;
        }

        .input-group input, .input-group select {
            width: 100%;
            padding: 12px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            outline: none;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .input-group input:focus, .input-group select:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
        }

        .tabs-container {
            display: flex;
            gap: 6px;
            margin-bottom: 12px;
            width: 100%;
        }

        .tab-btn {
            flex: 1;
            padding: 10px 4px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-color);
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s ease;
        }

        .tab-btn.active {
            background: var(--accent-gradient);
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        }

        .nav-buttons-row {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }

        button.nav-action-btn {
            flex: 1;
            padding: 12px;
            background: rgba(51, 65, 85, 0.8);
            color: white;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
        }

        button.action-btn {
            width: 100%;
            padding: 15px;
            background: var(--accent-gradient);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 14px;
            text-transform: uppercase;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.35);
        }

        /* Visualizzatore Catalogo Dinamico (Stile Scheda Tecnica) */
        .pool-visual-container {
            width: 100%;
            height: 230px;
            border-radius: 12px;
            overflow: hidden;
            background: #020617;
            border: 1px solid var(--border-color);
            position: relative;
            margin-top: 6px;
            box-shadow: inset 0 4px 12px rgba(0,0,0,0.5);
        }

        .pool-visual-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: opacity 0.3s ease;
        }

        .pool-visual-badge {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(7, 9, 14, 0.85);
            backdrop-filter: blur(6px);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            color: #38bdf8;
            border: 1px solid var(--border-color);
            text-transform: uppercase;
        }

        .results {
            margin-top: 10px;
            background: rgba(15, 23, 42, 0.8);
            padding: 12px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            border-left: 4px solid #38bdf8;
            color: #f8fafc;
            line-height: 1.4;
            border-top: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
        }

        .results p {
            margin-bottom: 4px;
        }

        .bom-container {
            margin-top: 10px;
            background: rgba(15, 23, 42, 0.8);
            border-radius: 10px;
            padding: 10px;
            border: 1px solid var(--border-color);
            width: 100%;
        }

        .bom-list {
            list-style-type: none;
            width: 100%;
        }

        .bom-list li {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 8px;
            width: 100%;
        }

        .bom-list li:last-child {
            border-bottom: none;
        }

        .bom-left {
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
        }

        .bom-left input[type="checkbox"] {
            width: 22px;
            height: 22px;
            accent-color: #0ea5e9;
            cursor: pointer;
            flex-shrink: 0;
            border-radius: 4px;
        }

        .bom-left label {
            font-size: 15px !important;
            color: #f8fafc !important;
            font-weight: 600;
            cursor: pointer;
            margin: 0;
            line-height: 1.3;
        }

        .bom-right {
            width: 100%;
            display: flex;
            justify-content: flex-end;
        }

        .bom-price-input {
            width: 100% !important;
            max-width: 200px;
            padding: 8px !important;
            font-size: 15px !important;
            text-align: right;
            background: rgba(30, 41, 59, 0.9) !important;
            color: #ffffff !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px;
            font-weight: 700;
        }

        .total-box {
            margin-top: 12px;
            background: rgba(14, 165, 233, 0.15);
            border: 1px solid var(--border-color);
            padding: 14px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            color: #f8fafc;
            line-height: 1.5;
            text-align: right;
            width: 100%;
        }

        .total-box span {
            color: #38bdf8;
            font-size: 22px;
            font-weight: 800;
        }

        .lite-summary-box {
            margin-top: 12px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-color);
            padding: 14px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            color: #f8fafc;
            line-height: 1.6;
            text-align: left;
            width: 100%;
        }

        .lite-summary-box .macro-row {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding: 6px 0;
        }

        .lite-summary-box .macro-row:last-child {
            border-bottom: none;
        }

        .lite-summary-box .macro-val {
            color: #38bdf8;
            font-weight: 700;
        }
    </style>
</head>
<body>

    <!-- SCHERMATA DI APERTURA (SPLASH SCREEN) -->
    <div id="splashScreen">
        <img src="logo-piscina.png" alt="Logo" class="splash-logo" onerror="this.style.display='none'">
        <div class="splash-title">MYPOOLQUOTE</div>
        <div class="splash-subtitle">Cataloghi Ufficiali &bull; Fluidra & Renolit</div>
        <div class="splash-buttons">
            <button type="button" class="splash-btn" onclick="startApp('pro')">Versione PRO</button>
            <button type="button" class="splash-btn lite" onclick="startApp('lite')">Versione LITE</button>
        </div>
    </div>

    <!-- APP PRINCIPALE -->
    <div id="mainAppContainer">
        <header>
            <img src="logo-piscina.png" alt="Logo" class="app-logo" onerror="this.style.display='none'">
            <h1>MYPOOL QUOTATION</h1>
            <p id="headerModeLabel">Modalità PRO</p>
        </header>

        <!-- BARRA DI NAVIGAZIONE ORIZZONTALE A SCHEDE -->
        <div class="carousel-nav">
            <button type="button" class="nav-step-btn active" id="nav_step_0" onclick="goToPage(0)">1. Anagrafica</button>
            <button type="button" class="nav-step-btn" id="nav_step_1" onclick="goToPage(1)">2. Catalogo & Schema</button>
            <button type="button" class="nav-step-btn" id="nav_step_2" onclick="goToPage(2)">3. Listino & Totali</button>
        </div>

        <!-- CONTENITORE CAROSELLO / SWIPE -->
        <div class="carousel-container">
            <div class="carousel-track" id="carouselTrack">
                
                <!-- PAGINA 1: DATI ANAGRAFICI -->
                <div class="carousel-page">
                    <div class="card">
                        <h2>0. Dati Anagrafici</h2>
                        <div class="input-group">
                            <label>Azienda Installatrice / Costruttore</label>
                            <input type="text" id="builderName" value="MYPOOL S.r.l." placeholder="Nome Azienda">
                        </div>
                        <div class="input-group">
                            <label>Referente / Installatore</label>
                            <input type="text" id="builderRef" value="Mario Rossi" placeholder="Nome Referente">
                        </div>
                        <div class="input-group">
                            <label>Partita IVA Costruttore</label>
                            <input type="text" id="builderPiva" value="IT12345678901" placeholder="P.IVA">
                        </div>
                        <hr style="border: 1px solid var(--border-color); margin: 12px 0;">
                        <div class="input-group">
                            <label>Nome & Cognome Cliente</label>
                            <input type="text" id="clientName" value="Giuseppe Verdi" placeholder="Cliente">
                        </div>
                        <div class="input-group">
                            <label>Indirizzo Cantiere</label>
                            <input type="text" id="clientAddress" value="Via Roma 10, Milano" placeholder="Indirizzo">
                        </div>
                        <div class="input-group">
                            <label>Telefono / Email Cliente</label>
                            <input type="text" id="clientContact" value="333 1234567 - info@email.it" placeholder="Contatti">
                        </div>

                        <div class="nav-buttons-row">
                            <button type="button" class="nav-action-btn" onclick="goToPage(1)" style="width:100%;">Avanti &rarr;</button>
                        </div>
                    </div>
                </div>

                <!-- PAGINA 2: CATALOGHI UFFICIALI & SCHEMA GRAFICO -->
                <div class="carousel-page">
                    <div class="card">
                        <h2>1. Selezioni da Cataloghi Ufficiali</h2>
                        
                        <div class="input-group">
                            <label>Modelli Cataloghi (Fluidra / Renolit / Puls)</label>
                            <select id="catalogModel" onchange="applyCatalogModel()">
                                <option value="custom">-- Personalizzato / Libero --</option>
                                <option value="fluidra_8x4" selected>Fluidra Skimmer Residential (8 x 4 m)</option>
                                <option value="liberty_6x3">Puls Vetroresina Monoblocco Liberty (6 x 3 m)</option>
                                <option value="puls_lagos_5x3">Puls Fuori Terra Pannellato (5 x 3 m)</option>
                                <option value="mirror_10x5">Fluidra Mirror High-End (10 x 5 m)</option>
                            </select>
                        </div>

                        <div class="input-group">
                            <label>Tipologia Costruttiva</label>
                            <select id="poolType" onchange="onManualChange()">
                                <option value="skimmer">Interrata a Skimmer (Fluidra / C.A.)</option>
                                <option value="sfioratore">Bordo Sfioratore Mirror (Fluidra)</option>
                                <option value="vetroresina">Monoblocco in Vetroresina (Puls)</option>
                                <option value="fuoriterra">Fuori Terra / Seminterrata (Direct Industry)</option>
                            </select>
                        </div>

                        <div class="input-group">
                            <label>Lunghezza Vasca (m)</label>
                            <input type="number" id="poolL" value="8" step="0.5" oninput="onManualChange()">
                        </div>
                        <div class="input-group">
                            <label>Larghezza Vasca (m)</label>
                            <input type="number" id="poolW" value="4" step="0.5" oninput="onManualChange()">
                        </div>
                        <div class="input-group">
                            <label>Profondità Media (m)</label>
                            <input type="number" id="poolH" value="1.4" step="0.1" oninput="updateAll()">
                        </div>
                        <div class="input-group">
                            <label>Ricircolo Acqua (Norma UNI 10637)</label>
                            <select id="turnoverTime" onchange="updateAll()">
                                <option value="4">4 Ore (Pubbliche / Natatorie)</option>
                                <option value="6" selected>6 Ore (Residenziali Standard)</option>
                                <option value="8">8 Ore (Risparmio Energetico)</option>
                            </select>
                        </div>
                        
                        <div class="results" id="hydraulicResults">
                            <p>Volume: -- m³</p>
                            <p>Portata: -- m³/h</p>
                        </div>
                    </div>

                    <!-- VISUALIZZATORE SCHEMA CATALOGO DINAMICO -->
                    <div class="card" id="cardRender">
                        <h2>2. Schema & Render Ufficiale Catalogo</h2>
                        <div class="pool-visual-container">
                            <img id="poolRenderImg" src="" alt="Schema Catalogo Piscina" onerror="this.src='https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?auto=format&fit=crop&w=800&q=80'">
                            <div class="pool-visual-badge" id="poolBadgeText">Fluidra Skimmer Standard</div>
                        </div>
                    </div>

                    <div class="card" style="padding: 10px;">
                        <div class="nav-buttons-row">
                            <button type="button" class="nav-action-btn" onclick="goToPage(0)">&larr; Indietro</button>
                            <button type="button" class="nav-action-btn" onclick="goToPage(2)">Avanti &rarr;</button>
                        </div>
                    </div>
                </div>

                <!-- PAGINA 3: LISTINO, RINCARI & TOTALI -->
                <div class="carousel-page">
                    <div class="card">
                        <h2 id="cardTitleListino">3. Listino & Distinta Base (PRO)</h2>
                        
                        <!-- SELETTORE TAB PRO -->
                        <div class="input-group" id="proTabsWrapper">
                            <label>Modalità Visualizzazione Preventivo</label>
                            <div class="tabs-container">
                                <button type="button" class="tab-btn active" id="tab_completo" onclick="setQuoteMode('completo')">Globale</button>
                                <button type="button" class="tab-btn" id="tab_edile" onclick="setQuoteMode('edile')">Opere Edili</button>
                                <button type="button" class="tab-btn" id="tab_impianto" onclick="setQuoteMode('impianto')">Impianto</button>
                            </div>
                        </div>

                        <div class="input-group">
                            <label>Membrana Armata (Renolit Alkorplan Catalog)</label>
                            <select id="liningModel" onchange="updateAll()">
                                <option value="1000">Alkorplan 1000 (Tinta Unita 1,5 mm)</option>
                                <option value="2000">Alkorplan 2000 (Laccato 1,5 mm)</option>
                                <option value="touch" selected>Alkorplan Touch (Effetto Pietra 2 mm)</option>
                                <option value="evolve">Alkorplan Ceramics Evolve</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>Solarium Perimetrale (mq)</label>
                            <input type="number" id="solariumArea" value="50" step="1" oninput="updateAll()">
                        </div>
                        <div class="input-group">
                            <label>Doccia Solare (Puls / Fluidra)</label>
                            <select id="solarShower" onchange="updateAll()">
                                <option value="none">Nessuna Doccia</option>
                                <option value="standard" selected>Doccia Solare Alluminio Standard</option>
                                <option value="luxury">Doccia Solare Curva Design con Lava-piedi</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>Pompa di Calore Inverter (Riscaldamento)</label>
                            <select id="heatPump" onchange="updateAll()">
                                <option value="none">Nessuna Pompa di Calore</option>
                                <option value="inverter_std" selected>Inverter Full-Inverter Eco</option>
                                <option value="inverter_pro">Inverter Pro Alta Efficienza</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>Copertura Piscina</label>
                            <select id="poolCover" onchange="updateAll()">
                                <option value="none">Nessuna Copertura</option>
                                <option value="bubble" selected>Isotermica a Bolle 400 micron</option>
                                <option value="automatic">Tapparella Automatica di Sicurezza</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>Ricarico Materiali (%) [Listino Partner]</label>
                            <input type="number" id="materialMarkup" value="35" step="1" oninput="updateAll()">
                        </div>
                        <div class="input-group">
                            <label>Incidenza Manodopera & Scavi (%)</label>
                            <input type="number" id="laborMarkup" value="40" step="1" oninput="updateAll()">
                        </div>
                        <div class="input-group">
                            <label>Margine d'Impresa / Utile (%)</label>
                            <input type="number" id="companyMargin" value="18" step="1" oninput="updateAll()">
                        </div>
                        <div class="input-group">
                            <label>Aliquota IVA Applicata</label>
                            <select id="vatRate" onchange="updateAll()">
                                <option value="0.22" selected>IVA Ordinaria 22%</option>
                                <option value="0.10">IVA Agevolata 10% (Ristrutturazioni)</option>
                                <option value="0.00">Esente 0%</option>
                            </select>
                        </div>

                        <!-- CONTENITORE DISTINTA PRO -->
                        <div class="bom-container" id="proBomWrapper">
                            <p style="color: #38bdf8; font-size: 15px; margin-bottom: 8px; font-weight: 700; text-transform: uppercase;" id="bomTitleText">Componenti & Lavori:</p>
                            <ul class="bom-list" id="bomListContainer"></ul>
                        </div>

                        <!-- CONTENITORE SINTESI MACRO LITE -->
                        <div class="lite-summary-box" id="liteSummaryWrapper" style="display: none;">
                            <p style="color: #38bdf8; font-size: 15px; margin-bottom: 10px; font-weight: 700; text-transform: uppercase; text-align: center;">Sintesi Preventivo Rapido LITE</p>
                            <div class="macro-row">
                                <span>Subtotale Lavori Edili:</span>
                                <span class="macro-val" id="liteEdileVal">€ 0,00</span>
                            </div>
                            <div class="macro-row">
                                <span>Subtotale Impianto & Accessori:</span>
                                <span class="macro-val" id="liteImpiantoVal">€ 0,00</span>
                            </div>
                            <div class="macro-row" style="border-top: 1px solid var(--border-color); margin-top: 6px; padding-top: 8px;">
                                <span>Imponibile Totale:</span>
                                <span class="macro-val" id="liteImponibileVal">€ 0,00</span>
                            </div>
                            <div class="macro-row">
                                <span>IVA Applicata:</span>
                                <span class="macro-val" id="liteVatVal">€ 0,00</span>
                            </div>
                        </div>

                        <div class="total-box" id="totalBoxContent">
                            Imponibile: € 0,00<br>
                            IVA: € 0,00<br>
                            <strong>Totale Complessivo: <span>€ 0,00</span></strong>
                        </div>

                        <div class="nav-buttons-row" style="margin-bottom: 8px;">
                            <button type="button" class="nav-action-btn" onclick="goToPage(1)" style="width:100%;">&larr; Indietro alle Misure</button>
                        </div>

                        <button class="action-btn" onclick="generatePDF()">Genera Preventivo PDF</button>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        let bomCustomItems = {};
        let currentRenderList = [];
        let currentTotals = {};
        let appVersion = 'pro';
        let activeQuoteMode = 'completo';
        let currentPage = 0;

        const catalogModels = {
            'fluidra_8x4': { l: 8, w: 4, h: 1.4, type: 'skimmer' },
            'liberty_6x3': { l: 6, w: 3, h: 1.3, type: 'vetroresina' },
            'puls_lagos_5x3': { l: 5, w: 3, h: 1.2, type: 'fuoriterra' },
            'mirror_10x5': { l: 10, w: 5, h: 1.5, type: 'sfioratore' }
        };

        let touchStartX = 0;
        let touchEndX = 0;

        document.addEventListener('touchstart', e => {
            touchStartX = e.changedTouches[0].screenX;
        }, false);

        document.addEventListener('touchend', e => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, false);

        function handleSwipe() {
            const threshold = 50;
            if (touchEndX < touchStartX - threshold && currentPage < 2) {
                goToPage(currentPage + 1);
            }
            if (touchEndX > touchStartX + threshold && currentPage > 0) {
                goToPage(currentPage - 1);
            }
        }

        function startApp(ver) {
            appVersion = ver;
            document.getElementById('splashScreen').style.display = 'none';
            document.getElementById('mainAppContainer').style.display = 'flex';

            if (ver === 'lite') {
                document.getElementById('cardRender').style.display = 'none';
                document.getElementById('proTabsWrapper').style.display = 'none';
                document.getElementById('proBomWrapper').style.display = 'none';
                document.getElementById('liteSummaryWrapper').style.display = 'block';
                document.getElementById('cardTitleListino').innerText = '3. Preventivo Rapido Globale (LITE)';
                document.getElementById('headerModeLabel').innerText = 'Modalità LITE';
            } else {
                document.getElementById('cardRender').style.display = 'block';
                document.getElementById('proTabsWrapper').style.display = 'block';
                document.getElementById('proBomWrapper').style.display = 'block';
                document.getElementById('liteSummaryWrapper').style.display = 'none';
                document.getElementById('cardTitleListino').innerText = '3. Listino & Distinta Base (PRO)';
                document.getElementById('headerModeLabel').innerText = 'Modalità PRO';
            }
            updateAll();
        }

        function goToPage(pageNum) {
            currentPage = pageNum;
            const track = document.getElementById('carouselTrack');
            track.style.transform = `translateX(-${pageNum * 33.333}%)`;

            for (let i = 0; i < 3; i++) {
                const btn = document.getElementById(`nav_step_${i}`);
                if (i === pageNum) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function setQuoteMode(mode) {
            activeQuoteMode = mode;
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`tab_${mode}`).classList.add('active');
            updateAll();
        }

        function applyCatalogModel() {
            const val = document.getElementById('catalogModel').value;
            if (val === 'custom') return;
            const model = catalogModels[val];
            if (model) {
                document.getElementById('poolL').value = model.l;
                document.getElementById('poolW').value = model.w;
                document.getElementById('poolH').value = model.h;
                document.getElementById('poolType').value = model.type;
                onDimensionsChange();
            }
        }

        function onManualChange() {
            document.getElementById('catalogModel').value = 'custom';
            onDimensionsChange();
        }

        function updateCatalogVisual(type, lining) {
            const imgElement = document.getElementById('poolRenderImg');
            const badgeElement = document.getElementById('poolBadgeText');

            let imageUrl = "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?auto=format&fit=crop&w=800&q=80";
            let badgeText = "Fluidra Skimmer Residential";

            if (type === 'sfioratore') {
                imageUrl = "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80";
                badgeText = "Fluidra Mirror High-End";
            } else if (type === 'vetroresina') {
                imageUrl = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80";
                badgeText = "Puls Monoblocco Liberty GFK";
            } else if (type === 'fuoriterra') {
                imageUrl = "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?auto=format&fit=crop&w=800&q=80";
                badgeText = "Direct Industry / Puls Fuori Terra";
            }

            if (lining === 'touch') {
                badgeText += " + Renolit Alkorplan Touch";
            } else if (lining === 'evolve') {
                badgeText += " + Renolit Alkorplan Ceramics Evolve";
            }

            imgElement.src = imageUrl;
            badgeElement.innerText = badgeText;
        }

        function onDimensionsChange() {
            const l = parseFloat(document.getElementById('poolL').value) || 0;
            const w = parseFloat(document.getElementById('poolW').value) || 0;
            document.getElementById('solariumArea').value = Math.round((l + 3) * (w + 3) - (l * w));
            updateAll();
        }

        function renderBOMList(items) {
            const container = document.getElementById('bomListContainer');
            let html = '';

            items.forEach((item, index) => {
                if (bomCustomItems[index] === undefined) {
                    bomCustomItems[index] = { checked: true, price: item.price };
                }
                const currentObj = bomCustomItems[index];

                html += `
                    <li>
                        <div class="bom-left">
                            <input type="checkbox" id="bom_chk_${index}" ${currentObj.checked ? 'checked' : ''} onchange="toggleBOMItem(${index})">
                            <label for="bom_chk_${index}">${item.name}</label>
                        </div>
                        <div class="bom-right">
                            <input type="number" step="1" class="bom-price-input" id="bom_prc_${index}" value="${currentObj.price.toFixed(0)}" oninput="updateBOMPrice(${index}, this.value)" ${!currentObj.checked ? 'disabled style="opacity:0.4"' : ''}>
                        </div>
                    </li>
                `;
            });
            container.innerHTML = html;
        }

        function toggleBOMItem(index) {
            bomCustomItems[index].checked = document.getElementById(`bom_chk_${index}`).checked;
            updateAll();
        }

        function updateBOMPrice(index, val) {
            bomCustomItems[index].price = parseFloat(val) || 0;
            updateAll();
        }

        function updateAll() {
            const l = parseFloat(document.getElementById('poolL').value) || 0;
            const w = parseFloat(document.getElementById('poolW').value) || 0;
            const h = parseFloat(document.getElementById('poolH').value) || 0;
            const t = parseFloat(document.getElementById('turnoverTime').value) || 6;
            const pType = document.getElementById('poolType').value;
            const lining = document.getElementById('liningModel').value;
            
            const matMarkup = parseFloat(document.getElementById('materialMarkup').value) / 100 || 0;
            const labMarkup = parseFloat(document.getElementById('laborMarkup').value) / 100 || 0;
            const compMargin = parseFloat(document.getElementById('companyMargin').value) / 100 || 0;
            const vatPercentage = parseFloat(document.getElementById('vatRate').value) || 0;

            const volume = l * w * h;
            const flowRate = volume / t;
            const area = Math.PI * Math.pow(0.027, 2); 
            const velocity = (flowRate / 3600) / area;

            document.getElementById('hydraulicResults').innerHTML = `
                <p><strong>Volume Acqua:</strong> ${volume.toFixed(2)} m³</p>
                <p><strong>Portata Richiesta (UNI 10637):</strong> ${flowRate.toFixed(2)} m³/h</p>
                <p><strong>Velocità Tubazione:</strong> ${velocity.toFixed(2)} m/s</p>
            `;

            const skimmerCount = l > 10 ? 3 : (l > 6 ? 2 : 1);
            const jetsCount = Math.max(2, Math.ceil((l * 2 + w * 2) / 4));
            const ledCount = l > 10 ? 3 : (l > 6 ? 2 : 1);

            let baseMatCost = 140;
            if (pType === 'sfioratore') baseMatCost = 185;
            if (pType === 'vetroresina') baseMatCost = 160;
            if (pType === 'fuoriterra') baseMatCost = 110;

            const surfaceArea = (l * w) + (2 * (l + w) * h);
            const rawMaterials = surfaceArea * baseMatCost;
            
            const solariumMq = parseFloat(document.getElementById('solariumArea').value) || 0;
            const solariumTotal = solariumMq * 55 * (1 + matMarkup);

            const showerVal = document.getElementById('solarShower').value;
            let showerTotal = showerVal === 'standard' ? 450 * (1 + matMarkup) : (showerVal === 'luxury' ? 850 * (1 + matMarkup) : 0);

            const hpVal = document.getElementById('heatPump').value;
            let hpTotal = hpVal === 'inverter_std' ? 1800 * (1 + matMarkup) : (hpVal === 'inverter_pro' ? 2800 * (1 + matMarkup) : 0);

            const coverVal = document.getElementById('poolCover').value;
            let coverTotal = coverVal === 'bubble' ? 650 * (1 + matMarkup) : (coverVal === 'automatic' ? 4500 * (1 + matMarkup) : 0);

            let liningUnitPrice = 32;
            if (lining === '2000') liningUnitPrice = 38;
            if (lining === 'touch') liningUnitPrice = 48;
            if (lining === 'evolve') liningUnitPrice = 55;

            const itemStruct = (rawMaterials * 0.35) * (1 + matMarkup);
            const itemLining = (surfaceArea * liningUnitPrice) * (1 + matMarkup);
            const itemFilter = (flowRate > 25 ? 2400 : 1600) * (1 + matMarkup);
            
            let itemHydraulics = 0;
            let hydraulicsLabel = "";
            if (pType === 'sfioratore') {
                hydraulicsLabel = `Canale Bordo Sfioratore Mirror & Vasca Compenso (Fluidra)`;
                itemHydraulics = ((l * 2 + w * 2) * 95 + jetsCount * 45) * (1 + matMarkup);
            } else {
                hydraulicsLabel = `Skimmer Fluidra (${skimmerCount} pz) & Bocchette (${jetsCount} pz)`;
                itemHydraulics = (skimmerCount * 120 + jetsCount * 45) * (1 + matMarkup);
            }

            const itemElectric = (ledCount * 220 + 450) * (1 + matMarkup);
            const itemPipes = (l * w * 12) * (1 + matMarkup);

            let allItemsList = [
                { name: `Struttura & Scavi [Catalog: ${pType.toUpperCase()}]`, price: itemStruct, cat: 'edile' },
                { name: `Membrana Renolit Alkorplan [${lining.toUpperCase()}] (~${surfaceArea.toFixed(0)} mq)`, price: itemLining, cat: 'edile' },
                { name: `Pavimentazione Solare Perimetrale (${solariumMq} mq)`, price: solariumTotal, cat: 'edile' },
                { name: `Filtro a Sabbia & Pompa Fluidra (${flowRate.toFixed(1)} m³/h)`, price: itemFilter, cat: 'impianto' },
                { name: hydraulicsLabel, price: itemHydraulics, cat: 'impianto' },
                { name: `Quadro Elettrico CE & ${ledCount} Fari LED`, price: itemElectric, cat: 'impianto' },
                { name: "Tubazioni PN16 & Pozzetti di Ispezione", price: itemPipes, cat: 'impianto' },
                { name: "Doccia Solare da Esterno (Puls/Fluidra)", price: showerTotal, cat: 'impianto' },
                { name: "Pompa di Calore Inverter", price: hpTotal, cat: 'impianto' },
                { name: "Copertura Piscina", price: coverTotal, cat: 'impianto' }
            ];

            let rawItemsList = appVersion === 'lite' ? allItemsList : allItemsList.filter(it => {
                if (activeQuoteMode === 'completo') return true;
                return it.cat === activeQuoteMode;
            });

            const subMatActive = rawItemsList.reduce((acc, curr, idx) => {
                if (bomCustomItems[idx] === undefined) {
                    bomCustomItems[idx] = { checked: true, price: curr.price };
                } else {
                    bomCustomItems[idx].price = curr.price;
                }
                return acc + (bomCustomItems[idx].checked ? bomCustomItems[idx].price : 0);
            }, 0);

            let sumEdileMaterials = allItemsList.filter(it => it.cat === 'edile').reduce((acc, curr) => acc + curr.price, 0);
            let sumImpiantoMaterials = allItemsList.filter(it => it.cat === 'impianto').reduce((acc, curr) => acc + curr.price, 0);

            const laborCost = subMatActive * labMarkup;
            const subtotalForMargin = subMatActive + laborCost;
            const companyUtile = subtotalForMargin * compMargin;

            let ratioEdile = subMatActive > 0 ? (sumEdileMaterials / subMatActive) : 0.5;
            let ratioImpianto = subMatActive > 0 ? (sumImpiantoMaterials / subMatActive) : 0.5;

            let subEdileFinal = sumEdileMaterials + (laborCost * ratioEdile) + (companyUtile * ratioEdile);
            let subImpiantoFinal = sumImpiantoMaterials + (laborCost * ratioImpianto) + (companyUtile * ratioImpianto);

            const laborIdx = rawItemsList.length;
            const marginIdx = laborIdx + 1;

            if (bomCustomItems[laborIdx] === undefined) bomCustomItems[laborIdx] = { checked: true, price: laborCost };
            else bomCustomItems[laborIdx].price = laborCost;

            if (bomCustomItems[marginIdx] === undefined) bomCustomItems[marginIdx] = { checked: true, price: companyUtile };
            else bomCustomItems[marginIdx].price = companyUtile;

            let finalRenderList = [...rawItemsList];
            let laborLabel = activeQuoteMode === 'edile' ? "Manodopera Opere Edili & Scavi" : (activeQuoteMode === 'impianto' ? "Installazione & Montaggio Impianto" : "Manodopera Specializzata & Scavi Edili");
            
            finalRenderList.push({ name: laborLabel, price: bomCustomItems[laborIdx].price });
            finalRenderList.push({ name: "Margine d'Impresa / Utile", price: bomCustomItems[marginIdx].price });

            currentRenderList = finalRenderList;

            let totalImponibile = 0;
            finalRenderList.forEach((it, idx) => {
                if (bomCustomItems[idx] && bomCustomItems[idx].checked) {
                    totalImponibile += bomCustomItems[idx].price;
                }
            });

            const calculatedVat = totalImponibile * vatPercentage;
            const calculatedTotalWithVat = totalImponibile + calculatedVat;

            currentTotals = { 
                imponibile: totalImponibile, 
                vat: calculatedVat, 
                total: calculatedTotalWithVat, 
                vatRateVal: vatPercentage,
                edileFinal: subEdileFinal * (1 + vatPercentage),
                impiantoFinal: subImpiantoFinal * (1 + vatPercentage)
            };

            if (appVersion === 'pro') {
                renderBOMList(finalRenderList);
                const modeNames = { 'completo': 'GLOBALE (EDILE + IMPIANTO)', 'edile': 'SOLO OPERE EDILI & SCAVI', 'impianto': 'SOLO IMPIANTO & ACCESSORI' };
                document.getElementById('bomTitleText').innerHTML = `Sezione: ${modeNames[activeQuoteMode]}`;
                document.getElementById('totalBoxContent').innerHTML = `
                    Vista PRO: <strong>${modeNames[activeQuoteMode]}</strong><br>
                    Imponibile: € ${totalImponibile.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}<br>
                    IVA (${(vatPercentage * 100).toFixed(0)}%): € ${calculatedVat.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}<br>
                    <strong>Totale Complessivo: <span>€ ${calculatedTotalWithVat.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span></strong>
                `;
            } else {
                document.getElementById('liteEdileVal').innerText = `€ ${(subEdileFinal * (1 + vatPercentage)).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
                document.getElementById('liteImpiantoVal').innerText = `€ ${(subImpiantoFinal * (1 + vatPercentage)).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
                document.getElementById('liteImponibileVal').innerText = `€ ${totalImponibile.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
                document.getElementById('liteVatVal').innerText = `€ ${calculatedVat.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

                document.getElementById('totalBoxContent').innerHTML = `
                    <strong>Totale Complessivo LITE (IVA Inclusa): <span>€ ${calculatedTotalWithVat.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span></strong>
                `;
            }

            updateCatalogVisual(pType, lining);
        }

        function generatePDF() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

            const builder = document.getElementById('builderName').value;
            const builderRef = document.getElementById('builderRef').value;
            const builderPiva = document.getElementById('builderPiva').value;
            const client = document.getElementById('clientName').value;
            const address = document.getElementById('clientAddress').value;
            const contact = document.getElementById('clientContact').value;
            
            const l = document.getElementById('poolL').value;
            const w = document.getElementById('poolW').value;
            const h = document.getElementById('poolH').value;
            const pType = document.getElementById('poolType').value;
            const lining = document.getElementById('liningModel').value;

            doc.setFont("helvetica", "bold");
            doc.setFontSize(16);
            doc.setTextColor(14, 165, 233);
            doc.text("MYPOOL QUOTATION", 14, 18);
            
            let titlePDF = appVersion === 'lite' ? "PREVENTIVO CATALOGO (LITE)" : `PREVENTIVO PRO CATALOGO (${activeQuoteMode.toUpperCase()})`;
            doc.setFontSize(11);
            doc.setTextColor(80);
            doc.text(titlePDF, 14, 25);

            doc.setFontSize(10);
            doc.setTextColor(100);
            doc.text(`Data: ${new Date().toLocaleDateString('it-IT')}`, 14, 32);

            doc.setFontSize(10);
            doc.setTextColor(0);
            doc.text("DATI COSTRUTTORE:", 14, 39);
            doc.setFont("helvetica", "normal");
            doc.text(`Azienda: ${builder} (P.IVA: ${builderPiva}) - Rif: ${builderRef}`, 14, 45);

            doc.setFont("helvetica", "bold");
            doc.text("DATI CLIENTE:", 14, 53);
            doc.setFont("helvetica", "normal");
            doc.text(`Cliente: ${client} - Cantiere: ${address} (${contact})`, 14, 59);

            doc.setFont("helvetica", "bold");
            doc.text("SPECIFICHE CATALOGO UFFICIALE:", 14, 67);
            doc.setFont("helvetica", "normal");
            doc.text(`Tipologia: ${pType.toUpperCase()} | Membrana: Renolit Alkorplan ${lining.toUpperCase()}`, 14, 73);
            doc.text(`Dimensioni: ${l}m x ${w}m x ${h}m`, 14, 79);

            let y = 90;

            if (appVersion === 'lite') {
                doc.setFontSize(11);
                doc.setFont("helvetica", "bold");
                doc.text("SINTESI ECONOMICA MACRO-VOCI:", 14, y);
                y += 8;
                doc.setFont("helvetica", "normal");
                doc.text(`- Subtotale Lavori Edili (IVA incl.):`, 14, y);
                doc.text(`€ ${currentTotals.edileFinal.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`, 170, y, { align: 'right' });
                y += 7;
                doc.text(`- Subtotale Impianto & Accessori (IVA incl.):`, 14, y);
                doc.text(`€ ${currentTotals.impiantoFinal.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`, 170, y, { align: 'right' });
                y += 10;
            } else {
                doc.setFontSize(10);
                doc.setFont("helvetica", "bold");
                doc.text("VOCI DI COMPUTO SELEZIONATE:", 14, y);
                y += 7;

                doc.setFont("helvetica", "normal");
                currentRenderList.forEach((item, idx) => {
                    if (bomCustomItems[idx] && bomCustomItems[idx].checked) {
                        if (y > 270) { doc.addPage(); y = 20; }
                        doc.text(`- ${item.name}`, 14, y);
                        doc.text(`€ ${bomCustomItems[idx].price.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`, 170, y, { align: 'right' });
                        y += 7;
                    }
                });
                y += 8;
            }

            if (y > 250) { doc.addPage(); y = 20; }

            doc.setFont("helvetica", "bold");
            doc.text(`Imponibile: € ${currentTotals.imponibile.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`, 170, y, { align: 'right' });
            y += 7;
            doc.text(`IVA (${(currentTotals.vatRateVal * 100).toFixed(0)}%): € ${currentTotals.vat.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`, 170, y, { align: 'right' });
            y += 9;
            doc.setFontSize(13);
            doc.setTextColor(14, 165, 233);
            doc.text(`TOTALE: € ${currentTotals.total.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`, 170, y, { align: 'right' });

            doc.save(`Preventivo_Catalog_${appVersion}_${client.replace(/\s+/g, '_')}.pdf`);
        }

        window.onload = function() {
            applyCatalogModel();
        };
    </script>
</body>
</html>
