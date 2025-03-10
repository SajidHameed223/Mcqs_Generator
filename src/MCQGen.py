import os
import sys
import traceback
import json
from dotenv import load_dotenv
import pandas as pd

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

# Define the prompt template
template = """
Generate a multiple choice quiz for the following topic:
Topic: {topic}

The quiz should have {num_questions} questions. Each question should have four options (a, b, c, d) and one correct answer.
The tone of the questions should be {tone}.

Output the quiz in the following JSON format:
{
    "questions": [
        {
            "question": "Question text",
            "options": {
                "a": "Option A",
                "b": "Option B",
                "c": "Option C",
                "d": "Option D"
            },
            "correct_answer": "a"
        },
        ...
    ]
}
"""
student_prompt = PromptTemplate(
    input_variables=["topic", "num_questions", "tone"],
    template=template,
)

student_chain = LLMChain(
    llm=llm,
    prompt_template=student_prompt,
    output_variables=["quiz"],
    verbose=True,
)
# Define the prompt template for evaluating the generated quiz
evaluation_template = """
Evaluate the following multiple choice quiz to determine if it is appropriate for the given subject:
Subject: {subject}

Quiz:
{quiz}

Provide feedback on whether the quiz is appropriate for the subject and suggest any necessary changes.
"""

teacher_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=evaluation_template,
)
teacher_chain = LLMChain(
    llm=llm,
    prompt_template=teacher_prompt,
    output_variables=["feedback"],
    verbose=True,
)
final_sequence = SequentialChain(
    chains=[student_chain, teacher_chain],
    input_variables = ["topic", "num_questions", "tone", "subject"],
    output_variables = ["quiz", "feedback"],
    verbose=True,       
)
Topic = 'Python lists'
num_questions = 5
tone = 'formal'
subject = 'Python Programming'

output = final_sequence(
    {
    "topic": Topic,
    "num_questions": num_questions,
    "tone": tone,
    "subject": subject,
    }
)
print(output)