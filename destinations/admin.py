from django.contrib import admin
from django.utils.html import format_html
from django import forms

from .models import Destination


# =========================
# FORM ADMIN DESTINATION
# =========================

class DestinationAdminForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = '__all__'

        widgets = {
            # Ô mô tả ngắn
            'short_description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'admin-textarea',
                }
            ),

            # Ô mô tả chi tiết
            'description': forms.Textarea(
                attrs={
                    'rows': 8,
                    'class': 'admin-textarea admin-textarea-large',
                }
            ),
        }


# =========================
# DESTINATION ADMIN
# =========================

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):

    form = DestinationAdminForm

    # Các cột hiển thị ở trang danh sách địa điểm
    list_display = (
        'preview',
        'name',
        'city',
        'price_vnd',
        'is_featured',
        'created_at',
    )

    # Click vào tên để mở trang chỉnh sửa
    list_display_links = (
        'name',
    )

    # Bộ lọc bên phải trong admin
    list_filter = (
        'city',
        'is_featured',
        'created_at',
    )

    # Các trường cho phép tìm kiếm
    search_fields = (
        'name',
        'city',
        'short_description',
        'description',
    )

    # Sắp xếp địa điểm mới nhất lên trên
    ordering = (
        '-created_at',
    )

    # Số địa điểm mỗi trang
    list_per_page = 10

    # Chia form thành từng nhóm
    fieldsets = (
        (
            'Thông tin địa điểm',
            {
                'fields': (
                    'name',
                    'city',
                    'image',
                    'preview',
                    'price',
                    'is_featured',
                )
            }
        ),

        (
            'Mô tả',
            {
                'fields': (
                    'short_description',
                    'description',
                )
            }
        ),

        (
            'Thông tin hệ thống',
            {
                'fields': (
                    'created_at',
                )
            }
        ),
    )

    # Các field chỉ xem, không cho nhập tay
    readonly_fields = (
        'preview',
        'created_at',
    )

    # =========================
    # PREVIEW ẢNH
    # =========================

    def preview(self, obj):

        if obj and obj.image:
            return format_html(
                '''
                <div class="admin-image-preview-box">
                    <img
                        src="{}"
                        class="admin-image-preview"
                    >
                </div>
                ''',
                obj.image.url
            )

        return format_html(
            '''
            <div class="admin-image-preview-empty">
                Chưa có ảnh
            </div>
            '''
        )

    preview.short_description = 'Xem trước'

    # =========================
    # FORMAT GIÁ TIỀN
    # =========================

    def price_vnd(self, obj):

        return f'{obj.price:,} VNĐ'

    price_vnd.short_description = 'Giá'