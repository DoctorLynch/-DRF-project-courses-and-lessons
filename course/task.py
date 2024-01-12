from celery import shared_task
from django.core.mail import send_mail

from config import settings
from course.models import Course, Subscription


@shared_task
def send_email_course_update(course_pk):
    subscribers = Subscription.objects.filter(course=course_pk, status=True)
    course = Course.objects.get(pk=course_pk)
    for subscriber in subscribers:
        send_mail(
            subject=f'Обновление курса {course}',
            message='В курс добавили новые материалы',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.user.email],
            fail_silently=False
        )