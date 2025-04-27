import os
from groq import Groq
from flask import current_app

class Chatbot:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            current_app.logger.error("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model = "gemma-7b-it"  # Using Mixtral model which is available on Groq
        
    def generate_response(self, prompt, context=None):
        if not self.client:
            return "Chat functionality is currently unavailable. Please configure GROQ_API_KEY."
            
        try:
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": prompt})
            
            # Add plant expert context
            system_message = {
                "role": "system",
                "content": "You are a plant disease expert helping users identify and treat plant diseases. "
                          "Provide accurate, helpful advice about plant health, disease prevention, and treatment."
            }
            messages.insert(0, system_message)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            current_app.logger.error(f"Error generating chatbot response: {error_msg}")
            if "api_key" in error_msg.lower():
                return "Chat functionality is currently unavailable. Please check the API key configuration."
            return "I apologize, but I'm having trouble processing your request at the moment. Please try again later."

    def stream_response(self, prompt, context=None):
        if not self.client:
            yield "Chat functionality is currently unavailable. Please configure GROQ_API_KEY."
            return
            
        try:
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": prompt})
            
            # Add plant expert context
            system_message = {
                "role": "system",
                "content": "You are a plant disease expert helping users identify and treat plant diseases. "
                          "Provide accurate, helpful advice about plant health, disease prevention, and treatment."
            }
            messages.insert(0, system_message)
            
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            error_msg = str(e)
            current_app.logger.error(f"Error streaming chatbot response: {error_msg}")
            if "api_key" in error_msg.lower():
                yield "Chat functionality is currently unavailable. Please check the API key configuration."
            else:
                yield "I apologize, but I'm having trouble processing your request at the moment. Please try again later." 