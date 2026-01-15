from dotenv import load_dotenv
import speech_recognition as sr
from langgraph.checkpoint.mongodb import MongoDBSaver
from graph.graph import create_chat_graph
import asyncio
from openai.helpers import LocalAudioPlayer
import os
from openai import OpenAI, AsyncOpenAI
from guardrails.hub import ToxicLanguage,GuardrailsPII
from guardrails import OnFailAction, Guard
load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="presidio")
openai = AsyncOpenAI()

MONGODB_URI = "mongodb://admin:admin@localhost:27017"
config = {"configurable": {"thread_id": "13"}}
 

async def speak(text: str):
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    guard = Guard().use_many(
        ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail=OnFailAction.EXCEPTION),
        GuardrailsPII(entities=["IP_ADDRESS","IN_AADHAAR"], on_fail="fix"))
    
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)
        
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 2

            while True:
                print("Say something!")
                audio = r.listen(source)

                print("Processing audio...")
                sst = r.recognize_google(audio)
                
                # Validate input with guardrail
                try:
                    guard.validate(sst)
                    print("You Said:", sst)
                
                # Process through the graph
                    for event in graph.stream({"messages": [{"role": "user", "content": sst}]}, config, stream_mode="values"):
                        if "messages" in event:
                            last_message = event["messages"][-1]
                            last_message.pretty_print()
                        
                        # Only speak if the message is from the assistant (not user)
                            if last_message.type == "ai" or getattr(last_message, 'role', None) == 'assistant':
                                temp = last_message.content
                                asyncio.run(speak(text=temp))
                except Exception as e:
                    print(f"Guardrail failed: {e}")
                    print("Skipping this input due to toxic content.")
                    continue  # Skip processing and continue to next input

                


if __name__ == "__main__":
    main()