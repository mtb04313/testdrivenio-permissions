from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('func/', views.post_list_view, name='list_by_viewfn'),
    #path('<int:pk>/', views.snippet_detail, name='snippet_detail'),

    path('class/', views.PostListView.as_view(), name='list_by_viewclass'),

    path('class/<int:pk>/', views.PostDetailsView.as_view(), name='details_by_viewclass'),
    path('details/<int:pk>/', views.PostDetailsView.as_view(), name='details_by_viewclass'),


    #path('users/', views.UserList.as_view(), name='user_list'),
    #path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    
]
