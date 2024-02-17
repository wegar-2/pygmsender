import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from loguru import logger
from pathlib import Path


class EmailSender:  # pylint: disable=R0903

    def __init__(
            self,
            sender: str,
            server: str,
            password: str,
            port: int = 587
    ):
        self._port = port
        self._server = server
        self._sender = sender
        self._pass = password

    def send_email(
            self,
            email_subject: str,
            email_text: str,
            recipients: list[str],
            attachments_paths: Optional[list[str]] = None
    ):

        session = smtplib.SMTP(self._server, self._port)
        session.starttls()
        if self._pass is not None:
            session.login(user=self._sender, password=self._pass)
        else:
            session.login(  # pylint: disable=E1120
                user=self._sender
            ) # noqa

        message = self._get_msg_content(
            email_subject=email_subject,
            attachments_paths=attachments_paths,
            recipients=recipients,
            email_text=email_text
        )

        session.sendmail(self._sender, recipients, message.as_string())
        session.quit()

    def _get_msg_content(
            self,
            email_subject: str,
            recipients: list[str],
            email_text: Optional[str] = None,
            attachments_paths: Optional[list[Path]] = None
    ):

        message = MIMEMultipart()
        message["Subject"] = email_subject
        message["From"] = self._sender
        message["To"] = ",".join(recipients)

        if email_text is not None:
            mime_text = MIMEText(email_text, "plain")
            message.attach(mime_text)

        if attachments_paths is not None:
            for iterpath in attachments_paths:
                if not iterpath.exists():
                    logger.warning(
                        f"The following path does not exist and cannot be "
                        f"attached to the email: {iterpath}"
                    )
                if iterpath.is_dir():
                    logger.warning(
                        f"The following path exists but it is a directory "
                        f"{iterpath}"
                    )
                else:
                    with open(iterpath, "rb") as fil:
                        part = MIMEApplication(fil.read(), Name=iterpath.name)
                        part['Content-Disposition'] = (f'attachment; '
                                                       f'filename='
                                                       f'"{iterpath.name}"')
                        message.attach(part)

        return message
