import logging
import os.path
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename


class EmailSender:
    _PORT = None
    _SERVER = None
    _SENDER = None
    _PASS = None

    def __init__(self, str_sender: str, str_server: str, str_pass: str, int_port: int = 587):
        self._PORT = int_port
        self._SERVER = str_server
        self._SENDER = str_sender
        self._PASS = str_pass

    def send_email(self, str_email_subject: str, str_email_text: str,
                   l_str_recipients: list[str], l_str_attachments_paths: list[str] = None):

        # create SMTP session
        session = smtplib.SMTP(self._SERVER, self._PORT)
        session.starttls()
        if self._PASS is not None:
            session.login(user=self._SENDER, password=self._PASS)
        else:
            session.login(user=self._SENDER)
        # create the message to send
        message = self.__get_msg_content(
            str_email_subject=str_email_subject, l_str_attachments_paths=l_str_attachments_paths,
            l_str_recipients=l_str_recipients, str_email_text=str_email_text)
        # send the message with attachments
        session.sendmail(self._SENDER, l_str_recipients, message.as_string())
        # close the session
        session.quit()

    def __get_msg_content(self, str_email_subject: str, l_str_recipients: list[str], str_email_text: str = None,
                          l_str_attachments_paths: list[str] = None):

        # create the message object and set its basic attributes
        message = MIMEMultipart()
        message["Subject"] = str_email_subject
        message["From"] = self._SENDER
        message["To"] = ",".join(l_str_recipients)

        # if there is any text to attach - add it
        if str_email_text is not None:
            mime_text = MIMEText(str_email_text, "plain")
            message.attach(mime_text)

        # add attachments to the message if there are any
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



