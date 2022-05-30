import smtplib


class Email:

    def __init__(self, sender: str, password: str) -> None:
        self.sender = sender
        self.password = password

        self.email_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.email_server.starttls()

    def send_message(self, reciever: str, title: str, message: str) -> bool:
        try:
            self.email_server.login(self.sender, self.password)
            self.email_server.sendmail(self.sender, reciever, f"Subject: {title}\n{message}")
            return True
        except Exception as error:
            print(f'[!] SMTP error: {error}')
            return False
