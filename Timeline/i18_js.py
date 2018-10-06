from django.contrib import admin
def js(request):
  return admin.site.i18n_javascript(request)