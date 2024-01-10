from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from course.models import Course, Lesson, Payments, Subscription
from course.paginators import ListPagination
from course.permissions import IsStaff, IsOwner, IsSuperuser
from course.serializers import LessonSerializer, PaymentsSerializer, LessonListSerializer, \
    LessonDetailSerializer, CourseListSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Viewset for course"""
    serializer_class = CourseListSerializer
    queryset = Course.objects.all().order_by('-id')
    permission_classes = [IsStaff | IsOwner | IsSuperuser]
    pagination_class = ListPagination


class LessonCreateAPIView(generics.CreateAPIView):
    """Lesson create endpoint"""
    serializer_class = LessonSerializer
    permission_classes = [~IsStaff]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all().order_by('-id')
    permission_classes = [IsStaff | IsOwner | IsSuperuser]
    pagination_class = ListPagination


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
    filterset_fields = ('paid_lesson', 'paid_course', 'payment_method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer, **kwargs):
        new_subscription = serializer.save()

        new_subscription.user = self.request.user
        new_subscription.course = Course.objects.get(id=self.kwargs['pk'])
        new_subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):

    queryset = Subscription.objects.all()  # список уроков

    def perform_destroy(self, instance, **kwargs):
        user = self.request.user
        subscription = Subscription.objects.get(course_id=self.kwargs['pk'], user=user)
        subscription.delete()
