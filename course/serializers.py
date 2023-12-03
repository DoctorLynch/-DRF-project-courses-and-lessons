from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from course.models import Course, Lesson, Payments
from course.validators import LinkToVideoValidator


class CourseListSerializer(serializers.ModelSerializer):
    num_of_lesson = SerializerMethodField()
    lesson_this_course = SerializerMethodField()

    def get_num_of_lesson(self, lesson):
        return Lesson.objects.filter(course=lesson).count()

    def get_lesson_this_course(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

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
