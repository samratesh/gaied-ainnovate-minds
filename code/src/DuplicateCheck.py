import datetime
import json
import eml_parser


def duplicate_check(eml_path):
    processed_emails = open('.processed_emails', 'r') # Stores the list of processed emails
    with open(eml_path, 'rb') as fhdl:
        raw_email = fhdl.read()

    ep = eml_parser.EmlParser()
    parsed_eml = ep.decode_email_bytes(raw_email)
    h = parsed_eml.get("header")['header']
    prev = "."
    if 'in-reply-to' in h:
        prev = h['in-reply-to']

    for line in processed_emails:
        if prev in line:
            return True
        if h['message-id'] in line:
            return True
    return False

def add_to_processed(eml_path):
    with open(eml_path, 'rb') as fhdl:
        raw_email = fhdl.read()

    ep = eml_parser.EmlParser()
    parsed_eml = ep.decode_email_bytes(raw_email)
    h = parsed_eml.get("header")['header']
    processed_emails = open('.processed_emails', 'a')
    processed_emails.write(str(h['message-id']) + '\n')
    processed_emails.close()