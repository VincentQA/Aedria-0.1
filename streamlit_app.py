import streamlit as st
import os

st.set_page_config(page_title="AedrIA", page_icon="📚")

# Titre et image de la page d'accueil
st.title("AedrIA")
# Si vous souhaitez retirer l'image d'accueil, commentez ou supprimez la ligne suivante
# st.image("images/accueil_image.jpg", use_column_width=True)
st.write("Bienvenue dans notre application de lecture interactive !")

# Liste des histoires avec leurs émojis et noms de fichiers
histoires = [
    {
        "titre": "Rencontre sur le court",
        "emoji": "🎾",
        "page": "Rencontre sur le court"
    },
    {
        "titre": "Sans état d'âme",
        "emoji": "🕵️‍♂️",
        "page": "Sans-etat-ame"
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
        # Création d'un lien vers la page de l'histoire
        page_name = histoire["page"].replace(' ', '_')
        link = f"[**{histoire['titre']}**]({os.path.join('pages', page_name + '.py')})"
        st.markdown(link, unsafe_allow_html=True)
