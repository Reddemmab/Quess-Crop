from django.urls import path
from .views import UserDataByName, load_cdr_data, load_user_data, UserDataByNameAndDate, UserDataByDateRange

urlpatterns = [
    path('load_cdr_data/', load_cdr_data, name='load_cdr_data'),
    path('load_user_data/', load_user_data, name='load_user_data'),
    path('user_data/<str:user_name>/', UserDataByName.as_view(), name='user_data_by_name'),
    path('user_data/<str:user_name>/<str:date>/', UserDataByNameAndDate.as_view(), name='user_data_by_name_and_date'),
    path('user_data/<str:user_name>/<str:from_date>/<str:to_date>/', UserDataByDateRange.as_view(), name='user_data_by_date_range'),
]
