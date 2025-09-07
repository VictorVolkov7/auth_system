from django.urls import path
from apps.users.views import (UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView,
                              AccessRoleRuleDetailView, AccessRoleRuleListView)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    path('access-rules/', AccessRoleRuleListView.as_view(), name='access_rule_list'),
    path('access-rules/<int:pk>/', AccessRoleRuleDetailView.as_view(), name='access_rule_detail'),
]
