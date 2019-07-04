from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import redirect
from pure_pagination import Paginator, PageNotAnInteger

from Mydemy.settings import PAGINATION_SETTINGS
from .models import City, CourseOrg
from .forms import UserRequestForm


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

        return render(request, 'org-list.html', {
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
        if org:
            return render(request, 'org_detail_overview.html', {
                'org': org
            })
        else:
            return redirect('org:list')


class OrgInfoView(View):

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        if org:
            return render(request, 'org_detail_org.html', {
                'org': org
            })
        else:
            return redirect('org:list')


class OrgInstructorView(View):

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        if org:
            return render(request, 'org_detail_instructor.html', {
                'org': org
            })
        else:
            return redirect('org:list')



class OrgCourseView(View):

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        if org:
            return render(request, 'org_detail_course.html', {
                'org': org
            })
        else:
            return redirect('org:list')
