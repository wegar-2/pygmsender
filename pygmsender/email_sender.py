import logging
import os.path
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from typing import Optional


class EmailSender:

    def __init__(self, sender: str, server: str, password: str, port: int = 587):
        self._PORT = port
        self._SERVER = server
        self._SENDER = sender
        self._PASS = password

    def send_email(
            self,
            email_subject: str,
            email_text: str,
            recipients: list[str],
            attachments_paths: Optional[list[str]] = None
    ):

        session = smtplib.SMTP(self._SERVER, self._PORT)
        session.starttls()
        if self._PASS is not None:
            session.login(user=self._SENDER, password=self._PASS)
        else:
            session.login(user=self._SENDER) # noqa

        message = self._get_msg_content(
            str_email_subject=email_subject,
            l_str_attachments_paths=attachments_paths,
            l_str_recipients=recipients,
            str_email_text=email_text
        )

        session.sendmail(self._SENDER, recipients, message.as_string())
        session.quit()

    def _get_msg_content(
            self,
            str_email_subject: str,
            l_str_recipients: list[str],
            str_email_text: Optional[str] = None,
            l_str_attachments_paths: Optional[list[str]] = None
    ):

        message = MIMEMultipart()
        message["Subject"] = str_email_subject
        message["From"] = self._SENDER
        message["To"] = ",".join(l_str_recipients)

        if str_email_text is not None:
            mime_text = MIMEText(str_email_text, "plain")
            message.attach(mime_text)

        if l_str_attachments_paths is not None:
            for iter_attachment in l_str_attachments_paths:
                if not os.path.exists(iter_attachment):
                    logging.warning("The following file does not exist and cannot be attached to the email: ",
                                    iter_attachment)
                else:
                    with open(iter_attachment, "rb") as fil:
                        part = MIMEApplication(fil.read(), Name=basename(iter_attachment))
                        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(iter_attachment)
                        message.attach(part)

        return message
