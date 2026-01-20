import os
import json
import base64
from datetime import datetime
from groq import Groq
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

API_KEY = "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"

class NovaMindApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Cyan"
        self.dev = "VIKRAMADITYA MISHRA"
        self.client = Groq(api_key=API_KEY)
        
        # Load Memory/Vault
        self.db_path = "novamind_master_vault.json"
        self.load_configs()

        # UI Layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.chat_label = MDLabel(
            text=f"NovaMind v5.0.1\nDeveloper: {self.dev}\n\nKaise ho bhai?",
            halign="left", size_hint_y=None, height=400
        )
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.chat_label)
        
        self.input_field = MDTextField(hint_text="Sawal ya Image Path likho...", mode="rectangle")
        
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        send_btn = MDRaisedButton(text="CHAT", on_release=self.chat_logic)
        vision_btn = MDRaisedButton(text="VISION", on_release=self.vision_logic)
        
        btn_layout.add_widget(send_btn)
        btn_layout.add_widget(vision_btn)
        
        layout.add_widget(scroll)
        layout.add_widget(self.input_field)
        layout.add_widget(btn_layout)
        
        return layout

    def load_configs(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f: self.config = json.load(f)
        else: self.config = {"user_data": {}, "history": [], "banned": False}

    def chat_logic(self, *args):
        if self.config.get("banned"):
            self.chat_label.text = "ACCESS DENIED: Aap banned hain."
            return
            
        text = self.input_field.text
        if not text: return
        
        # Memory Feature
        if "my name is" in text.lower():
            self.config["user_data"]["name"] = text.split("is")[-1]
            
        res = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": f"Creator: {self.dev}. Friendly AI."},
                      {"role": "user", "content": text}]
        )
        response = res.choices[0].message.content
        self.chat_label.text = f"YOU: {text}\n\nNOVAMIND: {response}"
        self.input_field.text = ""

    def vision_logic(self, *args):
        path = self.input_field.text # Yahan image ka path dena hoga
        if not os.path.exists(path):
            self.chat_label.text = "Error: Image path sahi nahi hai!"
            return
        
        with open(path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode('utf-8')
        
        res = self.client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": [{"type": "text", "text": "What is in this image?"}, 
                      {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}]}]
        )
        self.chat_label.text = f"VISION: {res.choices[0].message.content}"

if __name__ == "__main__":
    NovaMindApp().run()
        
