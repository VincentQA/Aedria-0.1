import streamlit as st
import urllib.parse

st.set_page_config(page_title="AedrIA", page_icon="📚")

st.title("AedrIA")
st.write("Bienvenue dans notre application de lecture interactive !")

st.sidebar.success("Sélectionnez une histoire dans le menu ci-dessus.")

# Liste des histoires avec leurs émojis, routes, descriptions et genres
histoires = [
    {
        "titre": "La légende du loup blanc",
        "emoji": "🐺",
        "route": "légende_loup_blanc",
        "description": "Une quête épique à travers des forêts enneigées pour découvrir les secrets d'un loup mythique.",
        "genre": "Fantasy"
    },
    {
        "titre": "Sous les masques du désir",
        "emoji": "🎹",
        "route": "sous_les_masques_du_désir",
        "description": "Un mystère romantique où la musique et les secrets se mêlent pour révéler des vérités cachées.",
        "genre": "Romance"
    },
    {
        "titre": "Le nouvel assistant",
        "emoji": "👨‍💻",
        "route": "Nouvel_Assistant",
        "description": "Un assistant IA révolutionnaire qui change la vie de son créateur d'une manière inattendue.",
        "genre": "Science-fiction"
    },
    
    # Ajoutez d'autres histoires ici
]

# Affichage des vignettes sous forme de grille
st.write("### Sélectionnez une histoire :")

# Définir le nombre de colonnes
num_cols = 3  # Vous pouvez ajuster ce nombre pour plus ou moins de colonnes

cols = st.columns(num_cols)
for idx, histoire in enumerate(histoires):
    col = cols[idx % num_cols]
    with col:
        route = histoire['route']
        route_encoded = urllib.parse.quote(route)
        st.markdown(f"""
            <a href='/{route_encoded}' style='text-decoration: none; color: inherit;'>
                <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; margin: 10px; transition: transform 0.2s; min-height: 300px; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; align-items: center; box-sizing: border-box; background-color: white; text-align: center; color: black;'>
                    <div style='font-size:60px;'>{histoire['emoji']}</div>
                    <div style='font-size:18px; font-weight:bold;'>{histoire['titre']}</div>
                    <div style='font-size:14px; margin-top: 10px;'>{histoire['description']}</div>
                    <div style='font-size:12px; font-style:italic; margin-top: 5px;'>Genre: {histoire['genre']}</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
