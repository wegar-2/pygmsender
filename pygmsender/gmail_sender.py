from pygmsender.email_sender import EmailSender


class GmailSender(EmailSender):

    def __init__(self, str_sender: str, str_pass: str):
        super().__init__(
            str_sender=str_sender,
            str_server="smtp.gmail.com",
            str_pass=str_pass,
            int_port=587
        )

