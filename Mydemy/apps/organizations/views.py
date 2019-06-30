from django.shortcuts import render
from django.views.generic import View


from .models import City, CourseOrg


class OrgView(View):
    def get(self, request):
        all_cities = City.objects.all()
        all_orgs = CourseOrg.objects.all()
        org_count = all_orgs.count()
        return render(request, 'org-list.html', {
            'all_cities': all_cities,
            'all_orgs': all_orgs,
            'org_count': org_count
        })
