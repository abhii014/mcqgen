import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logger
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key=KEY, model_name="llama-3.1-8b-instant", temperature=0.5)

# Load RESPONSE_JSON from file
with open("response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

TEMPLATE2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity \
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities.
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

review_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)

quiz_chain = quiz_prompt | llm | StrOutputParser()
review_chain = review_prompt | llm | StrOutputParser()

def generate_evaluate_chain(text, number, subject, tone, response_json):
    try:
        logger.info("Generating quiz...")
        quiz = quiz_chain.invoke({
            "text": text,
            "number": number,
            "subject": subject,
            "tone": tone,
            "response_json": json.dumps(response_json)
        })

        logger.info("Reviewing quiz...")
        review = review_chain.invoke({
            "subject": subject,
            "quiz": quiz
        })

        return {"quiz": quiz, "review": review}

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise e