from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from course.models import Course, Lesson, Payments
from course.permissions import IsStaff, IsOwner, IsSuperuser
from course.serializers import LessonSerializer, PaymentsSerializer, LessonListSerializer, \
    LessonDetailSerializer, CourseListSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()
    permission_classes = [IsStaff | IsOwner | IsSuperuser]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsStaff]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsOwner | IsSuperuser]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonDetailSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsOwner | IsSuperuser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsOwner | IsSuperuser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsSuperuser]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_lesson', 'paid_course', 'payment_method_choices')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]
