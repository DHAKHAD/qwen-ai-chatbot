import json
import os

from transformers import pipeline, GenerationConfig

from config import (
    MODEL_NAME,
    MAX_NEW_TOKENS,
    MAX_HISTORY,
    DO_SAMPLE,
    CHATS_DIR,
    SYSTEM_PROMPT
)


class Chatbot:

    def __init__(self, pipe, chat_id=1):

        self.pipe = pipe
        self.chat_id = chat_id
    
        os.makedirs(CHATS_DIR, exist_ok=True)
    
        self.title = f"Chat {chat_id}"
    
        chat_file = self.get_chat_file()
    
        if os.path.exists(chat_file):
    
            self.messages = self.load_chat()
    
        else:
    
            self.messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]
    
            self.save_chat()
    # -----------------------------
    # Chat file
    # -----------------------------

    def get_chat_file(self):

        return os.path.join(
            CHATS_DIR,
            f"chat_{self.chat_id}.json"
        )

    # -----------------------------
    # Load chat
    # -----------------------------

    def load_chat(self):

        chat_file = self.get_chat_file()

        if os.path.exists(chat_file):

            try:

                with open(
                    chat_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                # New format
                if isinstance(data, dict):

                    self.title = data.get(
                        "title",
                        f"Chat {self.chat_id}"
                    )

                    messages = data.get(
                        "messages",
                        []
                    )

                    if messages:
                        return messages

                # Old format
                elif isinstance(data, list):

                    if data:
                        return data

            except (
                json.JSONDecodeError,
                OSError
            ):
                pass

        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    # -----------------------------
    # Save chat
    # -----------------------------

    def save_chat(self):

        chat_file = self.get_chat_file()

        with open(
            chat_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {
                    "title": self.title,
                    "messages": self.messages
                },
                file,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------
    # Clear chat
    # -----------------------------

    def clear_memory(self):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        self.title = f"Chat {self.chat_id}"

        self.save_chat()

    # -----------------------------
    # Generate response
    # -----------------------------

    def generate_response(
        self,
        user_input,
        max_new_tokens=100,
        temperature=0.7,
        top_p=0.9
        ):    
    
        self.messages.append({
            "role": "user",
            "content": user_input
        })
    
        user_messages = [
            message
            for message in self.messages
            if message["role"] == "user"
        ]
    
        if len(user_messages) == 1:
    
            self.title = user_input[:40]
    
            if len(user_input) > 40:
                self.title += "..."
    
        if len(self.messages) > MAX_HISTORY + 1:
    
            self.messages = (
                [self.messages[0]]
                + self.messages[-MAX_HISTORY:]
            )
    
        generation_config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True
        )
        
        result = self.pipe(
            self.messages,
            generation_config=generation_config
        )
    
        generated_messages = result[0]["generated_text"]
    
        assistant_response = generated_messages[-1]["content"]
    
        self.messages.append({
            "role": "assistant",
            "content": assistant_response
        })
    
        self.save_chat()
    
        return assistant_response