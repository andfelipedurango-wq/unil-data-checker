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

st.markdown('<div class="main-title">⚖️ Data-Checker</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Système expert d\'audit automatisé pour la réutilisation des données de recherche</div>',
    unsafe_allow_html=True)
st.write("---")

# ==========================================
# MODULE INITIAL : VERROU DE COMPÉTENCE (ART. 2 LRH)
# ==========================================
st.markdown('<div class="section-header">📋 Évaluation de compétence (Art. 2 LRH)</div>', unsafe_allow_html=True)
st.markdown("""
<div class="legal-text">
<b>Art. 2 Champ d’application (LRH) :</b> La présente loi s’applique à la recherche sur les maladies humaines et sur la structure et le fonctionnement du corps humain.
</div>
""", unsafe_allow_html=True)

lrh_selection = st.radio(
    "Votre recherche est-elle pratiquée sur l'un des éléments suivants (Art. 2 al. 1 LRH) ?",
    [
        "a. Sur des personnes",
        "b. Sur des personnes décédées",
        "c. Sur des embryons et des fœtus",
        "d. Sur du matériel biologique non anonymisé",
        "e. Sur des données personnelles liées à la santé non anonymisées",
        "Aucun de ces éléments (Art. 2 al. 2 / Données anonymes)"
    ],
    index=5
)

if "Aucun de ces éléments" not in lrh_selection:
    st.error("🛑 VERROU ALGORITHMIQUE — APPLICATION DE LA LRH (LEX SPECIALIS)")
    st.markdown("""
    En vertu de l'art. 2 al. 1 LRH, votre projet entre dans le champ d'application de la recherche humaine. 
    Ce projet sort du cadre d'évaluation de cet outil général. Vous devez obligatoirement saisir la **CER-VD** (art. 51 al. 1 LRH).
    """)
    st.stop()
else:
    st.success("✔ Loi non applicable (Art. 2 al. 2 LRH). Régime général déverrouillé.")

st.write("---")

# Initialisation des variables de notation
score = 100
actions_correctives = []

# ==========================================
# MODULE RATTACHEMENT INSTITUTIONNEL (UNIL vs EXTERNE)
# ==========================================
st.markdown('<div class="section-header">🏫 Affiliation Institutionnelle</div>', unsafe_allow_html=True)
unil_check = st.radio(
    "Êtes-vous chercheur ou rattaché à l'UNIL ?",
    ["Oui, je suis membre de l'UNIL (Régime Directives internes)", "Non, chercheur externe"],
    index=0
)
is_unil = "Oui" in unil_check

st.write("---")

# ==========================================
# ÉTAPE 1 : VÉRIFICATION INITIALE DES DONNÉES
# ==========================================
st.markdown('<div class="section-header">Étape 1 : Vérification des données</div>', unsafe_allow_html=True)
etape1_option = st.selectbox(
    "Quelle est la nature juridique des fichiers de données ?",
    [
        "Sélectionnez une option...",
        "Données pseudonymisées ou codées",
        "Données anonymisées",
        "Données personnelles brutes"
    ]
)

if "Données anonymisées" in etape1_option:
    st.balloons()
    st.success("🟢 VERDICT : RÉUTILISATION LIBRE (Score : 100/100)")
    st.markdown("""
    Les données anonymes ne tombent pas sous le champ d'application de la LPD (art. 5 let. a) ni du RGPD. Réutilisation libre.
    """)
    st.stop()

elif "Sélectionnez" in etape1_option:
    st.warning("Veuillez sélectionner la nature des données.")
    st.stop()

else:
    st.write("---")

    # ==========================================
    # ÉTAPE 2 : DONNÉES SECONDAIRES
    # ==========================================
    st.markdown('<div class="section-header">Étape 2 : Données secondaires (Compatibilité de la finalité)</div>',
                unsafe_allow_html=True)
    st.caption("Réf : art. 6 al. 3 LPD ; art. 5 al. 1 let. b RGPD")
    etape2_choice = st.radio(
        "La nouvelle finalité scientifique de recherche est-elle compatible avec la finalité initiale de la collecte ?",
        ["Oui", "Non"], index=0, key="r_e2")

    if etape2_choice == "Non":
        score -= 25
        actions_correctives.append(
            "❌ **Action Étape 2 :** [LPD] Rupture du principe de finalité. Nouveau consentement requis ou mise à jour immédiate du cadre d'accord des participants.")

    # ==========================================
    # ÉTAPE 3 : COUVERTURE DU CONSENTEMENT
    # ==========================================
    st.markdown('<div class="section-header">Étape 3 : Couverture du consentement initial</div>',
                unsafe_allow_html=True)
    st.caption("Réf : art. 12 LPrD ; art. 6 al. 6 LPD")
    etape3_choice = st.radio(
        "Le consentement initial existant couvre-t-il expressément ou implicitement cette nouvelle finalité ?",
        ["Oui", "Non"], index=0, key="r_e3")

    if etape3_choice == "Non":
        score -= 25
        actions_correctives.append(
            "❌ **Action Étape 3 :** [LPD] Défaut de couverture du consentement. Obligation d'obtenir un nouveau consentement écrit et exprès auprès des personnes concernées.")

    # ==========================================
    # ÉTAPE 4 : STOCKAGE ET TRANSFERT INTERNATIONAL
    # ==========================================
    st.markdown('<div class="section-header">Étape 4 : Stockage et Transfert International</div>',
                unsafe_allow_html=True)
    st.caption("Réf : art. 16 LPD ; art. 46 RGPD")
    etape4_choice = st.radio(
        "Avez-vous validé la présence de garanties suffisantes ou de Clauses Contractuelles Types (CCT) pour le stockage externe ?",
        ["Oui", "Non"], index=0, key="r_e4")

    if etape4_choice == "Non":
        score -= 25
        if is_unil:
            actions_correctives.append(
                "❌ **Action Étape 4 : [Directive UNIL 4.5 & Art. 4 OPDo]** Risque de transfert international illicite. Vous devez impérativement rapatrier et stocker vos fichiers sur l'infrastructure de stockage centralisée sécurisée de l'UNIL (**serveur NAS de l'Amphimax**), gérée par le Centre Informatique (Ci-UNIL), garantissant la localisation des données en Suisse.")
        else:
            actions_correctives.append(
                "❌ **Action Étape 4 :** [LPD] Risque de transfert transfrontalier sans base légale. Obligation d'activer des Clauses Contractuelles Types (CCT) approuvées par le PFPDT ou d'utiliser un hébergement suisse souverain sécurisé (art. 4 OPDo).")

    # Application de la Directive UNIL 4.1
    if is_unil:
        st.write("---")
        st.markdown('<div><b>ℹ️ Contrôle de gouvernance institutionnelle activé (Directive UNIL 4.1)</b></div>',
                    unsafe_allow_html=True)
        unil_contract_choice = st.radio(
            "Si un sous-traitant externe ou tiers manipule les données, un contrat de traitement conforme à la Directive UNIL 4.1 a-t-il été signé ?",
            ["Oui", "Non"], index=0, key="r_unil41")

        if unil_contract_choice == "Non":
            score -= 10
            actions_correctives.append(
                "❌ **Gouvernance : [Directive UNIL 4.1]** Manquement de gouvernance contractuelle. Toute sous-traitance de données de recherche requiert la signature d'une convention de traitement standardisée validée par le **Service juridique de l'UNIL** avant le début des opérations informatique.")

    # ==========================================
    # ÉTAPE 5 : SENSIBILITÉ DES DONNÉES
    # ==========================================
    st.markdown('<div class="section-header">Étape 5 : Sensibilité des données</div>', unsafe_allow_html=True)
    st.caption("Réf : art. 5 let. c LPD")
    etape5_choice = st.radio(
        "Mon projet implique-t-il le traitement de données sensibles ou de catégories particulières ?", ["Oui", "Non"],
        index=1, key="r_e5")

    if etape5_choice == "Oui":
        score -= 20
        etape5_sensitive = True
    else:
        etape5_sensitive = False

    st.write("---")

    # ==========================================
    # VERDICT ET AFFICHAGE DES RÉSULTATS
    # ==========================================
    st.markdown('<div class="section-header">📊 Verdict & Rapport d\'Audit</div>', unsafe_allow_html=True)

    final_score = max(score, 0)
    st.write(f"### **Score global de conformité : {final_score} / 100**")

    if final_score == 100 and not etape5_sensitive:
        st.success("🟢 PROJET ENTIÈREMENT CONFORME — RÉUTILISATION POSSIBLE")
        st.write("Le protocole s'aligne entièrement sur les exigences de base de la LPD, de la LPrD et du RGPD.")
    else:
        if final_score >= 70:
            st.warning("🟧 CONFORMITÉ CONDITIONNELLE")
            st.write("Traitement autorisé sous réserve de l'application immédiate des mesures correctives.")
        else:
            st.error("🟥 RISQUE MAJEUR DE NON-CONFORMITÉ")
            st.write("Le score est insuffisant. Le traitement informatique doit être suspendu jusqu'à correction.")

        # Régime de Protection Renforcée (Données sensibles)
        if etape5_sensitive:
            st.info("🔵 RÉGIME DE PROTECTION RENFORCÉE (Art. 5 let. c LPD)")
            st.markdown("""
            **Mesures techniques de sécurité obligatoires :**
            * **Chiffrement fort obligatoire** de vos fichiers de données au repos (AES-256) et en transit (TLS 1.3) (art. 4 OPDo).
            * **Journalisation stricte et automatisée** de toutes les opérations d'accès et de modification des fichiers (art. 4 al. 4 OPDo).
            * **Obligation réglementaire** de réaliser une Analyse d'Impact relative à la Protection des Données (AIPD) selon l'art. 22 LPD.
            """)

        # Liste finale des actions de régularisation
        if len(actions_correctives) > 0:
            st.write("📋 **Mesures à adopter :**")
            for action in actions_correctives:
                st.markdown(action)
