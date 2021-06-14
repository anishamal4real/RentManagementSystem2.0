from django.urls import path, include
from . import views
from .views import  LandlordViewSet, TenantViewSet, RentViewSet
from rest_framework.routers import DefaultRouter

router= DefaultRouter()
router.register('tenant', TenantViewSet, basename="tenant")
router.register('landlord', LandlordViewSet, basename="landlord")
router.register('rent',RentViewSet, basename="rent")

urlpatterns = [path('', views.home, name="home"),
               path('tenant/<str:pk_test>/', views.tenant, name="tenant"),
               path('landlord/<str:pk>/', views.landlord,  name="landlord"),
               path('rent/<str:pk>/', views.rent, name="rent"),
               path('register/', views.registerPage, name="register"),
               path('login/', views.loginPage, name="login"),
               path('logout/', views.logoutUser, name="logout"),
               path('viewset/', include(router.urls)),
               path('viewset/<int:pk>/', include(router.urls)),
               path('profile/', views.view_profile, name='view_profile'),
               path('profile/edit/', views.edit_profile, name='edit_profile'),
]              
               
              
              