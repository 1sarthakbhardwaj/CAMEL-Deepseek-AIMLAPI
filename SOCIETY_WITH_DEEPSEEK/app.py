import os
import streamlit as st
import nest_asyncio
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType
from camel.models import ModelFactory
from society_helpers import create_gpt4o_model, create_society

# Enable nested asyncio loops
nest_asyncio.apply()

# Set page configuration
st.set_page_config(page_title="Role-Playing AI Society", layout="wide")
st.title("CAMEL-AI RolePlaying Society Session with DeepSeek & AIML API")
st.markdown("""
This interactive AI demo simulates a **role-playing conversation** between two AI agents. 

**How it works:**
1. Configure the session by providing roles and a task.
2. Run multiple rounds of conversation between the AI agents.
3. Get a final consolidated strategy using **DeepSeek using AIML API** .
""")

# Sidebar: API Key Setup
st.sidebar.header("🔑 API Key Setup")
st.sidebar.markdown("Provide the necessary API keys:")

aiml_api_key = st.sidebar.text_input("AIML API Key (for using DeepSeek-R1)", type="password")
openai_api_key = st.sidebar.text_input("OpenAI API Key (for GPT‑4O Mini)", type="password")

if aiml_api_key:
    os.environ["AIML_API_KEY"] = aiml_api_key
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

if not aiml_api_key or not openai_api_key:
    st.sidebar.error("⚠️ Both API keys are required to proceed.")
    st.stop()
st.sidebar.success("✅ API keys set successfully!")

# Session Configuration
st.header("🎭 Configure Your AI Role-Playing Session")

st.markdown("**Define the conversation details:**")

task_prompt = st.text_area(
    "Task Prompt",
    value="Develop a comprehensive marketing strategy for an AI startup launching a new AI Tool SmartAssist, focusing on demographics, psychographics, and specific needs of remote teams.",
    height=100
)
user_role_name = st.text_input("🧑‍💻 AI User Role", value="AI Enginner and Founder")
assistant_role_name = st.text_input("🧠 AI Assistant Role", value="Marketing Strategist")
round_limit = st.slider("🔄 Number of Conversation Rounds", min_value=1, max_value=10, value=5)

st.markdown("---")

# Step 1: Initialize Model
st.subheader("🚀 Step 1: Initialize AI Model")
st.markdown("Setting up **GPT‑4O Mini** for the conversation...")
gpt4o_model = create_gpt4o_model()
st.success("GPT‑4O Mini is ready!")

# Step 2: Configure Society Session
st.subheader("⚙️ Step 2: Set Up Role-Playing Session")
society = create_society(task_prompt, user_role_name, assistant_role_name, gpt4o_model)
st.success("AI society session configured successfully!")

# Step 3: Run the Society Session
st.subheader("💬 Step 3: Start the AI Conversation")
st.markdown("Click the button to initiate the role-playing session. CAMEL agents will interact based on your setup.")

def is_terminated(response):
    if response.terminated:
        role = response.msg.role_type.name
        reason = response.info.get('termination_reasons', 'Unknown reason')
        st.warning(f"**Session terminated early: {role} ended due to {reason}.**")
    return response.terminated

if st.button("▶️ Start AI Conversation"):
    conversation_output = []
    input_msg = society.init_chat()
    final_message = None

    for i in range(round_limit):
        st.markdown(f"### 🔄 Round {i+1}")
        assistant_response, user_response = society.step(input_msg)
        
        if assistant_response.terminated or user_response.terminated:
            st.warning("⚠️ The session ended earlier than expected.")
            break
        
        conversation_output.append((f"Round {i+1} - AI User", user_response.msg.content))
        conversation_output.append((f"Round {i+1} - AI Assistant", assistant_response.msg.content))
        
        st.markdown(f"**🧑‍💻 AI User:** {user_response.msg.content}")
        st.markdown(f"**🤖 AI Assistant:** {assistant_response.msg.content}")
        st.markdown("---")
        
        input_msg = assistant_response.msg
        final_message = assistant_response.msg

    st.subheader("📌 Final AI-Generated Response")
    if final_message:
        st.markdown(final_message.content)
    else:
        st.warning("No final output was generated.")

    # Step 4: Final Summarization and Strategy Generation
    st.subheader("🐋 Step 4: Summarizing & Generating Final Strategy with DeepSeek-R1")
    st.markdown("Generating a summary and final strategy with **DeepSeek using AI/ML API**...")
    
    aiml_model = ModelFactory.create(
        model_platform=ModelPlatformType.AIML,
        model_type='deepseek/deepseek-r1',
        model_config_dict={"max_tokens": 2000}
    )
    
    summarizer_agent = ChatAgent(
        system_message=BaseMessage.make_assistant_message(
            role_name="Summarizer",
            content="Summarize the conversation and derive a consolidated marketing strategy."
        ),
        model=aiml_model,
    )
    
    summarization_response = summarizer_agent.step(final_message.content)
    st.success("✅ Final Strategy Generated!")
    st.markdown("### 📝 Consolidated Strategy")
    st.write(summarization_response.msgs[0].content)
