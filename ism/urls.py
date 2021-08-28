from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('main.urls')),
    path('certificate/', include('certificate.urls')),
    path("login/", LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path("password-reset/",
        PasswordResetView.as_view(template_name='password_reset.html'),
        name="password_reset"),

    path("password-reset/done/",
        PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name="password_reset_confirm"),

    path("password-reset-complete/",
        PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)