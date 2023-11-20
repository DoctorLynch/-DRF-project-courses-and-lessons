from django.db import models
from django.db.models import options

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image_preview = models.ImageField(upload_to='image_course', height_field=None, width_field=None, max_length=100,
                                      **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image_preview = models.ImageField(upload_to='image_lesson', height_field=None, width_field=None, max_length=100,
                                      **NULLABLE)
    video = models.URLField(max_length=200)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
