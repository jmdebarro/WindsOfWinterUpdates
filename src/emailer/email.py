import smtplib
from email.message import EmailMessage
import dotenv, os

class Emailer:
    """Emails Winds of Winter updates"""

    def __init__(self, blog_email=False):
        self.blog_email = blog_email
        return

    # Emails based on updates or news in blog and twitter
    def email(self):
        if self.blog_email:
            dotenv.load_dotenv()
            blog_url = "https://georgerrmartin.com/notablog/"

            # Create message object
            msg = EmailMessage()
            email_content = f"Winds of Winter update on blog {blog_url}"

            # Initialize msg object
            msg['Subject'] = "Winds of Winter Update"
            msg['From'] = os.environ["EMAIL"]
            msg['To'] = "jmdebarro@gmail.com"

            s = smtplib.SMTP("smtp-mail.outlook.com", port=587)
            s.starttls()
            s.login(os.environ["EMAIL"], os.environ["PASS"])
            
            msg.set_content(email_content)
            s.send_message(msg)
            s.quit()
            return "Update to Email"
        return "No Update"