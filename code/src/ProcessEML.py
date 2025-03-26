import email
import os

from OCR import ocr_func


def process_eml(eml_path):
    with open(eml_path) as email_file:
        email_message = email.message_from_file(email_file)
    od = os.getcwd() + '/att'
    try:
        os.mkdir(od)
    except FileExistsError:
        pass
    email_data = {'FROM': email_message['from'], 'TO': email_message['to'], 'SUBJECT': email_message['subject'],
              'DATE': email_message['date'], 'BODY': '', 'ATTACHMENT': ''}
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                message = part.get_payload(decode=True)
                plain_message = message.decode()
                email_data['BODY'] += plain_message
            else:
                output_filename = part.get_filename()
                if output_filename:
                    with open(os.path.join(od, output_filename), "wb") as of:
                        of.write(part.get_payload(decode=True))
                        email_data['ATTACHMENT'] += ocr_func(os.path.join(od, output_filename))
    return email_data
