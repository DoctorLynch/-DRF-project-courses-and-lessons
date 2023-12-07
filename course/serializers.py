from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from course.models import Course, Lesson, Payments, Subscription
from course.validators import LinkToVideoValidator


class CourseListSerializer(serializers.ModelSerializer):
    num_of_lesson = SerializerMethodField(read_only=True)
    lesson_this_course = SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_num_of_lesson(self, lesson):
        return Lesson.objects.filter(course=lesson).count()

    def get_lesson_this_course(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    def get_is_subscribed(self, course):

        return Subscription.objects.filter(course=course, user=self.context['request'].user).exists()

    class Meta:
        model = Course
        fields = ('title', 'num_of_lesson', 'lesson_this_course',)


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkToVideoValidator('url')]


class LessonListSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('title', 'course',)


class LessonDetailSerializer(serializers.ModelSerializer):
    course = CourseDetailSerializer()

    class Meta:
        model = Lesson
        fields = ('title', 'course',)


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
