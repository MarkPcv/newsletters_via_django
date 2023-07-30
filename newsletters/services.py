import datetime
import os
import pytz  # module to convert timezone
from dateutil.relativedelta import relativedelta # package from monthly dates
import smtplib  # library to handle SMTP exceptions

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from newsletters.models import Newsletter, Client, Content, Trial

FREQUENCY = {
    'daily': datetime.timedelta(days=1),
    'weekly': datetime.timedelta(weeks=1),
    'monthly': relativedelta(months=1)
}


## TODO: Remove after finish
def log(message):
    message = str(datetime.datetime.now()) + ':   ' + message + '\n'
    with open('/Users/markpcv/Desktop/test/test.txt', 'a') as f:
        f.write(message)


def log_trial(trial: Trial):
    """
    Record each trial of mailing servie
    """
    message = (trial.date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d/%m/%Y @ %H:%M')
               + '   ' + trial.status
               + '  Client: ' + trial.client.email
               + '  Response: ' + str(trial.response)) + '\n'

    with open(os.path.join(settings.LOGS_ROOT, 'logs.txt'), 'a') as f:
        f.write(message)


def get_content(newsletter: Newsletter):
    """
    This function returns content object of the newsletter
    """
    content = Content.objects.get(settings=newsletter)
    return content


def is_scheduled(newsletter: Newsletter) -> bool:
    """
    This function checks if schedule has been met
    """
    # Get content of newsletter
    content = get_content(newsletter)
    # Get last trial
    last_trial = Trial.objects.all().filter(content=content).last()
    # Validate trial
    if not last_trial:
        return True
    # Find next date for mailing based on settings
    increment = FREQUENCY[newsletter.frequency.lower()]
    # Get date from last trial and add time from newsletter settings
    date_time = datetime.datetime.combine(last_trial.date.date(), newsletter.time)
    # Find next schedule date
    next_datetime =  date_time + increment
    # Validate the emailing procedure
    return next_datetime <= datetime.datetime.now()


def send_newsletter(newsletter: Newsletter, content: Content):
    """
    Sends a newsletter to every client in the database
    """
    # Get all clients
    clients = Client.objects.all().filter(owner=newsletter.owner)
    # Send email to each client
    for client in clients:

        # Create trial for mailing service
        trial = Trial(status='created', response=None,
                      content=content, client=client)

        try:
            send_mail(
                subject=content.title,
                message=content.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
            )
            trial.status = 'successful'

        # Handle SMTP service exceptions
        except smtplib.SMTPException as e:
            error_code = e.smtp_code
            error_message = e.smtp_error
            trial.status = 'unsuccessful'
            trial.response = (f'Error code: {error_code} '
                              f'Message: {error_message.decode("utf-8")}')
        finally:
            # Save a record for trial
            trial.save()
            # Log a trial
            log_trial(trial)


## TODO: perhaps not needed
def check_trials(content: Content) -> bool:
    """
    Checks if newsletter is successfully delivered to every client
    """
    # Get all clients
    clients = Client.objects.all()
    for client in clients:
        # Get last trial for a client
        trial = Trial.objects.all().filter(client=client,
                                           content=content).last()
        if trial.status == 'unsuccessful':
            return False

    return True


def is_active(newsletter:Newsletter) -> bool:
    # Check newsletter status
    return newsletter.status != 'finished'


def check_job():
    """
    This is a main algorithm of scheduler for mailing service
    """
    newsletters = Newsletter.objects.all()
    for newsletter in newsletters:

        # Send email when current time surpass scheduled time
        if (newsletter.time <= datetime.datetime.now().time()
                and is_scheduled(newsletter)) and is_active(newsletter):
            # Change status of newsletter
            newsletter.status = 'started'
            newsletter.save()
            # Get content from newsletter
            content = get_content(newsletter)
            # Send email to each client
            send_newsletter(newsletter, content)


def get_newsletter_cache():
    """
    Function to get cache of newsletters
    """
    if settings.CACHE_ENABLED:
        key = 'newsletter_list'
        newsletter_list = cache.get(key)
        if newsletter_list is None:
            newsletter_list = Newsletter.objects.all()
            cache.set(key, newsletter_list)
    else:
        newsletter_list = Newsletter.objects.all()

    return newsletter_list