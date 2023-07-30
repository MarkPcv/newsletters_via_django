from django.conf import settings
from django.db import models
from django.utils import timezone

# Model characteristics
NULLABLE = {
    'null': True,
    'blank': True,
}


class Client(models.Model):
    """A class model for client of the service"""
    email = models.EmailField(max_length=250, verbose_name='email')
    fullname = models.CharField(max_length=250, verbose_name='fullname')
    comment = models.TextField(max_length=250, verbose_name='comment',
                               **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='owner')

    def __str__(self):
        return f'{self.fullname} - {self.email}'

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        ordering = ['email']


class Newsletter(models.Model):
    """A class model for newsletter settings"""
    time = models.TimeField(default=timezone.now, verbose_name='time')
    frequency = models.CharField(max_length=50, verbose_name='frequency')
    status = models.CharField(max_length=50, verbose_name='status')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='owner')

    def __str__(self):
        return f'{self.time} at {self.frequency} - {self.status}'

    class Meta:
        verbose_name = 'newsletter'
        verbose_name_plural = 'newsletters'
        ordering = ['time']


class Content(models.Model):
    """A class model for newsletter content"""
    title = models.CharField(max_length=250, verbose_name='title')
    message = models.TextField(verbose_name='message')
    # Foreign keys
    client = models.ManyToManyField(Client, verbose_name='client')
    settings = models.ForeignKey(Newsletter, on_delete=models.CASCADE,
                                 verbose_name='settings')

    def __str__(self):
        return f'{self.title}: {self.message}'

    class Meta:
        verbose_name = 'content'
        verbose_name_plural = 'contents'


class Trial(models.Model):
    """A class model for newsletter trial"""
    date = models.DateTimeField(auto_now_add=True, verbose_name='date')
    status = models.CharField(max_length=100, default='created',
                              verbose_name='status')
    response = models.CharField(max_length=250, verbose_name='response',
                                **NULLABLE)
    # Foreign key
    content = models.ForeignKey(Content, on_delete=models.CASCADE,
                                verbose_name='content')
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               verbose_name='client')

    def __str__(self):
        return f'{self.date}: {self.status}'

    class Meta:
        verbose_name = 'trial'
        verbose_name_plural = 'trials'
        ordering = ['date']
