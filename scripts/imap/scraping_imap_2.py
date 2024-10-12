import imaplib
import email
from email.header import decode_header
import os
import hashlib

# Configuration
IMAP_SERVER = 'imap.example.com'
EMAIL_ACCOUNT = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'
FOLDER_NAME = 'INBOX'
CORRESPONDENTS = ['sender1@example.com', 'sender2@example.com']
SUBJECT_KEYWORD = 'Important'
OUTPUT_FOLDER = 'extracted_messages'

# Create output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to generate a unique hash for each message
def generate_message_hash(msg):
    msg_str = msg.as_string()
    return hashlib.sha256(msg_str.encode('utf-8')).hexdigest()

# Function to check if a message is already saved
def is_message_saved(msg_hash):
    for filename in os.listdir(OUTPUT_FOLDER):
        with open(os.path.join(OUTPUT_FOLDER, filename), 'r', encoding='utf-8') as f:
            if msg_hash in f.read():
                return True
    return False

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
mail.select(FOLDER_NAME)

# Search for messages from certain correspondents with a certain subject
search_query = f'(FROM {" OR FROM ".join(CORRESPONDENTS)} SUBJECT "{SUBJECT_KEYWORD}")'
status, messages = mail.search(None, search_query)

# Convert messages to a list of email IDs
email_ids = messages[0].split()

# Iterate over each email ID
for email_id in email_ids:
    # Fetch the email message by ID
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    
    # Parse the raw email message
    msg = email.message_from_bytes(msg_data[0][1])
    
    # Generate a unique hash for the message
    msg_hash = generate_message_hash(msg)
    
    # Check if the message is already saved
    if is_message_saved(msg_hash):
        print(f"Message with hash {msg_hash} already saved. Skipping.")
        continue
    
    # Extract the subject and sender
    subject, encoding = decode_header(msg['Subject'])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else 'utf-8')
    
    sender, encoding = decode_header(msg.get('From'))[0]
    if isinstance(sender, bytes):
        sender = sender.decode(encoding if encoding else 'utf-8')
    
    # Save the message to a file
    filename = f"{sender.replace('@', '_').replace('.', '_')}_{subject.replace(' ', '_')}.txt"
    with open(os.path.join(OUTPUT_FOLDER, filename), 'w', encoding='utf-8') as f:
        f.write(f"Hash: {msg_hash}\n")
        f.write(f"Subject: {subject}\n")
        f.write(f"From: {sender}\n")
        f.write(f"To: {msg['To']}\n")
        f.write(f"Date: {msg['Date']}\n\n")
        
        # If the message is multipart, iterate over each part
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Skip any attachments
                if "attachment" in content_disposition:
                    continue
                
                # Extract the text content
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(encoding if encoding else 'utf-8')
                    f.write(body)
        else:
            # If the message is not multipart, just extract the payload
            body = msg.get_payload(decode=True).decode(encoding if encoding else 'utf-8')
            f.write(body)

# Close the connection and logout
mail.close()
mail.logout()

print(f"Extracted {len(email_ids)} messages and saved them to {OUTPUT_FOLDER}.")

'''
Explanation:
Configuration:

The configuration variables remain the same as before.

Message Hash:

A function generate_message_hash is added to generate a unique hash for each message using the SHA-256 algorithm. This hash is based on the entire message content.

Check if Message is Saved:

A function is_message_saved checks if the message hash is already present in any of the saved files in the output folder. If the hash is found, the message is considered already saved.

Fetching and Saving Messages:

The script fetches each matching message, generates a hash, checks if the message is already saved, and if not, saves it to a text file in the specified output folder. The filename is constructed using the sender's email address and the subject.

Handling Multipart Messages:

The script handles multipart messages similarly to the previous version, extracting the plain text part and ignoring any attachments.

Closing the Connection:

The script closes the IMAP connection after processing all messages.

Notes:
Security: Be cautious with storing passwords in scripts. Consider using environment variables or a secure vault for credentials.

Error Handling: The script assumes that the IMAP server is accessible and that the credentials are correct. You may want to add error handling for more robustness.

Encoding: The script handles encoding issues by decoding the subject and sender using the appropriate encoding if available.

This script ensures that each message is only saved once by using a unique hash to identify each message. Adjust the configuration variables as needed for your specific use case.
'''