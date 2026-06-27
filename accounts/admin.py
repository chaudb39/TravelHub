from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django import forms

from .models import UserProfile


# =========================
# FORM PROFILE
# =========================

class UserProfileInlineForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = '__all__'

        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'class': 'admin-input admin-input-short',
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'rows': 2,
                    'class': 'admin-textarea',
                }
            ),

            'bio': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'admin-textarea',
                }
            ),
        }


# =========================
# INLINE USER PROFILE
# =========================

class UserProfileInline(admin.StackedInline):

    model = UserProfile
    form = UserProfileInlineForm

    extra = 0
    can_delete = False

    verbose_name = 'Hồ sơ'
    verbose_name_plural = 'Hồ sơ'

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'avatar_preview',
                    'avatar',
                    'phone',
                    'address',
                    'bio',
                )
            }
        ),
    )

    readonly_fields = (
        'avatar_preview',
    )

    # Hiển thị ảnh đại diện xem trước
    def avatar_preview(self, obj):

        if obj and obj.avatar:
            return format_html(
                '''
                <div class="admin-image-preview-box">
                    <img
                        src="{}"
                        class="admin-image-preview"
                    >
                </div>
                ''',
                obj.avatar.url
            )

        return format_html(
            '''
            <div class="admin-image-preview-empty">
                Chưa có ảnh
            </div>
            '''
        )

    avatar_preview.short_description = 'Ảnh đại diện'


# =========================
# USER ADMIN
# =========================

class CustomUserAdmin(UserAdmin):

    inlines = [
        UserProfileInline,
    ]

    fieldsets = (
        (
            'Tài khoản',
            {
                'fields': (
                    'username',
                    'password',
                )
            }
        ),

        (
            'Thông tin cá nhân',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                )
            }
        ),

        (
            'Phân quyền',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),

        (
            'Thông tin hệ thống',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )


# =========================
# GỠ USER ADMIN MẶC ĐỊNH
# =========================

admin.site.unregister(User)


# =========================
# ĐĂNG KÝ USER ADMIN MỚI
# =========================

admin.site.register(
    User,
    CustomUserAdmin
)