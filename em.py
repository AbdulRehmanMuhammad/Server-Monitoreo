import smtplib
from email.message import EmailMessage


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)

    gmail_user = 'keagan78@ethereal.email'
    gmail_password = 'Y4KZhqbTVrDvSj5GSe'
    msg['Subject'] = subject
    msg['From'] = "keagan78@ethereal.email"
    msg['To'] = to

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(gmail_user, gmail_password)
    s.send_message(msg)

    subject = 'Your server is down!'
    body = 'Your Server is down!'
    f'Subject: {subject}\n\n{body}'
    s.quit()


if __name__ == '__main__':
    email_alert("Your server is down!", "Test!", "davidpapa726@gmail.com")
