import streamlit as st
from openai import OpenAI
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock 

# Retrieve API key and assistant ID from secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Initialize the OpenAI client and retrieve the assistant
client = OpenAI(api_key=OPENAI_API_KEY)
assistant = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)

# Initialize session state to store conversation history locally
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Title and introduction
st.title("🎾 Rencontre sur le court ❤️")
st.write("""
Dans un monde où la passion du tennis se mêle à des émotions tumultueuses, Léa, une jeune femme déterminée, 
doit naviguer entre ses sentiments pour Luc, un joueur mystérieux, et les complications d'une romance naissante, 
tout en affrontant ses propres démons du passé.
""")

# Display messages in chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Define the initial hidden pre-prompt for the assistant
initial_preprompt = """
Tu es un romancier de style nouvelle romance 
# Tu commences le chapitre 1 
# Prends le temps d'installer l'histoire et de bien présenter le personnage principal ainsi que le contexte. 
# Avant de commencer la rédaction ouvre et apprends les informations du chapitre du chapitre en cours dans tes knowledges 
# Je veux que tu applique sans exception les points de l'auteur : 
# A. Le chapitre doit obligatoirement inclure ( exemple La présentation de Luc par Léa, il faut que tu intègres alors à la demande de l'auteur une descirption de Luc en suivant les intructions sur comment le décrire) 
# B. Le chapitre ne peut inclure ( exemple : si une discussions entre Luc et Léa est interdite, à aucun moment tu as le droit de créer une interaction entre eux). 
# C. Choix du lecteur durant le chapitre (il est important de respecter à la lettre l'odre ainsi que la formulation des choix du lecteur par contre il faut que ce soit dans un contexte pertinent Propose une histoire cohérente avec des choix dans un contexte cohérent si le choix est une tenue propsoe le quand elle fait son sac ou en sortie de douche et surtout évite les répétitions    
"""

# Define the user pre-prompt
user_preprompt = """
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

# Function to start the story with the initial pre-prompt
def commencer_histoire():
    if st.session_state.thread_id is None:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

        # Send the initial pre-prompt to set the context
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=initial_preprompt
        )

# Button to start the story
if st.button("Commencer l'histoire"):
    commencer_histoire()

# Textbox and streaming process
if user_query := st.chat_input("Vous :"):

    # Ensure the thread is created and the pre-prompt is sent
    if st.session_state.thread_id is None:
        commencer_histoire()

    # Combine the user's input with the pre-prompt
    full_message = f"{user_preprompt}\n\nRéponse du lecteur : {user_query}"

    # Display the user's query
    with st.chat_message("user"):
        st.markdown(user_query)

    # Store the user's query into the history
    st.session_state.chat_history.append({"role": "user",
                                          "content": user_query})
    
    # Add user query to the thread with the pre-prompt
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=full_message
    )

    # Stream the assistant's reply
    with st.chat_message("assistant"):
        stream = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID,
            stream=True
        )
        
        # Empty container to display the assistant's reply
        assistant_reply_box = st.empty()
        
        # A blank string to store the assistant's reply
        assistant_reply = ""

        # Iterate through the stream 
        for event in stream:
            if isinstance(event, ThreadMessageDelta):
                if isinstance(event.data.delta.content[0], TextDeltaBlock):
                    assistant_reply_box.empty()
                    assistant_reply += event.data.delta.content[0].text.value
                    assistant_reply_box.markdown(assistant_reply)
        
        # Once the stream is over, update chat history
        st.session_state.chat_history.append({"role": "assistant",
                                              "content": assistant_reply})
