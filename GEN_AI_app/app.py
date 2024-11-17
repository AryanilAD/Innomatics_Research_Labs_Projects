import google.generativeai as genai
import streamlit as st
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="E:\GEN AI application\.env_app\.env_app.txt")

# Load the API key from .env file
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("API key not found. Please set your API key in a .env file.")
    st.stop()

# Load system prompt from file
try:
    with open("system_prompt.txt", "r") as file:
        sys_prompt = file.read()
except FileNotFoundError:
    st.error("System prompt file (system_prompt.txt) not found. Please ensure it exists.")
    st.stop()

# Configure the Google Generative AI with the API key
genai.configure(api_key=api_key)

# Initialize the Generative AI model
try:
    model = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction=sys_prompt)
except Exception as e:
    st.error(f"Error initializing Generative AI model: {e}")
    st.stop()

# Initialize Streamlit session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Function to format chat history for the AI model
def format_history(history):
    formatted_history = []
    for entry in history:
        formatted_history.append(
            {
                "role": entry["role"],
                "parts": [{"text": entry["content"]}],
            }
        )
    return formatted_history

# Function to get AI response
def get_response(message):
    formatted_history = format_history(st.session_state.history)
    chatbot = model.start_chat(history=formatted_history)
    response = chatbot.send_message(message)

    # Append the message and response to the history
    st.session_state.history.append({"role": "user", "content": message})
    st.session_state.history.append({"role": "model", "content": response.text})

    return response.text

# Function to stream the AI's response (word by word)
def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

# Streamlit UI
st.title(":red[PygenAI] :robot_face:")
st.write("Your Personal Python Code Reviewer :mechanical_arm:")
st.image("mario.gif")

# Display chat history
for entry in st.session_state.history:
    if entry["role"] == "user":
        st.chat_message("human").write(entry["content"])
    else:
        st.chat_message("ai").write(entry["content"])

# Input box for the user's Python script
user_prompt = st.chat_input("Enter your Python script here...")

# Handle user input
if user_prompt:
    st.chat_message("human").write(user_prompt)  # Display the user's input
    with st.spinner("Analyzing your code..."):
        try:
            response = get_response(user_prompt)
            st.chat_message("ai").write(response)  # Display AI's response
        except Exception as e:
            st.error(f"Error processing the request: {e}")
