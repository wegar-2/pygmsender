from pygmsender.email_sender import EmailSender


class GmailSender(EmailSender):  # pylint: disable=R0903

    def __init__(self, sender: str, password: str):
        super().__init__(
            sender=sender,
            server="smtp.gmail.com",
            password=password,
            port=587
        )
