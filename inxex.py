import imaplib
import email
from email.header import decode_header
import os

# Connect to Gmail
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# Use an environment variable for the password
username = "your_email@gmail.com"
password = os.getenv("GMAIL_PASSWORD")  # Set this in your environment

try:
    imap.login(username, password)

    # Select the inbox
    imap.select("inbox")

    # Search for all emails
    status, messages = imap.search(None, "ALL")
    messages = messages[0].split()

    # Fetch and process the last 5 emails
    for msg_num in messages[-5:]:
        res, msg = imap.fetch(msg_num, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # Decode email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                print("Subject:", subject)
                # Email sender
                from_ = msg.get("From")
                print("From:", from_)
                print("=" * 50)

    # Close the connection
    imap.close()
    imap.logout()

except imaplib.IMAP4.error as e:
    print("Login failed:", str(e))
