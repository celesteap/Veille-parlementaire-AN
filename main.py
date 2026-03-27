import feedparser
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration via les secrets GitHub
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_USER = os.environ['EMAIL_USER']
EMAIL_PASS = os.environ['EMAIL_PASS']
DEST_EMAIL = os.environ['DEST_EMAIL']

RSS_URL = "http://www2.assemblee-nationale.fr/feeds/detail/documents-parlementaires"

def send_email(entry):
    msg = MIMEMultipart()
    msg['Subject'] = f"🏛️ AN : {entry.title}"
    msg['From'] = EMAIL_USER
    msg['To'] = DEST_EMAIL

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #0055a4;">Nouveau document parlementaire</h2>
        <p><strong>Titre :</strong> {entry.title}</p>
        <p><strong>Description :</strong> {entry.description}</p>
        <hr>
        <a href="{entry.link}" style="background-color: #0055a4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Consulter le document</a>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def run():
    feed = feedparser.parse(RSS_URL)
    
    # On lit le dernier ID traité pour éviter les doublons
    if os.path.exists("last_id.txt"):
        with open("last_id.txt", "r") as f:
            last_id = f.read().strip()
    else:
        last_id = ""

    new_entries = []
    for entry in feed.entries:
        if entry.id == last_id:
            break
        new_entries.append(entry)

    if new_entries:
        # On traite du plus vieux au plus récent
        for entry in reversed(new_entries):
            print(f"Envoi de : {entry.title}")
            send_email(entry)
        
        # On sauvegarde le nouvel ID le plus récent
        with open("last_id.txt", "w") as f:
            f.write(feed.entries[0].id)

if __name__ == "__main__":
    run()
