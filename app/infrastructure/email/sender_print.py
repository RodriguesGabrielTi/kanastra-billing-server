from infrastructure.email.sender import EmailSender


class EmailSenderPrint(EmailSender):
    def send(self, email: str, billet: str) -> None:
        print(f"Sending email to {email} with billet {billet}")
