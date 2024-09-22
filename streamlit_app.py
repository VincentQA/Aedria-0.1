import streamlit as st

st.set_page_config(page_title="AedrIA", page_icon="📚")

# Gestion de l'état de session pour la navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Accueil'

def navigate(page_name):
    st.session_state.page = page_name

if st.session_state.page == 'Accueil':
    st.title("AedrIA")
    st.write("Bienvenue dans notre application de lecture interactive !")

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

    cols = st.columns(3)
    for idx, histoire in enumerate(histoires):
        col = cols[idx % 3]
        with col:
            st.markdown(
                f"<div style='font-size:60px; text-align:center;'>{histoire['emoji']}</div>",
                unsafe_allow_html=True
            )
            if st.button(histoire['titre'], key=histoire['titre']):
                navigate(histoire['page'])
else:
    st.title(st.session_state.page.replace('_', ' '))

    # Afficher le contenu de l'histoire sélectionnée
    if st.session_state.page == 'Rencontre_sur_le_court':
        # Code de l'histoire directement dans app.py
        st.write("Bienvenue dans l'histoire **Rencontre sur le court**.")
        # Ajoutez ici le contenu interactif de votre histoire
    elif st.session_state.page == 'Sans_etat_ame':
        st.write("Bienvenue dans l'histoire **Sans état d'âme**.")
        # Ajoutez ici le contenu interactif de votre histoire

    if st.button("Retour à l'accueil"):
        navigate('Accueil')
