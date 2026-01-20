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
        self.db_path = "novamind_master_vault.json"
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.chat_label = MDLabel(text=f"NovaMind v5.0.1\nDev: {self.dev}\n\nKaise ho bhai?", halign="left", size_hint_y=None, height=400)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.chat_label)
        self.input_field = MDTextField(hint_text="Sawal likho...", mode="rectangle")
        send_btn = MDRaisedButton(text="CHAT", on_release=self.chat_logic, pos_hint={"center_x": 0.5})
        layout.add_widget(scroll); layout.add_widget(self.input_field); layout.add_widget(send_btn)
        return layout

    def chat_logic(self, *args):
        text = self.input_field.text
        if not text: return
        try:
            res = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Friendly AI assistant."}, {"role": "user", "content": text}]
            )
            self.chat_label.text = f"YOU: {text}\n\nNOVAMIND: {res.choices[0].message.content}"
            self.input_field.text = ""
        except: self.chat_label.text = "Connection Error!"

if __name__ == "__main__":
    NovaMindApp().run()
    
