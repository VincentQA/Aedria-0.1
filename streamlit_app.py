import streamlit as st
import os
from openai import OpenAI

# Access the OpenAI API key from the secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Set up the OpenAI API client
client = OpenAI(api_key=api_key)

# Initialiser les variables de session pour stocker la conversation et le statut du bouton
if "conversation" not in st.session_state:
    st.session_state.conversation = ""

if "has_started" not in st.session_state:
    st.session_state.has_started = False

# Créer l'interface Streamlit avec le nouveau titre et la description
st.title("🎾 Rencontre sur le court ❤️")
st.write("""
Dans un monde où la passion du tennis se mêle à des émotions tumultueuses, Léa, une jeune femme déterminée, 
doit naviguer entre ses sentiments pour Luc, un joueur mystérieux, et les complications d'une romance naissante, 
tout en affrontant ses propres démons du passé.
""")

# Utiliser un conteneur vide pour afficher la conversation
conversation_container = st.empty()

def envoyer_message(user_input, add_to_chat=True):
    hidden_text = """
Tu es un romancier de style nouvelle romance.
Prends le temps d'avancer dans l'histoire et surtout de tenir compte des choix du lecteur dans ta réponse. 
Avant de commencer la rédaction, ouvre et apprends les informations du chapitre en cours dans tes knowledges. 
Je veux que tu appliques sans exception les points de l'auteur :
A. Le chapitre doit obligatoirement inclure (exemple : La présentation de Luc par Léa, il faut que tu intègres alors à la demande de l'auteur une description de Luc en suivant les instructions sur comment le décrire).
B. Le chapitre ne peut inclure (exemple : si une discussion entre Luc et Léa est interdite, à aucun moment tu as le droit de créer une interaction entre eux).
C. Choix du lecteur durant le chapitre (il est important de poser à la lettre au mot près les choix du lecteur, mais il faut que ce soit dans un contexte pertinent. Propose une histoire cohérente avec des choix dans un contexte cohérent. Si le choix est une tenue, propose-le quand elle fait son sac ou en sortie de douche et surtout évite les répétitions).
N'oublie pas, tu dois respecter coûte que coûte ce que tu dois inclure mais surtout ne pas inclure dans le chapitre. 
Évite toute répétition avec ce que tu as déjà écrit. Ton rôle est de présenter une histoire cohérente jusqu'au choix et surtout d'éviter les répétitions. Chacune de tes interventions doit faire au minimum 4 gros paragraphes. 
S'il ne reste plus qu'une interaction dans le chapitre, tu dois lancer le chapitre suivant dans ta réponse et donc ouvrir également le document en question.
"""
    reader_response_prefix = "Réponse du lecteur : "
    full_message = f"{hidden_text}\n\n{reader_response_prefix}{user_input}"
    
    if add_to_chat:
        st.session_state.conversation += f"**Vous :** {user_input}\n\n"
    
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=full_message
    )
    
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id="asst_JWbCk8ZWNC2OgWwieWYuCgmQ"
    )

    if run.status == 'completed': 
        messages = list(client.beta.threads.messages.list(thread_id=thread.id))
        for message in messages:
            if message.role == "assistant":
                for content_block in message.content:
                    if content_block.type == 'text':
                        st.session_state.conversation += f"{content_block.text.value}\n\n"

        conversation_container.markdown(st.session_state.conversation, unsafe_allow_html=True)
    else:
        st.text(f"Le run est en cours, statut actuel : {run.status}")

def commencer_histoire():
    initial_message = """
Tu es un romancier de style nouvelle romance 
# Tu commences le chapitre 1 
# Prends le temps d'installer l'histoire et de bien présenter le personnage principal ainsi que le contexte. 
# Avant de commencer la rédaction ouvre et apprends les informations du chapitre du chapitre en cours dans tes knowledges 
# Je veux que tu applique sans exception les points de l'auteur : 
# A. Le chapitre doit obligatoirement inclure ( exemple La présentation de Luc par Léa, il faut que tu intègres alors à la demande de l'auteur une descirption de Luc en suivant les intructions sur comment le décrire) 
# B. Le chapitre ne peut inclure ( exemple : si une discussions entre Luc et Léa est interdite, à aucun moment tu as le droit de créer une interaction entre eux). 
# C. Choix du lecteur durant le chapitre (il est important de respecter à la lettre l'odre ainsi que la formulation des choix du lecteur par contre il faut que ce soit dans un contexte pertinent Propose une histoire cohérente avec des choix dans un contexte cohérent si le choix est une tenue propsoe le quand elle fait son sac ou en sortie de douche et surtout évite les répétitions    
 """
    envoyer_message(initial_message, add_to_chat=False)
    st.session_state.has_started = True  # Marque que l'histoire a commencé

# Bouton pour commencer l'histoire
if not st.session_state.has_started:
    if st.button("Commencer l'histoire"):
        commencer_histoire()
else:
    st.button("Commencer l'histoire", disabled=True)

# Afficher la conversation initiale
conversation_container.markdown(st.session_state.conversation, unsafe_allow_html=True)

# Champ de saisie pour entrer d'autres messages
user_input = st.text_input("Vous :")

# Bouton pour envoyer un message
if st.button("Envoyer"):
    if user_input:
        envoyer_message(user_input)
        conversation_container.markdown(st.session_state.conversation, unsafe_allow_html=True)
