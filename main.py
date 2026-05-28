import streamlit as st

# 1. CONFIGURATION DE L'INTERFACE
st.set_page_config(
    page_title="Data-Checker | UNIL Legal Tech",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Styles CSS professionnels
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #0077b6; text-align: center; }
    .subtitle { font-size: 18px; text-align: center; color: #555; margin-bottom: 20px; }
    .section-header { font-size: 20px; font-weight: bold; color: #1d3557; margin-top: 25px; }
    .legal-text { font-style: italic; color: #4a5568; background-color: #f7fafc; padding: 10px; border-left: 4px solid #0077b6; }
    </style>
""", unsafe_allow_html=True)

# 2. SÉLECTEUR DYNAMIQUE DE LANGUE
lang = st.sidebar.radio("Language / Langue", ["FR", "EN"], index=0)

st.markdown('<div class="main-title">⚖️ Data-Checker</div>', unsafe_allow_html=True)
if lang == "FR":
    st.markdown('<div class="subtitle">Système expert d\'audit automatisé pour la réutilisation des données de recherche</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="subtitle">Expert system for automated auditing of research data reuse</div>', unsafe_allow_html=True)
st.write("---")

# ==========================================
# MODULE INITIAL : VERROU DE COMPÉTENCE (ART. 2 LRH - TEXTE STRICT CORRIGÉ)
# ==========================================
if lang == "FR":
    st.markdown('<div class="section-header">📋 Évaluation de compétence (Art. 2 LRH)</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-text"><b>Art. 2 Champ d’application (LRH) :</b> La présente loi s’apply à la recherche sur les maladies humaines et sur la structure et le fonctionnement du corps humain.</div>', unsafe_allow_html=True)
    lrh_q = "Votre recherche est-elle pratiquée sur l'un des éléments suivants (Art. 2 al. 1 LRH) ?"
    lrh_ops = [
        "a. Sur des personnes", 
        "b. Sur des personnes décédées", 
        "c. Sur des embryons et des fœtus", 
        "d. Sur du matériel biologique", 
        "e. Sur des données personnelles liées à la santé", 
        "Aucun (Art. 2 al. 2 : matériel anonymisé / données collectées anonymement ou anonymisées)"
    ]
else:
    st.markdown('<div class="section-header">📋 Competence Assessment (Art. 2 HRA)</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-text"><b>Art. 2 Scope of application (HRA):</b> This Act applies to research on human diseases and on the structure and function of the human body.</div>', unsafe_allow_html=True)
    lrh_q = "Is your research conducted on any of the following elements (Art. 2 al. 1 HRA)?"
    lrh_ops = [
        "a. On persons", 
        "b. On deceased persons", 
        "c. On embryos and fetuses", 
        "d. On biological material", 
        "e. On personal data health-related", 
        "None (Art. 2 al. 2: anonymized material / data collected anonymously or anonymized)"
    ]

lrh_selection = st.radio(lrh_q, lrh_ops, index=5)

if "Aucun" not in lrh_selection and "None" not in lrh_selection:
    if lang == "FR":
        st.error("🛑 VERROU ALGORITHMIQUE — APPLICATION DE LA LRH (LEX SPECIALIS)")
        st.markdown("En vertu de l'art. 2 al. 1 LRH, votre projet entre dans le champ d'application de la recherche humaine. Ce projet sort du cadre d'évaluation de cet outil général. Vous devez obligatoirement saisir la **CER-VD** (art. 51 al. 1 LRH).")
    else:
        st.error("🛑 ALGORITHMIC LOCK — HRA APPLICATION (LEX SPECIALIS)")
        st.markdown("Pursuant to Art. 2 al. 1 HRA, your project falls within the scope of human research. This project steps out of this general tool. You must formally submit your project to the **CER-VD** (Art. 51 al. 1 HRA).")
    st.stop()
else:
    st.success("✔ Loi non applicable (Art. 2 al. 2 LRH). Régime général déverrouillé." if lang == "FR" else "✔ Act not applicable (Art. 2 al. 2 HRA). General regime unlocked.")

st.write("---")

score = 100
actions_correctives = []

# ==========================================
# MODULE RATTACHEMENT INSTITUTIONNEL (UNIL vs EXTERNE)
# ==========================================
if lang == "FR":
    st.markdown('<div class="section-header">🏫 Affiliation Institutionnelle</div>', unsafe_allow_html=True)
    unil_check = st.radio("Êtes-vous chercheur ou rattaché à l'UNIL ?", ["Oui, je suis membre de l'UNIL (Régime Directives internes)", "Non, chercheur externe"], index=0)
    is_unil = "Oui" in unil_check
else:
    st.markdown('<div class="section-header">🏫 Institutional Affiliation</div>', unsafe_allow_html=True)
    unil_check = st.radio("Are you a researcher or affiliated with UNIL?", ["Yes, I am a UNIL member (Internal Directives regime)", "No, external researcher"], index=0)
    is_unil = "Yes" in unil_check

st.write("---")

# ==========================================
# ÉTAPE 1 : VÉRIFICATION INITIALE DES DONNÉES
# ==========================================
if lang == "FR":
    st.markdown('<div class="section-header">Étape 1 : Vérification des données (Art. 5 LPD)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #f1f5f9; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
    <b>Guide de qualification juridique des données :</b><br>
    • <b>Données personnelles brutes :</b> Informations permettant d'identifier directement une personne (ex: nom, e-mail).<br>
    • <b>Données pseudonymisées / codées :</b> Les identifiants directs sont remplacés par un code. Elles restent des données personnelles car la clé de décodage permet la ré-identification.<br>
    • <b>Données anonymisées :</b> Processus irréversible rendant l'identification impossible. Hors champ LPD (réutilisation libre).
    </div>
    """, unsafe_allow_html=True)
    e1_q = "Quelle est la nature juridique des fichiers de données ?"
    e1_ops = ["Données pseudonymisées ou codées", "Données anonymisées", "Données personnelles brutes"]
else:
    st.markdown('<div class="section-header">Step 1: Data Verification (Art. 5 FADP)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #f1f5f9; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
    <b>Legal Data Classification Guide:</b><br>
    • <b>Raw personal data:</b> Information directly identifying a person (e.g., name, e-mail).<br>
    • <b>Pseudonymized / coded data:</b> Direct identifiers are replaced by a code. They remain personal data because the decoding key allows re-identification.<br>
    • <b>Anonymized data:</b> Irreversible process making identification permanently impossible. Outside FADP scope (free reuse).
    </div>
    """, unsafe_allow_html=True)
    e1_q = "What is the legal nature of the data files?"
    e1_ops = ["Pseudonymized or coded data", "Anonymized data", "Raw personal data"]

etape1_option = st.radio(e1_q, e1_ops, index=0)

if "Données anonymisées" in etape1_option or "Anonymized data" in etape1_option:
    st.balloons()
    st.success("🟢 VERDICT : RÉUTILISATION LIBRE (Score : 100/100)" if lang == "FR" else "🟢 VERDICT: FREE REUSE (Score: 100/100)")
    st.markdown("Les données anonymes ne tombent pas sous le champ d'application de la LPD (art. 5 let. a) ni du RGPD. Réutilisation libre." if lang == "FR" else "Anonymized data does not fall under the scope of the FADP (Art. 5 let. a) nor the GDPR. Free reuse.")
    st.stop()

else:
    st.write("---")
    
    # ==========================================
    # ÉTAPE 2 : DONNÉES SECONDAIRES
    # ==========================================
    if lang == "FR":
        st.markdown('<div class="section-header">Étape 2 : Données secondaires (Compatibilité de la finalité)</div>', unsafe_allow_html=True)
        st.caption("Réf : art. 6 al. 3 LPD ; art. 5 al. 1 let. b RGPD")
        e2_q = "La nouvelle finalité scientifique de recherche est-elle compatible avec la finalité initiale de la collecte ?"
        yes_no = ["Oui", "Non"]
    else:
        st.markdown('<div class="section-header">Step 2: Secondary Data (Purpose Compatibility)</div>', unsafe_allow_html=True)
        st.caption("Ref: Art. 6 al. 3 FADP; Art. 5 al. 1 let. b GDPR")
        e2_q = "Is the new scientific research purpose compatible with the initial collection purpose?"
        yes_no = ["Yes", "No"]
        
    etape2_choice = st.radio(e2_q, yes_no, index=0, key="r_e2")
    
    if etape2_choice in ["Non", "No"]:
        score -= 25
        actions_correctives.append("❌ **Action Étape 2 :** [LPD] Rupture du principe de finalité. Nouveau consentement requis ou mise à jour immédiate du cadre d'accord des participants." if lang == "FR" else "❌ **Action Step 2:** [FADP] Breach of the purpose limitation principle. New consent required or immediate update of the participants' agreement framework.")

    # ==========================================
    # ÉTAPE 3 : COUVERTURE DU CONSENTEMENT
    # ==========================================
    if lang == "FR":
        st.markdown('<div class="section-header">Étape 3 : Couverture du consentement initial</div>', unsafe_allow_html=True)
        st.caption("Réf : art. 12 LPrD ; art. 6 al. 6 LPD")
        e3_q = "Le consentement initial existant couvre-t-il expressément ou implicitement cette nouvelle finalité ?"
    else:
        st.markdown('<div class="section-header">Step 3: Initial Consent Coverage</div>', unsafe_allow_html=True)
        st.caption("Ref: Art. 12 LPrD; Art. 6 al. 6 FADP")
        e3_q = "Does the existing initial consent expressly or implicitly cover this new purpose?"
        
    etape3_choice = st.radio(e3_q, yes_no, index=0, key="r_e3")
    
    if etape3_choice in ["Non", "No"]:
        score -= 25
        actions_correctives.append("❌ **Action Étape 3 :** [LPD] Défaut de couverture du consentement. Obligation d'obtenir un nouveau consentement écrit et exprès auprès des personnes concernées." if lang == "FR" else "❌ **Action Step 3:** [FADP] Lack of consent coverage. Obligation to obtain a new express, written consent from the data subjects.")

    # ==========================================
    # ÉTAPE 4 : STOCKAGE ET TRANSFERT INTERNATIONAL (AVEC LISTE OPDo RECONNAISSANCE)
    # ==========================================
    if lang == "FR":
        st.markdown('<div class="section-header">Étape 4 : Stockage et Transfert International (Art. 16 LPD)</div>', unsafe_allow_html=True)
        st.caption("Réf : Annexe 1 OPDo (Liste révisée des États assurant une protection adéquate)")
        e4_q = "Dans quel pays ou zone géographique vos fichiers de recherche seront-ils stockés ou hébergés ?"
        e4_ops = [
            "Suisse (Infrastructure locale / Serveur interne)",
            "Zone Union Européenne / EEE (France, Allemagne, Italie, Islande, etc.)",
            "États-Unis (Entreprise certifiée Swiss-U.S. Data Privacy Framework)",
            "Royaume-Uni / Canada / Israël / Nouvelle-Zélande",
            "Autre pays tiers (Chine, Inde, Russie, USA non certifié, etc.)"
        ]
    else:
        st.markdown('<div class="section-header">Step 4: Storage & International Transfer (Art. 16 FADP)</div>', unsafe_allow_html=True)
        st.caption("Ref: Annex 1 DPO (Revised list of States ensuring adequate data protection)")
        e4_q = "In which country or geographical area will your research files be stored or hosted?"
        e4_ops = [
            "Switzerland (Local infrastructure / Internal server)",
            "European Union / EEA Zone (France, Germany, Italy, Iceland, etc.)",
            "United States (Certified under Swiss-U.S. Data Privacy Framework)",
            "United Kingdom / Canada / Israel / New Zealand",
            "Other third country (China, India, Russia, non-certified USA, etc.)"
        ]
        
    etape4_location = st.selectbox(e4_q, e4_ops, index=0)
    
    if "Autre pays tiers" in etape4_location or "Other third country" in etape4_location:
        score -= 25
        if is_unil:
            if lang == "FR":
                actions_correctives.append("❌ **Action Étape 4 : [Directive UNIL 4.5 & Art. 4 OPDo]** Hébergement dans un État au niveau de protection insuffisant. Vous devez impérativement rapatrier et stocker vos fichiers sur l'infrastructure sécurisée de l'UNIL (**serveur NAS de l'Amphimax**), gérée par le Ci-UNIL, garantissant la localisation des données en Suisse.")
            else:
                actions_correctives.append("❌ **Action Step 4: [UNIL Directive 4.5 & Art. 4 DPO]** Hosting in a State with an insufficient level of protection. You must repatriate and store your files on the secure infrastructure of UNIL (**Amphimax NAS server**), managed by Ci-UNIL, guaranteeing data localization in Switzerland.")
        else:
            if lang == "FR":
                actions_correctives.append("❌ **Action Étape 4 :** [LPD] Le pays choisi n'offre pas de protection adéquate (Annexe 1 OPDo). Vous devez obligatoirement mettre en place des Clauses Contractuelles Types (CCT) approuvées par le PFPDT et exiger un chiffrement fort géré par le responsable suisse.")
            else:
                actions_correctives.append("❌ **Action Step 4:** [FADP] The selected country does not offer adequate protection (Annex 1 DPO). You must implement Standard Contractual Clauses (SCC) approved by the FDPIC and mandate strong client-side encryption.")

    # Application de la Directive UNIL 4.1
    if is_unil:
        st.write("---")
        if lang == "FR":
            st.markdown('<div><b>ℹ️ Contrôle de gouvernance institutionnelle activé (Directive UNIL 4.1)</b></div>', unsafe_allow_html=True)
            e41_q = "Si un sous-traitant externe ou tiers manipule les données, un contrat de traitement conforme à la Directive UNIL 4.1 a-t-il été signé ?"
        else:
            st.markdown('<div><b>ℹ️ Institutional governance control activated (UNIL Directive 4.1)</b></div>', unsafe_allow_html=True)
            e41_q = "If an external processor or third party handles the data, has a data processing agreement compliant with UNIL Directive 4.1 been signed?"
            
        unil_contract_choice = st.radio(e41_q, yes_no, index=0, key="r_unil41")
        
        if unil_contract_choice in ["Non", "No"]:
            score -= 10
            actions_correctives.append("❌ **Gouvernance : [Directive UNIL 4.1]** Manquement de gouvernance contractuelle. Toute sous-traitance de données de recherche requiert la signature d'une convention de traitement standardisée validée par le **Service juridique de l'UNIL** avant le début des opérations informatiques." if lang == "FR" else "❌ **Governance: [UNIL Directive 4.1]** Contractual governance breach. Any outsourcing of research data processing requires the signature of a standardized processing agreement validated by the **UNIL Legal Service** before computing operations begin.")

    # ==========================================
    # ÉTAPE 5 : SENSIBILITÉ DES DONNÉES
    # ==========================================
    if lang == "FR":
        st.markdown('<div class="section-header">Étape 5 : Sensibilité des données (Art. 5 let. c LPD)</div>', unsafe_allow_html=True)
        st.caption("Réf : art. 5 let. c LPD"; art. 9 al. 2 let. j et art. 89 RGPD")
        st.markdown("""
        <div style="background-color: #f1f5f9; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
        <b>Rappel légal — Sont considérées comme données sensibles les données portant sur :</b><br>
        1. Les opinions religieuses, philosophiques, politiques ou syndicales.<br>
        2. La santé, la sphère intime ou l'appartenance raciale/ethnique.<br>
        3. Les données génétiques ou les données biométriques identifiant une personne physique.<br>
        4. Les poursuites, sanctions pénales ou administratives, ou les mesures d'aide sociale.
        </div>
        """, unsafe_allow_html=True)
        e5_q = "Vos fichiers contiennent-ils au moins une de ces catégories particulières de données ?"
    else:
        st.markdown('<div class="section-header">Step 5: Data Sensitivity (Art. 5 let. c FADP)</div>', unsafe_allow_html=True)
        st.caption("Ref: Art. 5 let. c FADP")
        st.markdown("""
        <div style="background-color: #f1f5f9; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
        <b>Legal Reminder — Sensitive personal data includes data relating to:</b><br>
        1. Religious, philosophical, political, or trade union opinions.<br>
        2. Health, the intimate sphere, or racial/ethnic origin.<br>
        3. Genetic data or biometric data identifying a natural person.<br>
        4. Administrative or criminal proceedings and sanctions, or social assistance measures.
        </div>
        """, unsafe_allow_html=True)
        e5_q = "Do your files contain at least one of these special categories of data?"

    etape5_choice = st.radio(e5_q, yes_no, index=1, key="r_e5")
    
    if etape5_choice in ["Oui", "Yes"]:
        score -= 20
        etape5_sensitive = True
    else:
        etape5_sensitive = False

    st.write("---")
    
    # ==========================================
    # VERDICT ET AFFICHAGE DES RÉSULTATS
    # ==========================================
    if lang == "FR":
        st.markdown('<div class="section-header">📊 Verdict & Rapport d\'Audit</div>', unsafe_allow_html=True)
        score_lbl = "Score global de conformité"
    else:
        st.markdown('<div class="section-header">📊 Audit Report & Verdict</div>', unsafe_allow_html=True)
        score_lbl = "Global Compliance Score"
        
    final_score = max(score, 0)
    st.write(f"### **{score_lbl} : {final_score} / 100**")
    
    if final_score == 100 and not etape5_sensitive:
        st.success("🟢 PROJET ENTIÈREMENT CONFORME — RÉUTILISATION POSSIBLE" if lang == "FR" else "🟢 FULLY COMPLIANT PROJECT — REUSE PERMITTED")
        st.write("Le protocole s'aligne entièrement sur les exigences de base de la LPD, de la LPrD et du RGPD." if lang == "FR" else "The research protocol fully aligns with the statutory requirements of the FADP, LPrD, and GDPR.")
    else:
        if final_score >= 70:
            st.warning("🟧 CONFORMITÉ CONDITIONNELLE" if lang == "FR" else "🟧 CONDITIONAL COMPLIANCE")
            st.write("Traitement autorisé sous réserve de l'application immédiate des mesures correctives." if lang == "FR" else "Processing authorized subject to the immediate application of the corrective actions below.")
        else:
            st.error("🟥 RISQUE MAJEUR DE NON-CONFORMITÉ" if lang == "FR" else "🟥 HIGH NON-COMPLIANCE RISK")
            st.write("Le score est insuffisant. Le traitement informatique doit être suspendu jusqu'à correction." if lang == "FR" else "The compliance score is insufficient. Data processing must be suspended until remediated.")
        
        # Régime de Protection Renforcée (Données sensibles)
        if etape5_sensitive:
            if lang == "FR":
                st.info("🔵 RÉGIME DE PROTECTION RENFORCÉE (Art. 5 let. c LPD)")
                st.markdown("""
                **Mesures techniques de sécurité obligatoires :**
                * **Chiffrement fort obligatoire** de vos fichiers (AES-256) au repos et en transit (TLS 1.3) (art. 4 OPDo).
                * **Journalisation stricte et automatisée** de toutes les opérations d'accès (art. 4 al. 4 OPDo).
                * **Obligation réglementaire** de réaliser une Analyse d'Impact relative à la Protection des Données (AIPD) selon l'art. 22 LPD.
                """)
            else:
                st.info("🔵 ENHANCED PROTECTION REGIME (Art. 5 let. c FADP)")
                st.markdown("""
                **Mandatory technical safeguards:**
                * **Mandatory strong encryption** of data files at rest (AES-256) and in transit (TLS 1.3) (Art. 4 DPO).
                * **Strict, automated logging** of all access and data modification operations (Art. 4 al. 4 DPO).
                * **Compulsory performance** of a Data Protection Impact Assessment (DPIA) according to Art. 22 FADP.
                """)
            
        # Liste finale des actions de régularisation
        if len(actions_correctives) > 0:
            st.write("📋 **Mesures à adopter :**" if lang == "FR" else "📋 **Corrective Actions Plan:**")
            for action in actions_correctives:
                st.markdown(action)
