from pydantic import BaseModel, Field
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from enum import Enum
from LLM import call_gemini
import json
from types import SimpleNamespace

class RequestTypes(str, Enum):
    Adjustment = "Adjustment"
    AU_Transfer = "AU Transfer"
    Closing_Notice = "Closing Notice"
    Commitment_Change = "Commitment Change"
    Fee_Payment = "Fee Payment"
    Money_Movement_Inbound = "Money Movement - Inbound"
    Money_Movement_Outbound = "Money Movement - Outbound"
    Generic_Request = "Generic Request"

class Intent(str, Enum):
    Inquiry = "Inquiry"
    Complaint = "Complaint"
    Request = "Request"
    Follow_up = "Follow-up"
    Acknowledgment = "Acknowledgment"

class EmailClassification(BaseModel):
    request_type: RequestTypes = Field(description="Type of request specified in the email.")
    sub_request_type: str = Field(description="Sub type of request")
    confidence: float = Field(description="Confidence of the model")
    intent: Intent = Field(description="Identify the intent of the email")

def classify_email(email_body):
    preamble = ("\n"
            "Your ability to extract and summarize this information accurately is essential for effective "
            "Commercial Bank Lending Services. Pay close attention to the request email content provided and "
            "identify the intent of the email and categorize the Request Type and the Sub-Request Type "
            "of the email provided. Remember to prioritize the content in BODY over ATTACHMENT in case of conflict.\n")
    postamble = "Do not include any explanation in the reply. Only include the extracted information in the reply."
    system_template = "{preamble}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "{format_instructions}\n{raw_file_data}\n{postamble}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    parser = PydanticOutputParser(pydantic_object=EmailClassification)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    request = chat_prompt.format_prompt(preamble=preamble,
                                    format_instructions=parser.get_format_instructions(),
                                    raw_file_data=email_body,
                                    postamble=postamble).to_messages()

    response = call_gemini(request, parser)
    return response