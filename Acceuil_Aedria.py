import streamlit as st
import urllib.parse

st.set_page_config(page_title="AedrIA", page_icon="📚")

st.title("AedrIA")
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

# Définir le nombre de colonnes en fonction de la largeur de l'écran
num_cols = 3  # Vous pouvez ajuster ce nombre pour plus ou moins de colonnes

cols = st.columns(num_cols)
for idx, histoire in enumerate(histoires):
    col = cols[idx % num_cols]
    with col:
        route = histoire['route']
        route_encoded = urllib.parse.quote(route)
        # Créer un lien qui enveloppe toute la case
        # Utiliser st.markdown avec du HTML

        # Créer un HTML pour la case
        case_html = f"""
        <a href='/{route_encoded}' style='text-decoration: none; color: inherit;'>
            <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; margin: 10px; transition: transform 0.2s;'>
                <div style='font-size:60px; text-align: center;'>{histoire['emoji']}</div>
                <div style='font-size:18px; font-weight:bold; text-align: center;'>{histoire['titre']}</div>
            </div>
        </a>
        <style>
        a:hover div {{
            transform: scale(1.05);
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}
        @media only screen and (max-width: 600px) {{
            div {{
                padding: 10px;
            }}
        }}
        </style>
        """
        st.markdown(case_html, unsafe_allow_html=True)
