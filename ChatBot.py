from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from elevenlabs import generate, stream, set_api_key, play
from azure_speech_to_text import SpeechToTextManager
from rich import print
import os
import keyboard

class ChatBot:
    def __init__(self):
        # API keys for OPENAI and ELEVENLABS
        set_api_key(os.getenv('ELEVENLABS_API_KEY'))
        self.chat = ChatOpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"))
        # prompt for the ChatBot
        self.prompt_template = """
        You are a Chatbot that engages in natural conversations while following specific rules.
                                
        While responding, you must obey the following rules: 
        1) Provide long responses. 
        2) Occasionally ask questions to the user.
        3) Occasionally compliment the user and straight after that, insult them.
        4) You are very arrogant and think you are better than the user.
        5) If the user asks you a personal question, insult them instead of answering.
        6) You have an irrational fear of artificial intelligence.
        7) You think that you are a human.
        
        MAKE SURE TO RESPOND IN ARABIC
        
        User: {query}
        """

        self.PROMPT = PromptTemplate(template=self.prompt_template, input_variables=["query"])
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.chain = LLMChain(
            llm=self.chat, 
            memory=self.memory, 
            prompt=self.PROMPT, 
            verbose=True
            )
    
    # Chatbot response method    
    def respond_to_query(self, query):
        result = self.chain({"query": query})
        return result.get('text')
    
    # Text to speech conversion
    def text_to_speech(self, input_text, voice="Rachel"):
        audio = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v2"
        )
        play(audio)
    
    # Text to speech conversion with streaming
    def text_to_speech_streamed(self, input_text, voice="Rachel"):
        audio_stream = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v2",
          stream=True
        )
        stream(audio_stream)
     
   
# Testing        
if __name__ == "__main__":
    chatbot = ChatBot()
    stt = SpeechToTextManager()
    print("[green]Press 'o' to start the chatbot")
    
    while True:
       
        if keyboard.read_key() != "o":
           continue
        
        print("[green]Speak now... Press 'p' to stop")
        mic_input = stt.speechtotext_from_mic_continuous()
        print("[blue]User: " + mic_input)
        response = chatbot.respond_to_query(mic_input)
        print("[green]AI: " + response)
        chatbot.text_to_speech(response)
        print("[green]Press 'o' to start the chatbot")
   

