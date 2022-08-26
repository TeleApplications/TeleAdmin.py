import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email import encoders


class EmailManager:
    def __init__(self, username: str, password: str, receiver: str, attachments: list = None):
        self.username = username
        self.password = password
        self.receiver = receiver
        self.attachments = attachments

    def create_email(self, subject: str, attachments: list[str, ...] = None) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = self.receiver
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())

                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={attachment}", )
                msg.attach(part)
        return msg

    def send_email(self, message: create_email) -> None:
        try:
            smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        except Exception:
            smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)

        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(self.username, self.password)
        smtpObj.sendmail(message["From"], message["To"], message.as_string())

        smtpObj.quit()


if __name__ == '__main__':
    from json_manager import Json

    data = Json().read()["email"]
    e = EmailManager(data["username"], data["password"], data["receiver"], ["logs.txt", "test.py"])
    email = e.create_email(subject="TEST", attachments=e.attachments)
    e.send_email(email)
