from ocr import ocr_func
from Classification import classify_email
from duplicateCheck import duplicate_check
from processEML import process_eml
eml_path = '/Users/amratesh/123.eml' # Path to the email file


def process_email(eml_path):
    if duplicate_check(eml_path): # Check if the email is a duplicate
        return "Email is a duplicate"
    email_data = process_eml(eml_path) # Process the email
    type = classify_email(email_data) # Classify the email
    return type

print(process_email(eml_path))
