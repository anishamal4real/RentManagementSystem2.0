from django.urls import path, include
from . import views
from .views import  LandlordViewSet, TenantViewSet, RentViewSet, CustomUserViewSet, edit_landlord
from rest_framework.routers import DefaultRouter

router= DefaultRouter()
router.register('customuser',CustomUserViewSet, basename="customuser")
router.register('tenant', TenantViewSet, basename="tenant")
router.register('landlord', LandlordViewSet, basename="landlord")
router.register('rent',RentViewSet, basename="rent")
router.register('editlandlord',LandlordViewSet, basename="edit_landlord")
router.register('edittenant',TenantViewSet, basename="edit_tenant")




urlpatterns = [path('', views.home, name="home"),
               path('rent/<str:pk>/', views.rent, name="rent"),
               path('register/', views.registerPage, name="register"),
               path('login/', views.loginPage, name="login"),
               path('logout/', views.logoutUser, name="logout"),
               path('viewset/', include(router.urls)),
               path('viewset/<int:pk>/', include(router.urls)),
               path('profile/', views.view_profile, name='view_profile'),
               path('profile/edit/', views.edit_profile, name='edit_profile'),
               path('tenant/',views.view_tenant, name='view_tenant'),
               path('tenant/edit/',views.edit_tenant, name='edit_tenant'),
               path('landlord/', views.view_landlord, name='view_landlord'),
               path('landlord/edit/', views.edit_landlord, name='edit_landlord'),
              
]              
               
              
              