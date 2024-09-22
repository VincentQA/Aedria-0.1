import streamlit as st
import os

st.set_page_config(page_title="AedrIA", page_icon="📚")

# Titre et image de la page d'accueil
st.title("AedrIA")
st.image("images/accueil_image.jpg", use_column_width=True)  # Remplacez par le nom de votre image d'accueil
st.write("Bienvenue dans notre application de lecture interactive !")

# Liste des histoires avec leurs images et noms de fichiers
histoires = [
    {
        "titre": "Rencontre sur le court",
        "image": "images/couverture_rencontre.jpg",
        "page": "Rencontre sur le court"
    },
   {
        "titre": "Sans état d'âme",
        "image": "images/couverture_rencontre.jpg",
        "page": "Sans-etat-ame"
    },
    # Ajoutez d'autres histoires ici

]

# Affichage des vignettes sous forme de grille
cols = st.columns(3)
for idx, histoire in enumerate(histoires):
    col = cols[idx % 3]
    with col:
        st.image(histoire["image"], use_column_width=True)
        # Création d'un lien vers la page de l'histoire
        page_name = histoire["page"].replace(' ', '_')
        link = f"[**{histoire['titre']}**]({os.path.join('pages', page_name + '.py')})"
        st.markdown(link, unsafe_allow_html=True)
    
