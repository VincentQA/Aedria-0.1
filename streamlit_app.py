import streamlit as st

st.set_page_config(page_title="AedrIA", page_icon="📚")

# Gestion des paramètres de requête pour la navigation
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Accueil"])[0]

if page == "Accueil":
    # Titre et message de bienvenue
    st.title("AedrIA")
    st.write("Bienvenue dans notre application de lecture interactive !")

    # Liste des histoires avec leurs émojis et noms de pages
    histoires = [
        {
            "titre": "Rencontre sur le court",
            "emoji": "🎾",
            "page": "Rencontre_sur_le_court"
        },
        {
            "titre": "Sans état d'âme",
            "emoji": "🕵️‍♂️",
            "page": "Sans_etat_ame"
        },
        # Ajoutez d'autres histoires ici
    ]

    # Affichage des vignettes sous forme de grille
    cols = st.columns(3)
    for idx, histoire in enumerate(histoires):
        col = cols[idx % 3]
        with col:
            # Afficher l'émoji à la place de l'image
            st.markdown(
                f"<div style='font-size:60px; text-align:center;'>{histoire['emoji']}</div>",
                unsafe_allow_html=True
            )
            # Création d'un lien vers la page de l'histoire en utilisant les paramètres de requête
            link = f"[**{histoire['titre']}**](/?page={histoire['page']})"
            st.markdown(link, unsafe_allow_html=True)
else:
    # Afficher la page de l'histoire sélectionnée
    st.title(page.replace('_', ' '))

    # Charger le contenu spécifique de la page
    if page == 'Rencontre_sur_le_court':
        st.write("Contenu de l'histoire **Rencontre sur le court**...")
        # Ajoutez ici le code spécifique à cette histoire
    elif page == 'Sans_etat_ame':
        st.write("Contenu de l'histoire **Sans état d'âme**...")
        # Ajoutez ici le code spécifique à cette histoire
    else:
        st.error("Page non trouvée.")

    # Ajouter un lien pour revenir à l'accueil
    st.markdown("[Retour à l'accueil](/?page=Accueil)")
