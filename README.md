# 🤖 Qwen AI Chatbot

A local conversational AI chatbot built with **Python, Streamlit, Hugging Face Transformers, PyTorch, and Qwen2.5-0.5B-Instruct**.

The application provides a ChatGPT-style conversational interface with persistent conversation history, multiple chats, chat management, configurable text-generation parameters, Markdown rendering, JSON-based storage, and error handling.

The project is designed to run locally and currently supports CPU-based inference.

---

# 📌 Project Overview

The goal of this project is to build a complete local AI chatbot application instead of simply calling a language model and printing its response.

The project combines:

- A web-based user interface
- A locally loaded Hugging Face language model
- Conversation memory
- Persistent JSON storage
- Multiple independent conversations
- Configurable generation parameters
- Chat management
- Error handling
- Streamlit session-state management

The application allows users to create and manage multiple conversations while maintaining their conversation history between application reruns.

---

# 🎯 Problem Statement

Traditional model experiments often involve running a Python script from the terminal and manually entering prompts.

This project improves that experience by providing a complete interactive application where users can:

- Ask questions through a web interface
- Maintain conversation context
- Create multiple conversations
- Save conversations automatically
- Rename conversations
- Delete conversations
- Clear conversation history
- Configure model generation behavior
- Import and export conversations

The project demonstrates how a pretrained language model can be integrated into a practical Python application.

---

# ✨ Key Features

## 1. Interactive Chat Interface 

The application provides a ChatGPT-style interface using Streamlit.

Users can enter prompts through:

```python
st.chat_input()
```

## 2. Qwen2.5 Language Model

The chatbot uses:

Qwen/Qwen2.5-0.5B-Instruct

The model is loaded using the Hugging Face Transformers pipeline:

pipeline(
    "text-generation",
    model=MODEL_NAME
)

The model is instruction-tuned and designed for conversational and instruction-following tasks.

🧠 How the Chatbot Works

The overall flow is:

User
  │
  ▼
Streamlit Chat Interface
  │
  ▼
app.py
  │
  ▼
Chatbot.generate_response()
  │
  ▼
Conversation History
  │
  ▼
Hugging Face Pipeline
  │
  ▼
Qwen2.5-0.5B-Instruct
  │
  ▼
Generated Response
  │
  ▼
Streamlit UI
  │
  ▼
JSON Chat Storage
🏗️ Application Architecture

The project is divided into three main responsibilities.

app.py

Responsible for the application interface and Streamlit logic.

It handles:

Page configuration
Sidebar
Chat selection
New chat
Clear chat
Rename chat
Delete chat
Settings
User input
Displaying messages
Error handling
Streamlit session state
chatbot.py

Responsible for chatbot logic.

It handles:

Loading conversations
Saving conversations
Maintaining message history
Clearing conversation memory
Generating AI responses
Updating conversation titles
Calling the Hugging Face model
config.py

Responsible for centralized configuration.

Typical configuration includes:

MODEL_NAME
MAX_NEW_TOKENS
MAX_HISTORY
DO_SAMPLE
CHATS_DIR
SYSTEM_PROMPT

Keeping configuration separate makes the project easier to maintain.

📁 Project Structure
huggingface_project/
│
├── app.py
├── chatbot.py
├── config.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── chats/
│   └── chat_*.json
│
└── venv/

venv/, __pycache__/, and chat JSON files should not be committed to GitHub.

🐍 Technologies Used
Python

Python is the primary programming language used for the project.

It is responsible for:

Application logic
File handling
JSON processing
Model interaction
Conversation management
Error handling
Streamlit

Streamlit is used to create the interactive web interface.

Important Streamlit components used include:

st.set_page_config()
st.sidebar
st.button()
st.expander()
st.slider()
st.chat_input()
st.chat_message()
st.session_state
st.cache_resource()
st.spinner()
st.error()
st.markdown()

Streamlit allows the Python application to be converted into an interactive browser-based application without requiring a separate frontend framework.

Hugging Face Transformers

The Transformers library provides access to pretrained transformer-based language models.

The project uses the text-generation pipeline:

pipeline(
    "text-generation",
    model=MODEL_NAME
)

This abstraction simplifies model loading and text generation.

Qwen2.5-0.5B-Instruct

## The project uses:

## 1 Qwen/Qwen2.5-0.5B-Instruct

The model generates responses based on the supplied conversation history and generation parameters.

Because this is a relatively small model, it can run locally without requiring a high-end GPU, although CPU inference can be slower.

## 2 PyTorch

PyTorch is used by the Transformers ecosystem as the underlying machine-learning framework for model inference.

The project currently runs on CPU when CUDA is unavailable.

## 3 CUDA availability was checked using:

torch.cuda.is_available()
JSON

JSON is used for persistent conversation storage.

Each conversation is stored as a JSON file.

Example:

{
    "title": "Python Question",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": "What is Python?"
        },
        {
            "role": "assistant",
            "content": "Python is a programming language..."
        }
    ]
}
💾 Conversation Persistence

The application stores conversations inside the:

chats/

directory.

Each conversation uses a separate JSON file:

chat_1.json
chat_2.json
chat_3.json

This allows conversations to remain available after Streamlit reruns or application restarts.

🧠 Conversation Memory

The chatbot maintains a list called:

self.messages

Messages follow a role-based structure:

system
user
assistant
user
assistant
...

For example:

[
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    },
    {
        "role": "user",
        "content": "What is Python?"
    },
    {
        "role": "assistant",
        "content": "Python is a programming language..."
    }
]

The conversation history is passed to the model during generation.

This allows the chatbot to maintain context across multiple messages.

📝 System Prompt

The chatbot uses a system prompt to define the behavior of the AI assistant.

The system prompt provides instructions such as:

Answer questions clearly
Avoid inventing facts
Use conversation history when relevant
Explain technical topics simply
Provide examples when useful
Format technical responses using Markdown
Use code blocks for programming code
Ask for clarification when necessary

This demonstrates how system-level instructions can influence model behavior.

🎛️ Generation Settings

The application provides configurable model-generation parameters.

Max New Tokens

Controls the maximum number of new tokens generated by the model.

Example:

max_new_tokens=200

Higher values allow longer responses but may increase generation time.

Temperature

Temperature controls randomness during generation.

General behavior:

Lower temperature
        ↓
More predictable / deterministic responses


Higher temperature
        ↓
More varied / creative responses

The application allows users to adjust temperature through the Streamlit settings interface.

Top P

Top P controls nucleus sampling.

Instead of considering every possible token, the model samples from a group of tokens whose cumulative probability reaches the selected threshold.

Example:

top_p=0.9
Do Sample

The project uses sampling during generation:

do_sample=True

This allows parameters such as temperature and top-p to influence generation.

⚙️ Settings Interface

The application provides a settings panel containing:

Max New Tokens
Temperature
Top P

These values are stored in Streamlit session state:

st.session_state

The selected values are then passed to:

generate_response()
💬 Chat Management

The application supports multiple conversations.

New Chat

Creates a new chat ID and initializes a new chatbot instance.

Example:

Chat 1
Chat 2
Chat 3
Clear Current Chat

Clears the current conversation while preserving the chat itself.

The system message is restored after clearing.

Rename Chat

Users can rename conversations.

For example:

Chat 4

can become:

Python Learning

The title is stored inside the corresponding JSON file.

Delete Chat

Users can delete a saved conversation.

A confirmation step is provided before deletion.

Load Conversation

Previously saved conversations can be selected from the sidebar and loaded into the current session.

📥 Import and 📤 Export

The application supports conversation persistence through JSON files.

Exported conversations can be saved and transferred as JSON.

The stored information includes:

Chat title
System message
User messages
Assistant messages

This makes the conversation data portable.

🛡️ Error Handling

The chatbot uses exception handling around model generation.

Example:

try:


    response = chatbot.generate_response(...)


except Exception as e:


    st.error(
        "Sorry, something went wrong while generating the response."
    )


    print(
        f"Generation Error: {e}"
    )

This prevents unexpected model-generation errors from crashing the entire application interface.

The user receives a friendly message while the technical error is printed in the terminal for debugging.

🔄 Streamlit Session State

Streamlit reruns the Python script when users interact with widgets.

To preserve important application state, the project uses:

st.session_state

Important state values include:

chat_id
chatbot
show_settings
max_tokens
temperature
top_p
rename_chat_id
delete_chat_id

This allows the application to maintain the current conversation and user settings across Streamlit reruns.

⚡ Model Loading Optimization

The model is loaded using:

@st.cache_resource
def load_model():


    return pipeline(
        "text-generation",
        model=MODEL_NAME
    )

st.cache_resource allows the loaded model resource to be reused across Streamlit reruns instead of unnecessarily loading the model repeatedly.

This is particularly important because loading a language model can be expensive in terms of memory and startup time.

🧹 Git and Security

The project uses .gitignore to prevent unnecessary or private files from being committed.

Examples include:

__pycache__/
venv/
.my-env/
.env
chats/*.json

Chat JSON files are excluded because they may contain personal conversation data.

Virtual environments are also excluded because dependencies can be recreated using:

pip install -r requirements.txt
⚙️ Installation
1. Clone the repository
git clone <YOUR_REPOSITORY_URL>
2. Navigate to the project
cd huggingface_project
3. Create a virtual environment

Windows:

python -m venv venv
4. Activate the environment

Windows PowerShell:

venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

Streamlit will provide a local URL in the terminal.

Open that URL in your browser to access the chatbot.