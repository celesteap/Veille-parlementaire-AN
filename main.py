import feedparser
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration pour OUTLOOK
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587  # Port standard pour Outlook avec STARTTLS
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
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="background-color: #0055a4; color: white; padding: 20px; text-align: center;">
            <h1>Veille Parlementaire</h1>
        </div>
        <div style="padding: 20px; border: 1px solid #ddd;">
            <h2 style="color: #0055a4;">{entry.title}</h2>
            <p>{entry.description}</p>
            <br>
            <a href="{entry.link}" style="display: inline-block; background-color: #0055a4; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Lire le document complet</a>
        </div>
        <p style="font-size: 11px; color: #888; margin-top: 20px;">Source : Flux RSS de l'Assemblée nationale</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    try:
        # Connexion spécifique à Outlook
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() 
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"Email envoyé avec succès : {entry.title}")
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")

def run():
    feed = feedparser.parse(RSS_URL)
    
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
        for entry in reversed(new_entries):
            send_email(entry)
        
        with open("last_id.txt", "w") as f:
            f.write(feed.entries[0].id)
    else:
        print("Aucune nouveauté dans le flux.")

if __name__ == "__main__":
    run()
