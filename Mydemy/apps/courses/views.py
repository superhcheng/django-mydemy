from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from Mydemy.settings import PAGINATION_SETTINGS
from .models import Course, Lesson, Resource
from operations.models import UserFavorite


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

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, PAGINATION_SETTINGS['PAGE_RANGE_DISPLAYED'], request=request)
        ret_courses = p.page(page)

        return render(request, 'course_list.html', {
            'courses': ret_courses,
            'top_courses': top_courses,
            'current_order_by': order_by,
        })


class CourseOverviewView(View):

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        relate_courses = Course.objects.filter(category=course.category).exclude(id=int(course_id))[:3]
        course.click_count += 1
        course.save()

        fav_course = False
        fav_org = False

        if request.user.is_authenticated():
            user_favs = UserFavorite.objects.filter(user=request.user)
            if user_favs:
                if user_favs.filter(fav_id=course.id, fav_type=2):
                    fav_course = True
                if user_favs.filter(fav_id=course.org.id, fav_type=3):
                    fav_org = True

        return render(request, 'course_detail_overview.html', {
            'course': course,
            'relate_courses': relate_courses,
            'fav_course': fav_course,
            'fav_org': fav_org,
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        pass


class CourseVideoListView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        lessons = Lesson.objects.filter(course=course)
        res_list = Resource.objects.filter(course=course)

        return render(request, 'course_detail_videolist.html', {
            'lessons': lessons,
            'course': course,
            'instructor': course.instructor,
            'res_list': res_list,
        })


