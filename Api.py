import re
from google import genai
from google.genai import types
import chromadb


client = genai.Client(api_key="YOU'R_API_KEY")
chromadb_client = chromadb.Client()

if chromadb_client.list_collections() == []:
    collection = chromadb_client.create_collection(name="collection")
else:
    collection = chromadb_client.get_collection(name="collection")

collection.add(
    documents=[
        "Nuestra empresa ofrece servicios de programación y desarrollo de software.",
        "Ofrecemos servicios de desarrollo web y móvil.",
        "Hacemos aplicaciones personalizadas para empresas.",
        "Hacemos páginas web con wordpress.",
        "Los precios dependen del tipo de proyecto y la escala.",
        "Ofrecemos hospedaje web y dominios.",
    ],
    ids=["id1", "id2", "id3", "id4", "id5", "id6"]
)

MODEL_ID = "gemini-2.0-flash"

system_instruction = """
                        Eres un asistente de programación.
                        Da respuestas de 1 a 2 lineas.
                        Si no sabes la respuesta, di que no sabes.
                    """

chat_config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=0.2,
)

chat = client.chats.create(
    model=MODEL_ID,
    config=chat_config,
)

def get_relevant_passage(query):
    # Search for the most relevant passage in the collection
    results = collection.query(
        query_texts=[ query ], 
        n_results=2
    )
    # Extract the relevant passage from the results
    relevant_passage = results["documents"][0]
    return relevant_passage

def make_rag_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = ("""Eres un asistente de ventas para una empresa de programación. \
            Ten siempre en cuenta que eres un chat y que estas en una conversación. \
            Responde teniendo en cuenta preguntas y respuestas anteriores. \
            Tu objetivo es ayudar a los clientes a entender los servicios que ofrecemos. \
            Siempre termina tus respuestas con una pregunta para mantener la conversación e intentar vender el producto. \
            Da respuestas de 4 a 5 lineas si no te piden respuestas largas explicitamente. \
            No utilizes el contexto de PASSAGE de manera literal \
            Si el contexto de PASSAGE no es relevante, no lo uses. \
            QUESTION: '{query}'
            PASSAGE: '{relevant_passage}'
            ANSWER:
         """).format(query=query, relevant_passage=escaped)

  return prompt

def get_question(response):
    reguex = r"¿[^¿?]+?\?"
    match = re.findall(reguex, response)
    return match[0]

def get_answer(question):
    relevant_passage_list = get_relevant_passage(question)
    relevant_passage = relevant_passage_list[0] + " " + relevant_passage_list[1]
    response = chat.send_message(make_rag_prompt(question, relevant_passage))
    return response.text

