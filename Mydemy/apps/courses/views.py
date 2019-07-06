from django.shortcuts import render
from django.views.generic import View

from .models import Course


class CourseListView(View):

    def get(self, request):
        order_by = request.GET.get('order_by', '')
        courses = Course.objects.all()
        top_courses = courses.order_by('-click_count')[:3]
        if order_by:
            if order_by == 'fav':
                courses = courses.order_by('-fav_count')
            elif order_by == 'stu':
                courses = courses.order_by('-student_count')
        else:
            courses = courses.order_by('-create_time')

        return render(request, 'course_list.html', {
            'courses': courses,
            'top_courses': top_courses,
            'current_order_by': order_by,
        })