import json
import os

import streamlit as st
from transformers import pipeline

from chatbot import Chatbot
from config import (
    MODEL_NAME,
    CHATS_DIR
)


# ============================================
# Page configuration
# ============================================

st.set_page_config(
    page_title="Qwen AI Chatbot",
    page_icon="🤖",
    layout="wide"
)


# ============================================
# Helper functions
# ============================================

def get_saved_chats():

    os.makedirs(CHATS_DIR, exist_ok=True)

    chat_files = [
        file
        for file in os.listdir(CHATS_DIR)
        if file.startswith("chat_")
        and file.endswith(".json")
    ]

    chat_ids = []

    for file in chat_files:

        try:

            chat_id = int(
                file.replace(
                    "chat_",
                    ""
                ).replace(
                    ".json",
                    ""
                )
            )

            chat_ids.append(chat_id)

        except ValueError:
            continue

    return sorted(chat_ids)


def get_next_chat_id():

    saved_chats = get_saved_chats()

    if not saved_chats:
        return 1

    return max(saved_chats) + 1


def get_chat_title(chat_id):

    chat_file = os.path.join(
        CHATS_DIR,
        f"chat_{chat_id}.json"
    )

    if not os.path.exists(chat_file):

        return f"Chat {chat_id}"

    try:

        with open(
            chat_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):

            return data.get(
                "title",
                f"Chat {chat_id}"
            )

    except (
        json.JSONDecodeError,
        OSError
    ):
        pass

    return f"Chat {chat_id}"


def delete_chat(chat_id):

    chat_file = os.path.join(
        CHATS_DIR,
        f"chat_{chat_id}.json"
    )

    if os.path.exists(chat_file):

        os.remove(chat_file)

        return True

    return False

def rename_chat(chat_id, new_title):

    chat_file = os.path.join(
        CHATS_DIR,
        f"chat_{chat_id}.json"
    )

    if not os.path.exists(chat_file):
        return False

    try:

        with open(
            chat_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):

            data["title"] = new_title

        else:

            data = {
                "title": new_title,
                "messages": data
            }

        with open(
            chat_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except (
        json.JSONDecodeError,
        OSError
    ):

        return False

# ============================================
# Load model ONLY ONCE
# ============================================

@st.cache_resource
def load_model():

    return pipeline(
        "text-generation",
        model=MODEL_NAME,
        clean_up_tokenization_spaces=False
    )


pipe = load_model()


# ============================================
# Session state
# ============================================

if "chat_id" not in st.session_state:

    saved_chats = get_saved_chats()

    if saved_chats:

        st.session_state.chat_id = saved_chats[-1]

    else:

        st.session_state.chat_id = 1


if "chatbot" not in st.session_state:

    st.session_state.chatbot = Chatbot(
        pipe=pipe,
        chat_id=st.session_state.chat_id
    )
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 100

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "top_p" not in st.session_state:
    st.session_state.top_p = 0.9    

# ============================================
# Sidebar
# ============================================

with st.sidebar:
    if not st.session_state.show_settings:
    
        st.title("💬 Conversations")
    
        # ----------------------------------------
        # New Chat
        # ----------------------------------------
    
        if st.button(
            "➕ New Chat",
            use_container_width=True
        ):
    
            new_id = get_next_chat_id()
    
            st.session_state.chat_id = new_id
    
            st.session_state.chatbot = Chatbot(
                pipe=pipe,
                chat_id=new_id
            )
    
            st.rerun()
    
        # ----------------------------------------
        # Clear current chat
        # ----------------------------------------
    
        if st.button(
            "🧹 Clear Current Chat",
            use_container_width=True
        ):
    
            st.session_state.chatbot.clear_memory()
    
            st.rerun()
    
        st.divider()
    
        # ----------------------------------------
        # Saved chats
        # ----------------------------------------
    
        saved_chats = get_saved_chats()
    
        if saved_chats:
    
            for chat_id in saved_chats:
    
                col1, col2,col3 = st.columns(
                    [4, 1,1]
                )
    
                with col1:
    
                    title = get_chat_title(
                        chat_id
                    )
    
                    if (
                        chat_id
                        == st.session_state.chat_id
                    ):
    
                        title += " ✓"
    
                    if st.button(
                        title,
                        key=f"open_{chat_id}",
                        use_container_width=True
                    ):
    
                        st.session_state.chat_id = chat_id
    
                        st.session_state.chatbot = Chatbot(
                            pipe=pipe,
                            chat_id=chat_id
                        )
    
                        st.rerun()
                with col2:
    
                    if st.button(
                        "✏️",
                        key=f"rename_{chat_id}"
                    ):
                
                        st.session_state.rename_chat_id = chat_id
                
                        st.rerun()        
                with col3:
    
                    if st.button(
                        "🗑️",
                        key=f"delete_{chat_id}"
                    ):
                
                        st.session_state.delete_chat_id = chat_id
                
                        st.rerun()  
        else:
        
                st.info(
                    "No saved conversations."
                )                 
        st.divider()
# ----------------------------------------
        # Setting button
# ----------------------------------------
        if st.button(
            "⚙️ Settings",
            use_container_width=True
        ):
            st.session_state.show_settings = True
            st.rerun()
# ----------------------------------------
        # export
# ----------------------------------------            
        st.divider()

        st.subheader("📦 Chat")

        export_data = json.dumps(
            {
                "title": st.session_state.chatbot.title,
                "messages": st.session_state.chatbot.messages
            },
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            "📥 Export Current Chat",
            data=export_data,
            file_name=f"chat_{st.session_state.chat_id}.json",
            mime="application/json",
            use_container_width=True
        )    
        uploaded_file = st.file_uploader(
            "📤 Import Chat",
            type=["json"],
            key="chat_import"
        )

        if uploaded_file is not None:

            import_key = (
                uploaded_file.name,
                uploaded_file.size
            )

            if (
                "last_imported_file" not in st.session_state
                or st.session_state.last_imported_file != import_key
            ):

                try:

                    imported_data = json.load(uploaded_file)

                    if not isinstance(imported_data, dict):

                        st.error(
                            "Invalid chat file format."
                        )

                    elif "messages" not in imported_data:

                        st.error(
                            "Chat file does not contain messages."
                        )

                    else:

                        imported_messages = imported_data["messages"]

                        if not isinstance(imported_messages, list):

                            st.error(
                                "Invalid messages format."
                            )

                        else:

                            new_id = get_next_chat_id()

                            chat_file = os.path.join(
                                CHATS_DIR,
                                f"chat_{new_id}.json"
                            )

                            imported_title = imported_data.get(
                                "title",
                                f"Chat {new_id}"
                            )

                            with open(
                                chat_file,
                                "w",
                                encoding="utf-8"
                            ) as file:

                                json.dump(
                                    {
                                        "title": imported_title,
                                        "messages": imported_messages
                                    },
                                    file,
                                    indent=4,
                                    ensure_ascii=False
                                )

                            st.session_state.last_imported_file = import_key

                            st.session_state.chat_id = new_id

                            st.session_state.chatbot = Chatbot(
                                pipe=pipe,
                                chat_id=new_id
                            )

                            st.success(
                                f"Chat imported as Chat {new_id}"
                            )

                            st.rerun()

                except (
                    json.JSONDecodeError,
                    UnicodeDecodeError
                ):

                    st.error(
                        "Invalid JSON file."
                    )
# ----------------------------------------
        # Setting
# ----------------------------------------    
    if st.session_state.show_settings:

        st.divider()

        st.title("⚙️ Settings")

        st.session_state.max_tokens = st.slider(
            "Max New Tokens",
            min_value=20,
            max_value=500,
            value=st.session_state.max_tokens,
            step=10
        )

        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.5,
            value=st.session_state.temperature,
            step=0.1
        )

        st.session_state.top_p = st.slider(
            "Top P",
            min_value=0.1,
            max_value=1.0,
            value=st.session_state.top_p,
            step=0.05
        )

        st.divider()

        if st.button(
            "⬅️ Back to Chats",
            use_container_width=True
        ):

            st.session_state.show_settings = False

            st.rerun()        

    if "rename_chat_id" in st.session_state:

        rename_id = st.session_state.rename_chat_id
    
        st.divider()
    
        st.subheader("✏️ Rename Chat")
    
        current_title = get_chat_title(rename_id)
    
        new_title = st.text_input(
            "Chat name",
            value=current_title,
            key="rename_input"
        )
    
        col1, col2 = st.columns(2)
    
        with col1:
    
            if st.button(
                "Save",
                use_container_width=True
            ):
    
                new_title = new_title.strip()
    
                if new_title:
    
                    rename_chat(
                        rename_id,
                        new_title
                    )
    
                    if rename_id == st.session_state.chat_id:
    
                        st.session_state.chatbot.title = new_title
    
                    del st.session_state.rename_chat_id
    
                    st.rerun()
    
        with col2:
    
            if st.button(
                "Cancel",
                use_container_width=True,
                key="cancel_rename"
):
                del st.session_state.rename_chat_id
    
                st.rerun()
    if "delete_chat_id" in st.session_state:

        delete_id = st.session_state.delete_chat_id
    
        st.divider()
    
        st.warning(
            f"Delete '{get_chat_title(delete_id)}'?"
        )
    
        st.write(
            "This action cannot be undone."
        )
    
        col1, col2 = st.columns(2)
    
        with col1:
    
            if st.button(
                "🗑️ Delete",
                use_container_width=True
            ):
    
                delete_chat(delete_id)
    
                del st.session_state.delete_chat_id
    
                remaining = get_saved_chats()
    
                if remaining:
    
                    if delete_id == st.session_state.chat_id:
    
                        new_current = remaining[-1]
    
                        st.session_state.chat_id = new_current
    
                        st.session_state.chatbot = Chatbot(
                            pipe=pipe,
                            chat_id=new_current
                        )
    
                else:
    
                    new_id = 1
    
                    st.session_state.chat_id = new_id
    
                    st.session_state.chatbot = Chatbot(
                        pipe=pipe,
                        chat_id=new_id
                    )
    
                st.rerun()
    
        with col2:
    
            if st.button(
                "Cancel",
                use_container_width=True,
                key="cancel_delete"
   ):
    
                del st.session_state.delete_chat_id
    
                st.rerun()
# ============================================
# Main UI
# ============================================

st.title("🤖 Qwen AI Chatbot")

st.caption(
    f"Current conversation: "
    f"Chat {st.session_state.chat_id}"
)


# ============================================
# Display messages
# ============================================

for message in st.session_state.chatbot.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================
# User input
# ============================================

user_input = st.chat_input(
    "Ask me anything..."
)


if user_input and user_input.strip():

    # User message
    with st.chat_message("user"):

        st.write(user_input)

    # AI response
    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                response = st.session_state.chatbot.generate_response(
                    user_input,
                    max_new_tokens=st.session_state.max_tokens,
                    temperature=st.session_state.temperature,
                    top_p=st.session_state.top_p
                )

                st.markdown(response)

            except Exception as e:

                st.error(
                    "Sorry, something went wrong while generating the response."
                )

                print(
                    f"Generation Error: {e}"
                )

    # Refresh UI
    st.rerun()