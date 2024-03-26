from django.urls import path
from django.contrib.auth import views as auth_views

# from . import views
from mytabs.views import search_tabs ,signup, login, account, passwordReset, qualityoflife, securityQuestions, IndexView, DetailView,  detail
app_name = "mytabs"
urlpatterns = [
    path("", login, name="login"),
    path("signup", signup, name="signup"),
    path("account", account, name="account"),
    path("passwordReset/<str:name>", passwordReset, name="passwordReset"),
    path("passwordReset/", passwordReset, name="passwordReset"),
    path("qualityoflife", qualityoflife, name="qualityoflife"),
    path("securityQuestions", securityQuestions, name="securityQuestions"),
    path("list", IndexView.as_view(), name="index"),
    path("<int:pk>/", DetailView.as_view(), name="detail"),
    path("detail",detail, name="detail"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search', search_tabs, name='search'),
    path('<int:pk>/search', search_tabs, name='search')
]