from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import os
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

ASSISTANT_ID = "asst_6yZpg5l9jPmsgmJzAyyMh53p"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client_threads = {}

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ChatMessage
import time

client_threads = {}  # Asegúrate de que este diccionario esté accesible

@api_view(['POST'])
def openai_chat(request):
    client_id = request.data.get('client_id')
    user_message = request.data.get('message', 'Quien eres')

    if not client_id:
        return Response({'error': 'No client_id provided'}, status=400)

    try:
        # Guardar el mensaje del usuario en la base de datos
        user_chat_message = ChatMessage(
            user_id=None,  # No se usa un ID de usuario por el momento
            message=user_message,
            is_agent_response=False
        )
        user_chat_message.save()

        # Crear o continuar el hilo de conversación para el usuario
        if client_id in client_threads:
            thread_id = client_threads[client_id]
        else:
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ]
            )
            thread_id = thread.id
            client_threads[client_id] = thread_id

        # Iniciar y esperar la respuesta del agente
        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=ASSISTANT_ID)
        print(f"👉 Run Created: {run.id}")

        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            print(f"🏃 Run Status: {run.status}")
            time.sleep(1)
        else:
            print(f"🏁 Run Completed!")

        # Obtener la respuesta del agente
        message_response = client.beta.threads.messages.list(thread_id=thread_id)
        messages = message_response.data

        if messages:
            latest_message = messages[0]
            response_content = latest_message.content[0].text.value
        else:
            response_content = "No response received."

        # Guardar la respuesta del agente en la base de datos
        agent_chat_message = ChatMessage(
            user_id=None,  # Igual que antes, sin un ID de usuario específico
            message=response_content,
            is_agent_response=True
        )
        agent_chat_message.save()

        # Responder al cliente
        return Response({'response': response_content})

    except Exception as e:
        return Response({'error': str(e)}, status=500)



def render_history_chat(request):
    return render(request,'test_chat_history.html')