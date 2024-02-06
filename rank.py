import re
from mail import extractEmails
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain_openai import OpenAI
from config import set_environment

set_environment()

def emailStr (emailObjectList) :
    s = ""
    for i in range(len(emailObjectList)) :
        s += f"  {i+1}. "
        s += f"SENDER: {emailObjectList[i].sender}"
        s += str(emailObjectList[i].subject) + " " + str(emailObjectList[i].summary)
        s += "  "
    return s

def rankedEmails (N=5) :
    Emails = extractEmails(N)
    instruction = """Give each email below a priority number between 0 to 1. 
                    With 0 being not urgent to 1 being very urgent. 
                    Generate only the priority numbers, in a list"""

    question = instruction + emailStr(Emails)
    template = "Instructions: {question} Response:"

    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm = OpenAI()
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    ranks = llm_chain.invoke(question)['text']

    for i in range(len(Emails)) :
        Emails[i].rank = ranks[i]
    
    return Emails










  


