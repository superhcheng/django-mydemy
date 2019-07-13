from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import redirect
from pure_pagination import Paginator, PageNotAnInteger

from Mydemy.settings import PAGINATION_SETTINGS
from .models import City, CourseOrg, Instructor
from .forms import UserRequestForm
from operations.models import UserFavorite
from courses.models import Course


class OrgView(View):

    def get(self, request):
        all_cities = City.objects.all()
        all_orgs = CourseOrg.objects.all()
        top_orgs = all_orgs.order_by('-click_count')[:5]
        city_filter = request.GET.get('city_filter', '')
        provider_type = request.GET.get('provider_type', '')
        org_list_order_by = request.GET.get('org_list_order_by', '')

        if city_filter:
            all_orgs = all_orgs.filter(city=city_filter)

        if provider_type:
            all_orgs = all_orgs.filter(category=provider_type)

        if org_list_order_by:
            if org_list_order_by == 'student':
                all_orgs = all_orgs.order_by('-student_count')
            elif org_list_order_by == 'course':
                all_orgs = all_orgs.order_by('-course_count')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, PAGINATION_SETTINGS['PAGE_RANGE_DISPLAYED'], request=request)
        ret_orgs = p.page(page)

        return render(request, 'org_list.html', {
            'all_cities': all_cities,
            'all_orgs': ret_orgs,
            'top_orgs': top_orgs,
            'org_count': all_orgs.count(),
            'city_filter': city_filter,
            'provider_type': provider_type,
            'org_list_order_by': org_list_order_by,
        })


class UserRequestView(View):

    def post(self, request):
        user_request_form = UserRequestForm(request.POST)
        if user_request_form.is_valid():
            user_request_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            ret_err_msg = ''
            for field, errors in user_request_form.errors.items():
                ret_err_msg += 'Field: {} Error(s): {}'.format(field, ','.join(errors)) + '<br>'
            return HttpResponse('{"status": "fail", "err_msg": "Invalid Input"}', content_type='application/json')


class OrgOverviewView(View):

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        org_courses = org.course_set.all()[:3]
        org_instructors = org.instructor_set.all()[:1]
        if org:
            return render(request, 'org_detail_overview.html', {
                'org': org,
                'org_courses': org_courses,
                'org_instructors': org_instructors,
                'fav_btn_val': getFavState(request, fav_id=org_id),
            })
        else:
            return redirect('org:list')


class OrgInfoView(View):

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        if org:
            return render(request, 'org_detail_org.html', {
                'org': org,
                'fav_btn_val': getFavState(request, fav_id=org_id),
            })
        else:
            return redirect('org:list')


class OrgInstructorView(View):

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        org_instructors = org.instructor_set.all()
        if org:
            return render(request, 'org_detail_instructor.html', {
                'org': org,
                'org_instructors': org_instructors,
                'fav_btn_val': getFavState(request, fav_id=org_id),
            })
        else:
            return redirect('org:list')


class OrgCourseView(View):

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        org_courses = org.course_set.all()
        if org:
            return render(request, 'org_detail_course.html', {
                'org': org,
                'org_courses': org_courses,
                'fav_btn_val': getFavState(request, fav_id=org_id),
            })
        else:
            return redirect('org:list')


class OrgFavView(View):

    def post(self, request):
        if request.user.is_authenticated():
            fav_id = int(request.POST.get('fav_id', 0))
            fav_type = int(request.POST.get('fav_type', 0))

            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if user_fav:
                user_fav.delete()
                return HttpResponse('{"status": "success", "msg": "Favorite"}', content_type='application/json')
            else:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return HttpResponse('{"status": "success", "msg": "Un-Favorite"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "err_msg": "Login Required"}', content_type='application/json')


class InstructorListView(View):
    def get(self, request):
        instructors = Instructor.objects.all()
        order_by = request.GET.get('order_by', '')

        if order_by == 'fav':
            instructors = instructors.order_by('-click_count')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        if request.user.is_authenticated():
            for ins in instructors:
                if UserFavorite.objects.filter(user=request.user, fav_id=ins.id, fav_type=1):
                    ins.is_fav = True

        p = Paginator(instructors, PAGINATION_SETTINGS['PAGE_RANGE_DISPLAYED'], request=request)
        ret_instructors = p.page(page)

        return render(request, 'instructor_list.html', {
            'instructors': ret_instructors,
            'order_by': order_by,
            'top_instructors': instructors.order_by('-click_count')[:5],
        })


class InstructorInfoView(View):
    def get(self, request, ins_id):
        instructor = Instructor.objects.get(id=int(ins_id))
        top_instructors = Instructor.objects.all().order_by('-fav_count')[:5]
        courses = Course.objects.filter(instructor=instructor)
        ins_fav = False
        org_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(ins_id), fav_type=1):
                ins_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=instructor.org.id, fav_type=3):
                org_fav = True

        return render(request, 'instructor_info.html', {
            'instructor': instructor,
            'top_instructors': top_instructors,
            'courses': courses,
            'org': instructor.org,
            'ins_fav': ins_fav,
            'org_fav': org_fav,
        })


def getFavState(request, fav_id):
    if request.user.is_authenticated():
        if UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=3):
            return 'Un-favorite'
        else:
            return 'Favorite'
    else:
        return 'Favorite'
