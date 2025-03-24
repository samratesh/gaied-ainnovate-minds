from langchain.chains import LLMChain
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = ""

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)

def call_gemini(request):
    response = llm.invoke(request)

    if response and response.content:
        return response.content
    else:
        return "No content received"
