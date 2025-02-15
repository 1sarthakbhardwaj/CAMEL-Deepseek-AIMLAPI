import os
import streamlit as st
import nest_asyncio
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType
from camel.models import ModelFactory

# Import helper functions from our helper file
from society_helpers import create_gpt4o_model, create_society

# Allow nested asyncio loops (required in Streamlit)
nest_asyncio.apply()

# Set page configuration and style
st.set_page_config(page_title="Dynamic RolePlaying Society Demo", layout="wide")
st.title("Dynamic RolePlaying Society Demo")
st.markdown("""
This application demonstrates a dynamic RolePlaying Society session.  
Configure the session details below and run a conversation between two agents.  
The session uses **GPT‑4O mini** for the conversation rounds, and the final output is summarized using **AIML DeepSeek**.
""")

# --------------------------------------------------
# Sidebar: API Key Setup
# --------------------------------------------------
st.sidebar.header("API Key Setup")
st.sidebar.markdown("""
Provide the following API keys:
- **AIML API Key:** Used for the final output summarization using DEEPSEEK-R1.
- **OpenAI API Key:** Required for running GPT‑4O mini.
""")
aiml_api_key = st.sidebar.text_input("Enter your AIML API Key", type="password")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if aiml_api_key:
    os.environ["AIML_API_KEY"] = aiml_api_key
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

if not (aiml_api_key and openai_api_key):
    st.sidebar.warning("Please enter both API keys to proceed.")
    st.stop()
st.sidebar.success("API Keys are set.")

# --------------------------------------------------
# Main: Dynamic Society Configuration
# --------------------------------------------------
st.header("Configure Your RolePlaying Session")
st.markdown("Customize the details for your session:")

task_prompt = st.text_area(
    "Task Prompt", 
    value="Develop a comprehensive marketing strategy for an innovative AI startup launching a new agentic framework.", 
    height=120
)
user_role_name = st.text_input("AI User Role Name", value="A AI engineer ")
assistant_role_name = st.text_input("AI Assistant Role Name", value="A seasoned marketing strategist")
round_limit = st.number_input("Number of Conversation Rounds", min_value=1, max_value=10, value=5, step=1)

st.markdown("---")

# --------------------------------------------------
# Step 1: Initialize GPT‑4O Mini Model
# --------------------------------------------------
st.subheader("Step 1: Initialize Model")
st.markdown("Initializing GPT‑4O mini model for the conversation...")
gpt4o_model = create_gpt4o_model()
st.write("GPT‑4O mini model initialized.")

# --------------------------------------------------
# Step 2: Configure the Society Session Dynamically
# --------------------------------------------------
st.subheader("Step 2: Configure Society Session")
society = create_society(task_prompt, user_role_name, assistant_role_name, gpt4o_model)
st.write("RolePlaying Society session configured successfully.")

# --------------------------------------------------
# Step 3: Run the Society Session (Conversation Rounds)
# --------------------------------------------------
st.subheader("Step 3: Run the Society Session")
st.markdown("Click the button below to run the conversation rounds. Intermediate outputs for each round will be displayed.")

def is_terminated(response):
    if response.terminated:
        role = response.msg.role_type.name
        reason = response.info.get('termination_reasons', 'Unknown reason')
        st.write(f"**AI {role} terminated due to {reason}**")
    return response.terminated

if st.button("Run RolePlaying Session"):
    conversation_output = []
    input_msg = society.init_chat()  # Get the initial message from the society
    final_message = None

    for i in range(int(round_limit)):
        st.markdown(f"**Round {i+1}:**")
        assistant_response, user_response = society.step(input_msg)
        
        # Check if session terminated early
        if assistant_response.terminated or user_response.terminated:
            st.write("Session terminated early.")
            break
        
        # Capture outputs for each round
        conversation_output.append((f"Round {i+1} - AI User", user_response.msg.content))
        conversation_output.append((f"Round {i+1} - AI Assistant", assistant_response.msg.content))
        
        st.markdown(f"**AI User:** {user_response.msg.content}")
        st.markdown(f"**AI Assistant:** {assistant_response.msg.content}")
        st.markdown("---")
        
        input_msg = assistant_response.msg
        final_message = assistant_response.msg

    st.markdown("### Final Output from Society Session")
    if final_message:
        st.markdown(final_message.content)
    else:
        st.write("No final output produced from the society session.")

    # --------------------------------------------------
    # Step 4: Final Summarization using AIML DeepSeek
    # --------------------------------------------------
    st.subheader("Step 4: Final Summarization")
    st.markdown("Processing the final output with AIML DeepSeek for a polished summary...")
    
    aiml_model = ModelFactory.create(
        model_platform=ModelPlatformType.AIML,
        model_type='deepseek/deepseek-r1',
        model_config_dict={"max_tokens": 1500}
    )
    summarizer_agent = ChatAgent(
        system_message=BaseMessage.make_assistant_message(
            role_name="Final Summarizer",
            content="Summarize the conversation above and extract the key points of the marketing strategy."
        ),
        model=aiml_model,
    )
    
    summarization_response = summarizer_agent.step(final_message.content)
    st.markdown("### Final Summarized Output")
    st.write(summarization_response.msgs[0].content)
