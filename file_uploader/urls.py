from django.conf.urls import url
 
from . import views
 
urlpatterns = [
    url(r'^$', views.fileUploaderView),
]

# from django.conf.urls import url, include
# from django.contrib import admin
 
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^file-upload/', include('file_uploader.urls'))
# ]