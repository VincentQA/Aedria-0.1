import streamlit as st
import urllib.parse  # Importation du module pour encoder les URL

st.set_page_config(page_title="AedrIA", page_icon="📚")

# Titre et image d'accueil
st.title("AedrIA")
# Si vous avez une image d'accueil, décommentez la ligne suivante
# st.image("images/accueil_image.jpg", use_column_width=True)
st.write("Bienvenue dans notre application de lecture interactive !")

st.sidebar.success("Sélectionnez une histoire dans le menu ci-dessus.")

# Liste des histoires avec leurs émojis et routes
histoires = [
    {
        "titre": "Rencontre sur le court",
        "emoji": "🎾",
        "route": "Rencontre_sur_le_court"
    },
    {
        "titre": "Sans état d'âme",
        "emoji": "🕵️‍♂️",
        "route": "Sans_état_d'âme"
    },
    # Ajoutez d'autres histoires ici
]

# Affichage des vignettes sous forme de grille
st.write("### Sélectionnez une histoire :")

cols = st.columns(3)
for idx, histoire in enumerate(histoires):
    col = cols[idx % 3]
    with col:
        # Afficher l'émoji en grand
        st.markdown(
            f"<div style='font-size:60px; text-align:center;'>{histoire['emoji']}</div>",
            unsafe_allow_html=True
        )
        # Créer un lien vers la page de l'histoire
        route = histoire['route']
        # Encoder la route pour une URL correcte
        route_encoded = urllib.parse.quote(route)
        link = f"[**{histoire['titre']}**](/{route_encoded})"
        st.markdown(f"<div style='text-align: center;'>{link}</div>", unsafe_allow_html=True)
