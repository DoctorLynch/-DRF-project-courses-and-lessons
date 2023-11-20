# Generated by Django 4.2.7 on 2023-11-20 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('image_preview', models.ImageField(blank=True, null=True, upload_to='image_lesson')),
                ('video', models.URLField()),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
        migrations.AlterField(
            model_name='course',
            name='image_preview',
            field=models.ImageField(blank=True, null=True, upload_to='image_course'),
        ),
    ]
