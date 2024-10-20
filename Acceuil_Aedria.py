import streamlit as st
import urllib.parse

st.set_page_config(page_title="AedrIA", page_icon="📚")

st.title("AedrIA")
st.write("Bienvenue dans notre application de lecture interactive !")

st.markdown("Votre avis est précieux ! Partagez vos impressions et aidez-nous à améliorer l'application en répondant à notre questionnaire rapide.")
if st.button('Répondre au questionnaire'):
    st.write('[Cliquez ici pour accéder au questionnaire](https://forms.gle/4FiNG71ZP7bWFcV4A)')

st.sidebar.success("Sélectionnez une histoire dans le menu ci-dessus.")

# Liste des histoires avec leurs émojis, routes, descriptions et genres
histoires = [
    {
        "titre": "La légende du loup blanc",
        "emoji": "🐺",
        "route": "légende_loup_blanc",
        "description": "Aléna, une jeune guérisseuse du village de Valoria, sauve Lucian, un étranger mystérieux.",
        "genre": "Romance Fantastique"
    },
    {
        "titre": "Le nouvel assistant",
        "emoji": "👨‍💻",
        "route": "Nouvel_Assistant",
        "description": "Chloé, une chef de projet ambitieuse et perfectionniste, voit son quotidien bouleversé par l'arrivée de Lucas, un nouvel assistant maladroit mais bien intentionné.",
        "genre": "Comédie-romantique"
    },
 {
        "titre": "Les lettres de l'ombre",
        "emoji": "✉️",
        "route": "Les_lettres_de_l_ombre",
        "description": "L'héritière d'une grande fortune, reçoit des menaces anonymes. Son père engage Mathieu, un garde du corps sérieux et protecteur. Simultanément, son ami d'enfance revenu après des années d'absence.",
        "genre": "Romance suspence"
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
                <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; margin: 10px; transition: transform 0.2s; min-height: 350px; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; align-items: center; box-sizing: border-box; background-color: white; text-align: center; color: black;'>
                    <div style='font-size:60px;'>{histoire['emoji']}</div>
                    <div style='font-size:18px; font-weight:bold;'>{histoire['titre']}</div>
                    <div style='font-size:14px; margin-top: 10px;'>{histoire['description']}</div>
                    <div style='font-size:12px; font-style:italic; margin-top: 5px;'>Genre: {histoire['genre']}</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
