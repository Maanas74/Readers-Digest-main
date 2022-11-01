import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_login import current_user


def send_mail(mail, sub, say, link, link_say):
    message = Mail(
        from_email='singhankit3952@gmail.com',
        to_emails=mail,
        subject=sub,
        html_content=f'<h1>Readers Digest</h1><strong>{sub}</strong><br>Hello, {current_user.fname}.<br>{say}<br><a href="{link}>">{link_say}</a>')
    try:
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
       print(e.message)
