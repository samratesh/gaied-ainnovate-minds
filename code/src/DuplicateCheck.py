import datetime
import json
import eml_parser

processed_emails = [] # Stores the list of processed emails

def duplicate_check(eml_path):
    with open(eml_path, 'rb') as fhdl:
        raw_email = fhdl.read()

    ep = eml_parser.EmlParser()
    parsed_eml = ep.decode_email_bytes(raw_email)
    h = parsed_eml.get("header")['header']
    prev = ""
    if 'in-reply-to' in h:
        prev = h['in-reply-to']

    if prev in processed_emails:
        processed_emails.append(h['message-id'])
        return True
    else:
        return False

def add_to_processed_emails(eml_path):
    with open(eml_path, 'rb') as fhdl:
        raw_email = fhdl.read()

    ep = eml_parser.EmlParser()
    parsed_eml = ep.decode_email_bytes(raw_email)
    h = parsed_eml.get("header")['header']
    processed_emails.append(h['message-id'])
