# Several specific folders of the mailbox are to be checked.

# Messages from several different correspondents are to be extracted to unique folders.

import imaplib
import email
from email.header import decode_header
import os
import hashlib
import codecs
import sys
import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')



# Configuration
IMAP_SERVER = 'imap.yandex.com'
EMAIL_ACCOUNT = 'm.pitsukov@tcnordproject.ru'
EMAIL_PASSWORD = 'nDj@gXaOm%j|e*Ni7'
FOLDERS_TO_CHECK = ['Dikson_test']
#'2_Dudinka_disps'
CORRESPONDENTS = {
    '<np.dikson@ashipping.ru>': '/home/mike-pi/Documents/coding/projects/disp/data/dikson',
    
}

# 'sp.dudinka@ashipping.ru': '/home/mike-pi/Documents/coding/projects/disp/data/dudinka'
SUBJECT_KEYWORD = 'Дисп'

# Function to generate a unique hash for each message
def generate_message_hash(msg):
    msg_str = msg.as_string()
    return hashlib.sha256(msg_str.encode('koi8-r')).hexdigest()

# Function to check if a message is already saved
def is_message_saved(msg_hash, output_folder):
    for filename in os.listdir(output_folder):
        with open(os.path.join(output_folder, filename), 'r', encoding='koi8-r') as f:
            if msg_hash in f.read():
                return True
    return False

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.debug = 4
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

# Iterate over each folder to check
for folder in FOLDERS_TO_CHECK:
    mail.select(folder)
    
    # Search for messages from certain correspondents with a certain subject
    for correspondent, output_folder in CORRESPONDENTS.items():
        search_query = f'(FROM "{correspondent}")'
        # SUBJECT "{SUBJECT_KEYWORD}"
      
        search_query = search_query.encode('koi8-r')
        status, messages = mail.search(None, search_query)
        
        
        # Convert messages to a list of email IDs
        email_ids = messages[0].split()
                
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Iterate over each email ID
        for email_id in email_ids:
            # Fetch the email message by ID
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            # Parse the raw email message
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Generate a unique hash for the message
            msg_hash = generate_message_hash(msg)
            
            # Check if the message is already saved
            if is_message_saved(msg_hash, output_folder):
                print(f"Message with hash {msg_hash} already saved in {output_folder}. Skipping.")
                continue
            
            # Extract the subject and sender
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'koi8-r')
            
            sender, encoding = decode_header(msg.get('From'))[0]
            if isinstance(sender, bytes):
                sender = sender.decode(encoding if encoding else 'koi8-r')
            
            # Save the message to a file
            filename = msg_hash[:5]
            # f"{sender.replace('@', '_').replace('.', '_')}.txt"
            # _{subject.replace(' ', '_')[:9]}
            # print(filename.strip('<>'))
            with open(os.path.join(output_folder, filename), 'w', encoding='koi8-r') as f:
                f.write(f"Hash: {msg_hash}\n")
                # f.write(f"Subject: {subject}\n")
                f.write(f"From: {sender}\n")
                f.write(f"To: {msg['To']}\n")
                f.write(f"Date: {msg['Date']}\n\n")
                # body = msg.get_payload(decode=True).decode(encoding if encoding else 'koi8-r')
                # f.write(body)
                
                # If the message is multipart, iterate over each part
                if msg.is_multipart():
                    # continue
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        # body = part.get_payload(decode=True).decode(encoding if encoding else 'koi8-r')
                        # f.write(body)
                        
                        # Skip any attachments
                        if "attachment" in content_disposition:
                            continue
                        
                        # Extract the text content
                        if content_type == "text/plain":
                            #  or content_type == "text/html" 
                            body = part.get_payload(decode=True).decode(encoding='koi8-r')
                                # encoding if encoding else 'koi8-r')
                            f.write(body)
                else:
                    # If the message is not multipart, just extract the payload
                    body = msg.get_payload(decode=True).decode(encoding if encoding else 'koi8-r')
                    f.write(body)

            with codecs.open(os.path.join(output_folder, filename), 'r', encoding=encoding) as infile:
            # Read the content
                content = infile.read()
        
            # Open the output file with UTF-8 encoding
            with codecs.open(os.path.join(output_folder, filename), 'w', encoding='utf-8') as outfile:
                # Write the content
                outfile.write(content)

# Close the connection and logout
mail.close()
mail.logout()

print("Extraction completed.")


"""
Explanation:
Configuration:

IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD, FOLDERS_TO_CHECK, CORRESPONDENTS, and SUBJECT_KEYWORD are configured as before.

CORRESPONDENTS is now a dictionary where the key is the correspondent's email address and the value is the output folder name for that correspondent.

Message Hash:

The generate_message_hash function remains the same, generating a unique hash for each message.

Check if Message is Saved:

The is_message_saved function now takes an additional parameter output_folder to check if the message hash is already present in the specific output folder.

Iterate Over Folders:

The script iterates over each folder specified in FOLDERS_TO_CHECK and selects it for processing.

Search and Extract Messages:

For each correspondent, the script constructs a search query to find messages with the specified subject keyword.

It then processes each matching message, checks if it is already saved, and if not, saves it to the corresponding output folder.

Handling Multipart Messages:

The script handles multipart messages similarly to the previous version, extracting the plain text part and ignoring any attachments.

Closing the Connection:

The script closes the IMAP connection after processing all messages.

Notes:
Security: Be cautious with storing passwords in scripts. Consider using environment variables or a secure vault for credentials.

Error Handling: The script assumes that the IMAP server is accessible and that the credentials are correct. You may want to add error handling for more robustness.

Encoding: The script handles encoding issues by decoding the subject and sender using the appropriate encoding if available.

This script ensures that each message is only saved once by using a unique hash to identify each message and saves messages from different correspondents 
to unique folders. Adjust the configuration variables as needed for your specific use case.
"""