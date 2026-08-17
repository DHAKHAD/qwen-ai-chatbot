import os

from chatbot import Chatbot
from config import CHATS_DIR


def get_next_chat_id():

    os.makedirs(CHATS_DIR, exist_ok=True)

    chat_files = [
        file
        for file in os.listdir(CHATS_DIR)
        if file.startswith("chat_") and file.endswith(".json")
    ]

    if not chat_files:
        return 1

    chat_ids = []

    for file in chat_files:

        try:

            chat_id = int(
                file.replace("chat_", "").replace(".json", "")
            )

            chat_ids.append(chat_id)

        except ValueError:
            continue

    return max(chat_ids) + 1
def get_saved_chats():

    os.makedirs(CHATS_DIR, exist_ok=True)

    chat_files = [
        file
        for file in os.listdir(CHATS_DIR)
        if file.startswith("chat_") and file.endswith(".json")
    ]

    chat_ids = []

    for file in chat_files:

        try:

            chat_id = int(
                file.replace("chat_", "").replace(".json", "")
            )

            chat_ids.append(chat_id)

        except ValueError:
            continue

    return sorted(chat_ids)

def main():

    chat_id = get_next_chat_id()

    chatbot = Chatbot(chat_id)

    print("================================")
    print("        Qwen AI Chatbot")
    print("================================")

    print(f"\nCurrent conversation: Chat {chat_id}")

    print("\nCommands:")
    print("/new       - Start new conversation")
    print("/chats     - Show saved conversations")
    print("/load <id> - Load a conversation")
    print("/clear     - Clear current conversation")
    print("/exit      - Exit chatbot")

    while True:

        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "/exit":

            print("AI: Goodbye!")
            break

        if user_input.lower() == "/new":

            chat_id = get_next_chat_id()

            chatbot = Chatbot(chat_id)

            print(f"AI: New conversation started — Chat {chat_id}.")
            continue
        if user_input.lower().startswith("/load"):

            parts = user_input.split()
        
            if len(parts) != 2:
        
                print("AI: Usage: /load <chat_id>")
                continue
        
            try:
        
                load_id = int(parts[1])
        
            except ValueError:
        
                print("AI: Chat ID must be a number.")
                continue
        
            saved_chats = get_saved_chats()
        
            if load_id not in saved_chats:
        
                print(f"AI: Chat {load_id} does not exist.")
                continue
        
            chatbot = Chatbot(load_id)
        
            chat_id = load_id
        
            print(f"AI: Chat {chat_id} loaded.")
        
            continue
        if user_input.lower() == "/chats":

            saved_chats = get_saved_chats()
        
            if not saved_chats:
                print("AI: No saved conversations.")
            else:
                print("\nSaved Conversations:")
        
                for chat in saved_chats:
                    print(f"Chat {chat}")
        
                print()
        
            continue
        if user_input.lower() == "/clear":

            chatbot.clear_memory()

            print(f"AI: Chat {chat_id} cleared.")
            continue

        try:

            response = chatbot.generate_response(user_input)

            print("AI:", response)

        except Exception as e:

            print("Error:", e)


if __name__ == "__main__":
    main()