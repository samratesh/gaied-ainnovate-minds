from Classification import classify_email
from DuplicateCheck import duplicate_check, add_to_processed
from ProcessEML import process_eml
from Extraction import extract_data


def process_email(eml_path):
    if duplicate_check(eml_path): # Check if the email is a duplicate
        return "Email is a duplicate"
    email_data = process_eml(eml_path) # Process the email
    request_type = classify_email(email_data) # Classify the email
    extracted_data = extract_data(email_data, request_type) # Extract the data
    extracted_data.key_data.update(request_type.__dict__) # Update the extracted data with the request
    try:
        add_to_processed(extracted_data)
    except:
        extracted_data.key_data.update({"Duplicate Error": "Email header should have message-id to support duplicate check"})
    return extracted_data.key_data
