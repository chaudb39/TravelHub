from django.contrib import admin
from django.utils.html import format_html
from django import forms

from .models import Post


# =========================
# FORM ADMIN POST
# =========================

class PostAdminForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'

        widgets = {
            # Ô tóm tắt bài viết
            'summary': forms.Textarea(
                attrs={
                    'rows': 5,
                    'class': 'admin-textarea admin-textarea-medium',
                }
            ),
        }


# =========================
# POST ADMIN
# =========================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):


    form = PostAdminForm

    # Các cột hiển thị
    list_display = (
        'preview',
        'title',
        'author',
        'is_published',
        'created_at',
    )

    # Các trường cho phép tìm kiếm
    search_fields = (
        'title',
        'summary',
        'author',
    )

    # Bộ lọc bên phải 
    list_filter = (
        'is_published',
        'created_at',
    )

    # Sắp xếp bài viết mới nhất lên trên
    ordering = (
        '-created_at',
    )

    # Số bài viết mỗi trang
    list_per_page = 10

    # Chia form thành từng nhóm rõ ràng
    fieldsets = (
        (
            'Thông tin bài viết',
            {
                'fields': (
                    'title',
                    'thumbnail',
                    'preview',
                    'summary',
                    'content',
                )
            }
        ),

        (
            'Cài đặt',
            {
                'fields': (
                    'author',
                    'is_published',
                )
            }
        ),
    )

    # preview chỉ để xem, không cho nhập tay
    readonly_fields = (
        'preview',
    )

    # =========================
    # PREVIEW ẢNH
    # =========================

    def preview(self, obj):

        if obj and obj.thumbnail:
            return format_html(
                '''
                <div class="admin-image-preview-box">
                    <img
                        src="{}"
                        class="admin-image-preview"
                    >
                </div>
                ''',
                obj.thumbnail.url
            )

        return format_html(
            '''
            <div class="admin-image-preview-empty">
                Chưa có ảnh
            </div>
            '''
        )

    preview.short_description = 'Xem trước'