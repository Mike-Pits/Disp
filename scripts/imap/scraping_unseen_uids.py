import imaplib
import email
from email.header import decode_header
import os

# Configuration

IMAP_SERVER = 'imap.yandex.com'
EMAIL_ACCOUNT = ''
EMAIL_PASSWORD = ''
FOLDERS_TO_CHECK = []
#'2_Dudinka_disps'
CORRESPONDENTS = {
    '<np.dikson@ashipping.ru>': '/home/mike-pi/Documents/coding/projects/disp/data/dikson',
    
}

# 'sp.dudinka@ashipping.ru': '/home/mike-pi/Documents/coding/projects/disp/data/dudinka'
SUBJECT_KEYWORD = 'Дисп'


MAILBOX_FOLDER = 'Dikson_test'
STORAGE_FOLDER = '/home/mike-pi/Documents/coding/projects/disp/data/dikson/unseen'
UID_FILE = '/home/mike-pi/Documents/coding/projects/disp/data/dikson/unseen/retrieved_uids.txt'

# Function to connect to the IMAP server
def connect_to_imap():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select(MAILBOX_FOLDER)
    return mail

# Function to retrieve UIDs of already retrieved emails
def get_retrieved_uids():
    if os.path.exists(UID_FILE):
        with open(UID_FILE, 'r') as f:
            return set(f.read().splitlines())
    return set()

# Function to save UIDs of retrieved emails
def save_retrieved_uids(uids):
    with open(UID_FILE, 'a') as f:
        for uid in uids:
            f.write(f"{uid}\n")

# Function to retrieve new emails
def retrieve_new_emails(mail):
    retrieved_uids = get_retrieved_uids()
    status, messages = mail.uid('search', None, 'UNSEEN')
    if status != 'OK':
        raise Exception("No messages found")

    uids = messages[0].split()
    new_uids = [uid for uid in uids if uid.decode('utf-8') not in retrieved_uids]

    for uid in new_uids:
        status, msg_data = mail.uid('fetch', uid, '(RFC822)')
        if status != 'OK':
            print(f"Error fetching message {uid}")
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')

        from_, encoding = decode_header(msg.get('From'))[0]
        if isinstance(from_, bytes):
            from_ = from_.decode(encoding if encoding else 'utf-8')

        print(f"Processing message UID {uid}: Subject: {subject}, From: {from_}")

        # Save the email to a file
        filename = os.path.join(STORAGE_FOLDER, f"{uid}.eml")
        with open(filename, 'wb') as f:
            f.write(msg_data[0][1])

    save_retrieved_uids(new_uids)

# Main function
def main():
    mail = connect_to_imap()
    retrieve_new_emails(mail)
    mail.logout()
    print('Successfully logged out')

# main()

if __name__ == "__main__":
    main()

'''

To improve the script by checking for new messages without collecting all messages from the mailbox folder, you can use the `SEARCH` command in IMAP to filter messages based on their flags or date. For example, you can search for messages that are not marked as seen (`UNSEEN`). This approach is more efficient as it avoids fetching all messages and only retrieves the new ones.

Below is an improved version of the script that uses the `UNSEEN` flag to filter new messages:

### Step 1: Install Required Libraries

Ensure you have the required libraries installed:

```bash
pip install imaplib email
```

### Step 2: Create the Python Script

```python
import imaplib
import email
from email.header import decode_header
import os

# Configuration
IMAP_SERVER = 'imap.example.com'
EMAIL_ACCOUNT = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'
MAILBOX_FOLDER = 'INBOX'
STORAGE_FOLDER = 'path/to/storage/folder'
UID_FILE = 'retrieved_uids.txt'

# Function to connect to the IMAP server
def connect_to_imap():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select(MAILBOX_FOLDER)
    return mail

# Function to retrieve UIDs of already retrieved emails
def get_retrieved_uids():
    if os.path.exists(UID_FILE):
        with open(UID_FILE, 'r') as f:
            return set(f.read().splitlines())
    return set()

# Function to save UIDs of retrieved emails
def save_retrieved_uids(uids):
    with open(UID_FILE, 'a') as f:
        for uid in uids:
            f.write(f"{uid}\n")

# Function to retrieve new emails
def retrieve_new_emails(mail):
    retrieved_uids = get_retrieved_uids()
    status, messages = mail.uid('search', None, 'UNSEEN')
    if status != 'OK':
        raise Exception("No messages found")

    uids = messages[0].split()
    new_uids = [uid for uid in uids if uid.decode('utf-8') not in retrieved_uids]

    for uid in new_uids:
        status, msg_data = mail.uid('fetch', uid, '(RFC822)')
        if status != 'OK':
            print(f"Error fetching message {uid}")
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')

        from_, encoding = decode_header(msg.get('From'))[0]
        if isinstance(from_, bytes):
            from_ = from_.decode(encoding if encoding else 'utf-8')

        print(f"Processing message UID {uid}: Subject: {subject}, From: {from_}")

        # Save the email to a file
        filename = os.path.join(STORAGE_FOLDER, f"{uid}.eml")
        with open(filename, 'wb') as f:
            f.write(msg_data[0][1])

    save_retrieved_uids(new_uids)

# Main function
def main():
    mail = connect_to_imap()
    retrieve_new_emails(mail)
    mail.logout()

if __name__ == "__main__":
    main()
```

### Explanation:

1. **Configuration**: Set the IMAP server, email account, password, mailbox folder, storage folder, and a file to store the UIDs of retrieved emails.

2. **`connect_to_imap` Function**: Connects to the IMAP server and selects the specified mailbox folder.

3. **`get_retrieved_uids` Function**: Reads the UIDs of emails that have already been retrieved from the UID file.

4. **`save_retrieved_uids` Function**: Appends the UIDs of newly retrieved emails to the UID file.

5. **`retrieve_new_emails` Function**: Retrieves new emails by searching for `UNSEEN` messages. It then compares the UIDs of these messages with the UIDs in the UID file and saves the new emails to the storage folder.

6. **`main` Function**: Connects to the IMAP server, retrieves new emails, and logs out.

### Running the Script:

- Replace the placeholders in the configuration section with your actual IMAP server, email account, password, mailbox folder, and storage folder.
- Run the script regularly using a scheduler like `cron` on Unix-based systems or Task Scheduler on Windows.

### Notes:

- **Security**: Storing passwords in plain text is not secure. Consider using environment variables or a secure vault for storing credentials.
- **Error Handling**: The script includes basic error handling, but you may want to add more robust error handling depending on your use case.
- **Performance**: This script is more efficient as it only fetches new messages that are not marked as seen.

This improved script ensures that only new messages are retrieved and processed, making it more efficient and suitable for handling large volumes of emails.'''