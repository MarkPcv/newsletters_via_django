from django.db import models

from newsletters.models import NULLABLE


class Blog(models.Model):
    """A class model for blogs"""
    title = models.CharField(max_length=150, verbose_name='title')
    content = models.TextField(verbose_name='content')
    image = models.ImageField(upload_to='students/', verbose_name='image',
                               **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='views')
    date_published = models.DateTimeField(auto_now_add=True,
                                          verbose_name='date_published')

    def __str__(self):
        return (f'{self.title} published on '
               f'{self.date_published.strftime("%H:%M on %d/%m/%Y")}')

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
        ordering = ['date_published']