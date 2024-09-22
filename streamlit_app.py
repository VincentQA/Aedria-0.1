import streamlit as st

st.set_page_config(page_title="AedrIA", page_icon="📚")

# Titre et image de la page d'accueil
st.title("AedrIA")
st.image("images/accueil_image.jpg", use_column_width=True)  # Remplacez par le nom de votre image

st.write("Bienvenue dans notre application de lecture interactive !")

# Liste des histoires avec leurs images et noms de fichiers
histoires = [
    {
        "titre": "Rencontre sur le court",
        "image": "images/couverture_rencontre.jpg",
        "page": "encontre_sur_le_court"
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
        if st.button(histoire["titre"], key=idx):
            st.experimental_set_query_params(page=histoire["page"])
            st.experimental_rerun()
