import streamlit as st
from openai import OpenAI
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock
import time 

# Récupération des clés API et des identifiants des assistants depuis les secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
ASSISTANT_ID_SCENARISTE_NA_RSLC = st.secrets["ASSISTANT_ID_SCENARISTE_NA"]
ASSISTANT_ID_ECRIVAIN_RSLC = st.secrets["ASSISTANT_ID_ECRIVAIN"]

# Initialisation du client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Nombre maximum d'interactions autorisées
MAX_INTERACTIONS = 3

# Initialisation de l'état de la session pour stocker l'historique des conversations et les threads
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thread_ID_SCENARISTE_NA" not in st.session_state:
    st.session_state.thread_ID_SCENARISTE_NA = None
if "thread_id_ecrivain" not in st.session_state:
    st.session_state.thread_id_ecrivain = None
if "story_started" not in st.session_state:
    st.session_state.story_started = False
if "checkpoint" not in st.session_state:
    st.session_state.checkpoint = 1  # Suivi du checkpoint actuel
# Initialisation du compteur d'interactions
if "interaction_count" not in st.session_state:
    st.session_state.interaction_count = 0

# Titre de l'application
st.title("👨‍💻 Le nouvel assistant")
st.subheader("Une aventure interactive où vos choix façonnent l'histoire")
st.markdown("Votre avis est précieux ! Partagez vos impressions et aidez-nous à améliorer l'application en répondant à notre questionnaire rapide.")
if st.button('Répondre au questionnaire'):
    st.write('[Cliquez ici pour accéder au questionnaire](https://forms.gle/4FiNG71ZP7bWFcV4A)')

# Fonction pour créer un nouveau thread pour un assistant s'il n'existe pas encore
def initialize_thread(assistant_role):
    if assistant_role == "scenariste":
        if st.session_state.thread_ID_SCENARISTE_NA is None:
            thread = client.beta.threads.create()
            st.session_state.thread_ID_SCENARISTE_NA = thread.id
    elif assistant_role == "ecrivain":
        if st.session_state.thread_id_ecrivain is None:
            thread = client.beta.threads.create()
            st.session_state.thread_id_ecrivain = thread.id

# Fonction pour envoyer un message et diffuser la réponse en continu
def send_message_and_stream(assistant_id, assistant_role, user_input):
    # Initialiser le thread si nécessaire
    initialize_thread(assistant_role)
    thread_id = st.session_state.thread_ID_SCENARISTE_NA if assistant_role == "scenariste" else st.session_state.thread_id_ecrivain
    # Ajouter le message utilisateur au thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )
    # Créer le run et streamer la réponse de l'assistant
    assistant_reply = ""
    # N'afficher que les réponses de l'écrivain
    if assistant_role == "ecrivain":
        with st.chat_message("assistant"):
            stream = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                stream=True
            )
            # Boîte vide pour afficher la réponse
            assistant_reply_box = st.empty()
            # Itération à travers le stream pour récupérer la réponse au fur et à mesure
            for event in stream:
                if isinstance(event, ThreadMessageDelta):
                    if event.data.delta.content and isinstance(event.data.delta.content[0], TextDeltaBlock):
                        assistant_reply += event.data.delta.content[0].text.value
                        assistant_reply_box.markdown(assistant_reply)
            # Ajouter la réponse finale à l'historique de la conversation
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
    else:
        # Si c'est le scénariste, on attend simplement la réponse sans l'afficher
        stream = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            stream=True
        )
        for event in stream:
            if isinstance(event, ThreadMessageDelta):
                if event.data.delta.content and isinstance(event.data.delta.content[0], TextDeltaBlock):
                    assistant_reply += event.data.delta.content[0].text.value
    # Retourner la réponse complète de l'assistant
    return assistant_reply

# Fonction pour démarrer l'histoire avec le scénariste sans prendre en compte une réponse du lecteur
def start_story():
    st.session_state.story_started = True
    st.session_state.checkpoint = 1  # Réinitialiser au checkpoint 1
    st.session_state.interaction_count = 0  # Réinitialiser le compteur d'interactions
    # Afficher le message d'attente
    waiting_message = st.empty()
    waiting_message.info("Votre histoire est en train de s'écrire...")
    # Envoyer un message simple pour démarrer l'histoire
    user_input = "Commence le plan pour le checkpoint 1."
    scenariste_plan = send_message_and_stream(ASSISTANT_ID_SCENARISTE_NA_RSLC, "scenariste", user_input)
    # Après avoir récupéré le plan, envoyer ce plan à l'écrivain
    send_message_and_stream(ASSISTANT_ID_ECRIVAIN_RSLC, "ecrivain", f"Voici le plan : {scenariste_plan}. Développe le checkpoint en suivant le plan")
    # Supprimer le message d'attente
    waiting_message.empty()

# Fonction pour gérer le passage du plan scénariste à l'écrivain
def generate_plan_and_pass_to_writer(user_input):
    # Afficher le message d'attente
    waiting_message = st.empty()
    waiting_message.info("Votre histoire est en train de s'écrire...")
    # Préparer le pré-prompt pour le scénariste avec l'instruction explicite de passer au checkpoint suivant
    scenariste_prompt = f"Le lecteur a répondu : {user_input}. Passe maintenant au checkpoint suivant : {st.session_state.checkpoint + 1}. Adapte le plan du checkpoint en fonction de la réponse du lecteur."
    # Envoyer le message pour générer le plan avec le scénariste
    scenariste_plan = send_message_and_stream(ASSISTANT_ID_SCENARISTE_NA_RSLC, "scenariste", scenariste_prompt)
    # Après avoir récupéré le plan, envoyer ce plan à l'écrivain
    send_message_and_stream(ASSISTANT_ID_ECRIVAIN_RSLC, "ecrivain", f"Voici le plan : {scenariste_plan}. Assure toi de la cohérence entre la transition du choix du lecteur et du plan en cours")
    # Incrémenter le checkpoint
    st.session_state.checkpoint += 1
    # Supprimer le message d'attente
    waiting_message.empty()

# Affichage de l'historique des messages dans le chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Afficher le bouton pour démarrer l'histoire
if not st.session_state.story_started:
    if st.button("Lancer l'histoire"):
        start_story()

# Gestion des choix du lecteur et progression des checkpoints
if st.session_state.story_started:
    user_query = st.chat_input("Faites votre choix :", disabled=st.session_state.interaction_count >= MAX_INTERACTIONS)
    if user_query is not None and user_query.strip() != '' and st.session_state.interaction_count < MAX_INTERACTIONS:
        with st.chat_message("user"):
            st.markdown(user_query)
        # Incrémenter le compteur d'interactions
        st.session_state.interaction_count += 1
        # Stocker la réponse du lecteur dans l'historique de conversation
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        # Envoyer le choix du lecteur au scénariste pour générer un nouveau plan et passer à l'écrivain
        generate_plan_and_pass_to_writer(user_query)
    elif st.session_state.interaction_count >= MAX_INTERACTIONS:
        st.info(" Vous êtes arrivés au bout de l'histoire, la suite arrive dans quelques jours")
