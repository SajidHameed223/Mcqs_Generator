import os
import sys
import traceback
import json
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from src.logger import logging
# from src.utlis import read_file, get_table_data

# Import Langchain dependencies
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

# Initialize the OpenAI Chat model
llm = ChatOpenAI(
    openai_api_key=api_key,
    base_url=base_url,
    model_name='gpt-4o',
    temperature=0.9,
)
st.title("Multiple Choice Question Generator")
# Define the prompt template    
st.file_uploader("Upload the text file", type=['txt'])
num_question = st.number_input("Enter the number of questions", min_value=1, max_value=10, value=5)
topic = st.text_input("Enter the topic of the quiz", placeholder="Enter the topic of the quiz")
tone = st.text_input("Enter the tone of the questions", placeholder="Enter the tone of the questions")
subject = st.text_input("Enter the subject of the quiz",placeholder="Enter the subject of the quiz")
st.button('Generate Questions')