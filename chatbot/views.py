from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

ASSISTANT_ID = "asst_6yZpg5l9jPmsgmJzAyyMh53p"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client_threads = {}

@api_view(['POST'])
def openai_chat(request):
    client_id = request.data.get('client_id')
    user_message = request.data.get('message', 'Quien eres')

    if not client_id:
        return Response({'error': 'No client_id provided'}, status=400)

    try:
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

        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=ASSISTANT_ID)
        print(f"👉 Run Created: {run.id}")

        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            print(f"🏃 Run Status: {run.status}")
            time.sleep(1)
        else:
            print(f"🏁 Run Completed!")

        message_response = client.beta.threads.messages.list(thread_id=thread_id)
        messages = message_response.data

        if messages:
            latest_message = messages[0]
            response_content = latest_message.content[0].text.value
        else:
            response_content = "No response received."

        return Response({'response': response_content})

    except Exception as e:
        return Response({'error': str(e)}, status=500)
