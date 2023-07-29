import datetime
import smtplib

from django.conf import settings
from django.core.mail import send_mail

from newsletters.models import Newsletter, Client, Content, Trial


## TODO: Remove after finish
def log(message):
    message = str(datetime.datetime.now()) + ':   ' + message + '\n'
    with open('/Users/markpcv/Desktop/test/test.txt', 'a') as f:
        f.write(message)


def get_content(newsletter: Newsletter):
    """
    This function returns content object of the newsletter
    """
    content = Content.objects.get(settings=newsletter)
    return content


def send_newsletter(newsletter: Newsletter, content: Content):
    """
    Sends a newsletter to every client in the database
    """
    # Get all clients
    clients = Client.objects.all()
    # Send email to each client
    for client in clients:
        # Create trial for mailing service
        trial = Trial(status='created', response=None, content=content, client=client)
        # TODO: REMOVE IF STATEMENT
        # if client.fullname == "Test Testov":
        try:
            send_mail(
                subject=content.title,
                message=content.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
            )
            log(f'Sending email for newsletter @ {newsletter.time} to {client.email}')
            trial.status = 'successful'

        except smtplib.SMTPException as e:
            error_code = e.smtp_code
            error_message = e.smtp_error
            log(str(error_code) + ": " + error_message.decode('utf-8'))
            trial.status = 'unsuccessful'
            trial.response = (f'Error code: {error_code}\n'
                              f'Message: {error_message.decode("utf-8")}')
        finally:
            # Save a record for trial
            trial.save()


def check_trials(content: Content) -> bool:
    """
    Checks if newsletter is successfully delivered to every client
    """
    # Get all clients
    clients = Client.objects.all()
    for client in clients:
        # Get last trial for a client
        trial = Trial.objects.all().filter(client=client, content=content).last()
        if trial.status == 'unsuccessful':
         return False

    return True


def check_job():
    """
    This is a main algorithm of scheduler for mailing service
    """
    newsletters = Newsletter.objects.all()
    for newsletter in newsletters:
        # Change status of newsletter
        if newsletter.status.lower() ==  'created':
            newsletter.status = 'started'
            newsletter.save()
        # Send email when current time surpass scheduled time
        if newsletter.time <= datetime.datetime.now().time():
            # Get content from newsletter
            content = get_content(newsletter)
            # Send email to each client
            send_newsletter(newsletter, content)
            # Check if newsletter has been delivered to everyone
            if check_trials(content):
                # Change newsletter status and save it
                newsletter.status = 'finished'
                newsletter.save()


