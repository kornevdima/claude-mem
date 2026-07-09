class EmailSender:
    def send_email(self, to, subject, body):
        print(f"[email] to={to} subject={subject}")
        return True
