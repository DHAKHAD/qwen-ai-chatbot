# 🤖 Qwen AI Chatbot

A local conversational AI chatbot built with **Python, Streamlit, Hugging Face Transformers, PyTorch, and Qwen2.5-0.5B-Instruct**.

The application provides a ChatGPT-style conversational interface with **persistent conversation history, multiple conversations, chat management, configurable text-generation parameters, Markdown response rendering, JSON-based storage, and error handling**.

The project is designed to run locally and currently supports **CPU-based inference**.

---

## 📌 Project Overview

The goal of this project is to build a complete local AI chatbot application rather than simply loading a language model and printing its response in the terminal.

The project combines:

* Interactive web-based chat interface
* Local Hugging Face language model inference
* Conversation memory
* Persistent JSON-based chat storage
* Multiple independent conversations
* Configurable text-generation parameters
* Chat creation and management
* Streamlit session-state management
* Error handling
* Markdown response rendering

The application allows users to create, manage, and continue multiple conversations while preserving their chat history across Streamlit reruns and application restarts.

---

## 🎯 Problem Statement

Traditional language-model experiments often require users to run a Python script from the terminal and manually enter prompts.

This project improves that workflow by providing a complete interactive application where users can:

* Ask questions through a web interface
* Maintain conversation context
* Create multiple conversations
* Save conversations automatically
* Load previous conversations
* Rename conversations
* Delete conversations
* Clear conversation history
* Configure model-generation behavior
* Import and export conversations
* Receive formatted Markdown responses

The project demonstrates how a pretrained language model can be integrated into a practical Python application with a persistent user interface and conversation-management system.

---

# ✨ Key Features

## 1. 💬 Interactive Chat Interface

The application provides a ChatGPT-style conversational interface using **Streamlit**.

Users can enter prompts using:

```python
st.chat_input("Ask me anything...")
```

Messages are displayed using:

```python
st.chat_message()
```

The interface also provides a sidebar for chat management and model settings.

---

## 2. 🤖 Qwen2.5 Language Model

The chatbot uses:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

The model is loaded using the Hugging Face Transformers pipeline:

```python
pipeline(
    "text-generation",
    model=MODEL_NAME
)
```

Qwen2.5-0.5B-Instruct is an instruction-tuned language model designed for conversational and instruction-following tasks.

Because it is a relatively small model, it is suitable for local experimentation and CPU-based inference, although CPU inference can be slower than GPU inference.

---

## 3. 🧠 Conversation Memory

The chatbot maintains conversation history using:

```python
self.messages
```

Messages follow a role-based structure:

```text
system
user
assistant
user
assistant
...
```

Example:

```python
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
```

The conversation history is passed to the model during response generation, allowing the chatbot to maintain context across multiple messages.

---

## 4. 💾 Persistent Chat Storage

Conversations are stored as JSON files inside:

```text
chats/
```

Example:

```text
chats/
├── chat_1.json
├── chat_2.json
└── chat_3.json
```

Each conversation stores:

* Chat title
* System message
* User messages
* Assistant messages

Example JSON structure:

```json
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
```

This allows conversations to remain available after Streamlit reruns and application restarts.

---

## 5. 🆕 Multiple Conversations

The application supports multiple independent conversations.

Example:

```text
Chat 1
Chat 2
Chat 3
Chat 4
```

Each conversation receives its own chat ID and JSON storage file.

Users can switch between previously saved conversations through the application interface.

---

## 6. 📝 Automatic Chat Titles

When a new conversation starts, the application can generate a title based on the first user message.

For example:

```text
User:
Explain Python decorators
```

The conversation can automatically receive a title such as:

```text
Explain Python decorators
```

The title is stored together with the conversation data.

---

## 7. ✏️ Rename Chat

Users can rename existing conversations.

For example:

```text
Chat 4
```

can be renamed to:

```text
Python Learning
```

The updated title is saved in the corresponding JSON file.

---

## 8. 🗑️ Delete Chat

Users can delete saved conversations through the chat-management interface.

A confirmation step is used before deletion to reduce accidental removal of conversations.

---

## 9. 🧹 Clear Conversation

Users can clear the current conversation while keeping the chat itself.

When a conversation is cleared, the system message is restored:

```python
{
    "role": "system",
    "content": SYSTEM_PROMPT
}
```

The chat title is also reset.

---

## 10. 📥 Import and 📤 Export

The application supports conversation portability through JSON files.

Conversation data can include:

* Chat title
* System message
* User messages
* Assistant messages

JSON-based storage makes conversation data easy to inspect, back up, and transfer.

---
## 📸 Screenshots

### Chat Interface

![Chat Interface](https://github.com/DHAKHAD/qwen-ai-chatbot/blob/main/screenshots/Screenshot%202026-1%20ai.png)

### Chat Management

![Chat Management](https://github.com/DHAKHAD/qwen-ai-chatbot/blob/main/screenshots/Screenshot%202026-22-ai.png)
### chat settings

![chat Settings](https://github.com/DHAKHAD/qwen-ai-chatbot/blob/main/screenshots/Screenshot%202026-setting.png)

---
# 🧠 How the Chatbot Works

The overall application flow is:

```text
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
```

### Response Generation Flow

1. User enters a prompt.
2. Streamlit receives the input.
3. The user message is added to conversation history.
4. The chatbot checks and manages conversation history.
5. Generation parameters are created.
6. The conversation is passed to the Hugging Face pipeline.
7. Qwen generates the response.
8. The assistant response is added to conversation history.
9. The conversation is saved as JSON.
10. Streamlit refreshes the interface and displays the response.

---

# 🏗️ Application Architecture

The project separates responsibilities across different Python modules.

## `app.py`

Responsible for the **Streamlit application interface**.

It handles:

* Page configuration
* Sidebar
* Chat selection
* New chat
* Clear chat
* Rename chat
* Delete chat
* Import/export interface
* Settings interface
* User input
* Message rendering
* Error handling
* Streamlit session state

---

## `chatbot.py`

Responsible for the **core chatbot logic**.

It handles:

* Loading conversations
* Saving conversations
* Maintaining message history
* Clearing conversation memory
* Generating AI responses
* Updating conversation titles
* Calling the Hugging Face model
* Managing chat JSON files

---

## `config.py`

Responsible for **centralized application configuration**.

Typical configuration values include:

```python
MODEL_NAME
MAX_NEW_TOKENS
MAX_HISTORY
DO_SAMPLE
CHATS_DIR
SYSTEM_PROMPT
```

Keeping configuration separate makes the application easier to maintain and modify.

---

## `main.py`

Provides a **terminal-based chatbot entry point**.

It contains functionality for:

* Starting a new conversation
* Loading saved conversations
* Listing saved chats
* Clearing conversations
* Exiting the chatbot

The primary user interface of the project is the Streamlit application in `app.py`.

---

# 📁 Project Structure

```text
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
```

### Important

The following directories/files should **not** be committed to GitHub:

```text
venv/
.my-env/
__pycache__/
.streamlit/
chats/*.json
.env
```

Virtual environments and generated chat files can be recreated or generated locally.

---

# 🐍 Technologies Used

## Python

Python is the primary programming language used throughout the project.

It is responsible for:

* Application logic
* File handling
* JSON processing
* Model interaction
* Conversation management
* Error handling
* Configuration management

---

## Streamlit

Streamlit is used to build the interactive web application.

Important Streamlit components used include:

```python
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
```

Streamlit allows the Python application to be converted into an interactive browser-based application without requiring a separate frontend framework.

---

## Hugging Face Transformers

The Transformers library provides access to pretrained transformer-based language models.

The project uses the text-generation pipeline:

```python
pipeline(
    "text-generation",
    model=MODEL_NAME
)
```

The pipeline abstraction simplifies model loading and text generation.

---

## Qwen2.5-0.5B-Instruct

The project uses:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

The model generates responses based on:

* System instructions
* Conversation history
* User prompts
* Generation parameters

The relatively small model size makes it suitable for local experimentation.

---

## PyTorch

PyTorch is used by the Transformers ecosystem as the underlying machine-learning framework for model inference.

The project checks CUDA availability using:

```python
torch.cuda.is_available()
```

When CUDA is unavailable, the application can run using CPU inference.

---

## JSON

JSON is used for persistent conversation storage.

Each conversation is stored as an individual JSON file.

This provides a simple and human-readable persistence mechanism without requiring a database.

---

# 📝 System Prompt

The chatbot uses a system prompt to define the behavior of the AI assistant.

The system prompt can provide instructions such as:

* Answer questions clearly
* Avoid inventing facts
* Use conversation history when relevant
* Explain technical topics simply
* Provide examples when useful
* Format technical responses using Markdown
* Use code blocks for programming code
* Ask for clarification when necessary

This demonstrates how system-level instructions can influence model behavior.

---

# 🎛️ Generation Settings

The application provides configurable model-generation parameters.

## Max New Tokens

Controls the maximum number of new tokens generated by the model.

Example:

```python
max_new_tokens=200
```

Higher values allow longer responses but can increase generation time and memory usage.

---

## Temperature

Temperature controls the randomness of generated responses.

General behavior:

```text
Lower temperature
        ↓
More predictable responses


Higher temperature
        ↓
More varied responses
```

The application allows users to adjust the temperature through the settings interface.

---

## Top P

Top P controls **nucleus sampling**.

Instead of considering every possible token, the model samples from a group of tokens whose cumulative probability reaches the selected threshold.

Example:

```python
top_p=0.9
```

A lower value generally restricts the sampling pool, while a higher value allows more possible tokens to be considered.

---

## Do Sample

The project uses sampling during generation:

```python
do_sample=True
```

This allows parameters such as `temperature` and `top_p` to influence the generated response.

---

# ⚙️ Settings Interface

The application provides configurable settings including:

* Max New Tokens
* Temperature
* Top P

These values are maintained using Streamlit session state:

```python
st.session_state
```

The selected values are passed to:

```python
generate_response()
```

This allows users to modify model behavior without changing the source code.

---

# 🔄 Streamlit Session State

Streamlit reruns the Python script when users interact with widgets.

To preserve important application state, the project uses:

```python
st.session_state
```

Important state values include:

```text
chat_id
chatbot
show_settings
max_tokens
temperature
top_p
rename_chat_id
delete_chat_id
```

This allows the application to maintain the current conversation and user settings across Streamlit reruns.

---

# ⚡ Model Loading Optimization

The model is loaded using Streamlit's resource caching mechanism:

```python
@st.cache_resource
def load_model():

    return pipeline(
        "text-generation",
        model=MODEL_NAME
    )
```

`st.cache_resource` allows the loaded model resource to be reused across Streamlit reruns instead of unnecessarily loading the model repeatedly.

This is important because loading a language model can require significant memory and startup time.

---

# 🛡️ Error Handling

The chatbot uses exception handling around model generation.

Example:

```python
try:

    response = chatbot.generate_response(
        user_input,
        max_new_tokens=st.session_state.max_tokens,
        temperature=st.session_state.temperature,
        top_p=st.session_state.top_p
    )

except Exception as e:

    st.error(
        "Sorry, something went wrong while generating the response."
    )

    print(
        f"Generation Error: {e}"
    )
```

This prevents unexpected model-generation errors from crashing the entire application interface.

The user receives a friendly error message while the technical error is printed in the terminal for debugging.

---

# 🧹 Git and Security

The project uses `.gitignore` to prevent unnecessary or private files from being committed.

Important ignored files include:

```text
__pycache__/
*.py[cod]

.my-env/
venv/
env/

.streamlit/

chats/*.json

.cache/
huggingface_cache/

.env

.vscode/
.idea/
```

### Why are chat files ignored?

Conversation JSON files may contain private or personal conversation data, so they should not be uploaded to a public repository.

### Why are virtual environments ignored?

Virtual environments contain installed packages that can be recreated using:

```bash
pip install -r requirements.txt
```

Therefore, the environment itself does not need to be committed to GitHub.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/DHAKHAD/qwen-ai-chatbot.git
```

---

## 2. Navigate to the Project

```bash
cd qwen-ai-chatbot
```

---

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

---

## 4. Activate the Virtual Environment

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal.

Open that URL in your browser to access the chatbot.

---

# 💻 Example Usage

After starting the application, users can enter prompts such as:

```text
Explain Python decorators with an example.
```

```text
What is the difference between a list and a tuple in Python?
```

```text
Write a Python function to find the largest number in a list.
```

The chatbot processes the prompt using the Qwen2.5 model and returns the generated response.

---

# 📊 Project Highlights

This project demonstrates practical experience with:

* Python application development
* Streamlit application development
* Large Language Model integration
* Hugging Face Transformers
* Qwen instruction-tuned models
* Prompt and system-message handling
* Conversation memory
* JSON persistence
* Session-state management
* Model-generation parameters
* Error handling
* Git and GitHub
* Local AI inference
* Modular Python architecture

---

# 🚀 Future Improvements

Potential future improvements include:

* GPU acceleration
* Streaming token-by-token responses
* User authentication
* Database-based chat storage
* SQLite/PostgreSQL integration
* Retrieval-Augmented Generation (RAG)
* Document upload and question answering
* Vector database integration
* Multiple model selection
* Voice input
* Text-to-speech responses
* Improved conversation search
* Docker deployment
* Cloud deployment

---

# 👨‍💻 Author

**Sunil Nagar**

Computer Science Engineer | Python | Data Science | Machine Learning | AI

---

# 📄 License

This project is intended for educational and portfolio purposes.

The Qwen2.5-0.5B-Instruct model and Hugging Face Transformers library are subject to their respective licenses and usage terms.
