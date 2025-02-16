# Dynamic RolePlaying Society Demo

## Overview
This project is a dynamic Streamlit application demonstrating a RolePlaying Society session using the CAMEL framework. In this demo, two AI agents collaborate to develop a comprehensive marketing strategy for an innovative eco-friendly startup. The conversation rounds are powered by **GPT‑4O mini** for dynamic dialogue, and the final output is polished using the **AIML DeepSeek R1** model for summarization.

## Features
- **Dynamic Configuration:**  
  Users can input their own task prompt and role names to configure the session, making the application fully customizable.
  
- **Multi-Round Conversation:**  
  The app conducts several conversation rounds between:
  - **AI User:** An enthusiastic eco-entrepreneur.
  - **AI Assistant:** A seasoned marketing strategist.
  
- **Final Summarization:**  
  After the conversation rounds, the final output is processed by an AIML DeepSeek R1 model to extract and summarize key points.

- **API Key Integration:**  
  The app requires two API keys:
  - **OpenAI API Key:** Powers the GPT‑4o mini models for the conversation rounds.
  - **AIML API Key:** Used by the AIML DeepSeek R1 model for final summarization.

- **User-Friendly Interface:**  
  Built with Streamlit, the application features a sidebar for API key inputs, a dynamic configuration section for the roleplaying session, and detailed displays of each conversation round and the final summarized output.

## Requirements
- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [camel-ai](https://github.com/angelabauer/CAMEL-UI) (version 0.2.16 or compatible)

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
 ```
2. Create and Activate a Virtual Environment:

 ```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install Dependencies:

```bash
pip install streamlit
pip install camel-ai[all]==0.2.20
```
# File Structure

- **`app.py`**:  
  Main Streamlit application that handles the UI, dynamic configuration, conversation rounds, and final summarization.

- **`society_helpers.py`**:  
  Helper functions to initialize the GPT‑4O mini model and dynamically configure the RolePlaying Society session.

---

# Usage

## API Key Setup:
1. Open the app and enter your **AIML API Key** (for final summarization) and **OpenAI API Key** (for running GPT‑4O mini) in the sidebar.

## Configure the Session:
1. Enter a **custom task prompt** (e.g.,  
   *""Develop a comprehensive marketing strategy for an innovative startup launching a AI Agent Startup"*).
2. Set **custom role names** for:  
   - **AI User** (e.g., *"an enthusiastic AI-Engineer"*)  
   - **AI Assistant** (e.g., *"a seasoned marketing strategist"*)
3. Choose the **number of conversation rounds**.

## Run the Session:
1. Click the **"Run RolePlaying Session"** button to start the conversation.
2. Each conversation round’s output is displayed with detailed **intermediate messages**.

## Final Summarization:
- After the conversation rounds, the final message is processed by the **AIML DeepSeek R1** model.
- A **polished summary** is displayed.

---

# Acknowledgements

- **Built using** the **CAMEL framework**  
- **Conversation powered by** **GPT‑4o mini** (*OpenAI API*)  
- **Final summarization using** **AIML -> DeepSeek R1**  
- **Developed UI with** **Streamlit**
