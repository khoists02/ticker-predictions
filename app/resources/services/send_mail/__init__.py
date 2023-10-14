from resources.services.mail import mail
from flask_mail import Message
from flask import render_template


class SendMailStockService:
    def __init__(self) -> None:
        self.mail = mail

    def send_email(self, ticker, per, close, updatedAt, username, link):
        subject = 'Stock Notification Alert! {}'.format(ticker)
        msg = Message(subject=subject,
                      sender='stockapplication@gmail.com', recipients=['khoile@gmail.com'])
        # msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
        msg.html = render_template(
            'notification.html', username=username, link=link, ticker=ticker, per=per, close=close, updatedAt=updatedAt)
        self.mail.send(message=msg)
