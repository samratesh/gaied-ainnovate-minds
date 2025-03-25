from langchain_core.output_parsers import JsonOutputParser, CommaSeparatedListOutputParser
from pydantic import BaseModel, Field
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from enum import Enum
from LLM import call_gemini
import json
from types import SimpleNamespace

class KeyData(BaseModel):
    key_data : dict = Field(description="Key attributes of the request email")

def extract_data(email_body, requestType):
    preamble = ("\n"
                "Your ability to extract and summarize this information accurately is essential for effective "
                "Commercial Bank Lending Services. Pay close attention to the request email content provided and "
                "extract the key attributes of the request of the email provided in a JSON format."
                "The intent of the email is " + requestType.intent + ".\n"
                "The request type is: " + requestType.request_type + "and the sub-request type is" + requestType.sub_request_type + ".\n"
                "Return a json format only.\n")
    postamble = "Do not include any explanation in the reply. Only include the extracted information in the reply."
    system_template = "{preamble}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "{format_instructions}\n{raw_file_data}\n{postamble}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    parser = PydanticOutputParser(pydantic_object=KeyData)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    request = chat_prompt.format_prompt(preamble=preamble,
                                        format_instructions=parser.get_format_instructions(),
                                        raw_file_data=email_body,
                                        postamble=postamble).to_messages()

    response = call_gemini(request, parser)
    return response