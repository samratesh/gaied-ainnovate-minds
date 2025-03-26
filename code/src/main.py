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
    add_to_processed(eml_path) # Add the email to the processed list
    return extracted_data.key_data
