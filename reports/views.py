# =========================
# 1. Thư viện chuẩn của Python
# =========================
import csv
import json
import os
import platform


# =========================
# 2. Thư viện bên ngoài
# =========================
import pdfkit


# =========================
# 3. Các thành phần của Django
# =========================
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string


# =========================
# 4. Model trong project
# =========================
from destinations.models import Destination
from bookings.models import Booking
from reviews.models import Review

#cache
from django.core.cache import cache


# =========================
# DASHBOARD BÁO CÁO
# =========================
@login_required
def dashboard(request):
    """
    Hiển thị trang dashboard báo cáo.

    Chức năng chính:
    - Lọc booking theo tháng/năm.
    - Hiển thị KPI tổng quan.
    - Tạo dữ liệu cho biểu đồ cột, biểu đồ đường, biểu đồ tròn.
    - Hiển thị bảng chi tiết booking.
    """

    # =========================
    # 1. Lấy tháng/năm từ form lọc
    # =========================
    month = request.GET.get('month')
    year = request.GET.get('year')

    # =========================
    # 2. Lấy danh sách booking
    # =========================
    # select_related giúp lấy kèm user và destination trong cùng truy vấn,
    # tránh truy vấn database nhiều lần khi hiển thị bảng.
    bookings = Booking.objects.select_related(
        'user',
        'destination'
    ).order_by('-id')

    # =========================
    # 3. Lọc booking theo tháng nếu người dùng chọn
    # =========================
    if month:
        bookings = bookings.filter(created_at__month=month)

    # =========================
    # 4. Lọc booking theo năm nếu người dùng chọn
    # =========================
    if year:
        bookings = bookings.filter(created_at__year=year)

    # =========================
    # 5. Tính KPI tổng quan
    # =========================
    '''
    tong_destination = Destination.objects.count()
    tong_booking = bookings.count()
    tong_review = Review.objects.count()

    # Tính tổng doanh thu từ các booking sau khi lọc.
    # Nếu không có dữ liệu thì trả về 0.
    tong_doanh_thu = bookings.aggregate(
        total=Sum('total_price')
    )['total'] or 0
    '''

    # =========================
    # 5. CACHE KPI DASHBOARD
    # =========================

    # NEW
    cache_key = f'kpi_{month}_{year}'

    # NEW
    kpi_data = cache.get(cache_key)

    # NEW
    if kpi_data is None:

        print('QUERY DATABASE KPI')

        tong_destination = Destination.objects.count()

        tong_booking = bookings.count()

        tong_review = Review.objects.count()

        tong_doanh_thu = bookings.aggregate(
            total=Sum('total_price')
        )['total'] or 0

        kpi_data = {
            'tong_destination': tong_destination,
            'tong_booking': tong_booking,
            'tong_review': tong_review,
            'tong_doanh_thu': tong_doanh_thu,
        }

        # cache 2 phút
        cache.set(
            cache_key,
            kpi_data,
            60 * 2
        )

    else:

        print('LẤY KPI TỪ CACHE')

        tong_destination = kpi_data['tong_destination']

        tong_booking = kpi_data['tong_booking']

        tong_review = kpi_data['tong_review']

        tong_doanh_thu = kpi_data['tong_doanh_thu']

    # =========================
    # 6. Biểu đồ cột:
    # Top 10 địa điểm được đặt nhiều nhất
    # =========================
    top_destinations = (
        bookings
        .values('destination__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )

    # Nhãn trục X: tên địa điểm
    destination_labels = [
        item['destination__name'] for item in top_destinations
    ]

    # Dữ liệu trục Y: số lượt đặt
    destination_data = [
        item['total'] for item in top_destinations
    ]

    # =========================
    # 7. Biểu đồ đường:
    # Doanh thu theo tháng
    # =========================
    revenue_by_month = (
        bookings
        .annotate(month_value=TruncMonth('created_at'))
        .values('month_value')
        .annotate(total=Sum('total_price'))
        .order_by('month_value')
    )

    month_labels = []
    revenue_data = []

    # Chuyển dữ liệu doanh thu theo tháng thành 2 list:
    # month_labels: tên tháng
    # revenue_data: doanh thu tương ứng
    for item in revenue_by_month:
        if item['month_value']:
            month_labels.append(item['month_value'].strftime('%m/%Y'))
            revenue_data.append(float(item['total'] or 0))

    # =========================
    # 8. Biểu đồ tròn:
    # Tỷ lệ review theo số sao
    # =========================
    rating_stats = (
        Review.objects
        .values('rating')
        .annotate(total=Count('id'))
        .order_by('rating')
    )

    # Nhãn biểu đồ: 1 sao, 2 sao, 3 sao...
    rating_labels = [
        f"{item['rating']} sao" for item in rating_stats
    ]

    # Dữ liệu biểu đồ: số lượng review ở mỗi mức sao
    rating_data = [
        item['total'] for item in rating_stats
    ]

    # =========================
    # 9. Gom dữ liệu gửi sang template
    # =========================
    context = {
        # Dữ liệu bộ lọc
        'selected_month': month,
        'selected_year': year,

        # Dữ liệu KPI
        'tong_destination': tong_destination,
        'tong_booking': tong_booking,
        'tong_review': tong_review,
        'tong_doanh_thu': tong_doanh_thu,

        # Dữ liệu biểu đồ cột
        'destination_labels': json.dumps(destination_labels, ensure_ascii=False),
        'destination_data': json.dumps(destination_data),

        # Dữ liệu biểu đồ đường
        'month_labels': json.dumps(month_labels, ensure_ascii=False),
        'revenue_data': json.dumps(revenue_data),

        # Dữ liệu biểu đồ tròn
        'rating_labels': json.dumps(rating_labels, ensure_ascii=False),
        'rating_data': json.dumps(rating_data),

        # Dữ liệu bảng chi tiết booking
        'bookings': bookings,
    }

    # =========================
    # 10. Render giao diện dashboard
    # =========================
    return render(request, 'reports/dashboard.html', context)


# =========================
# XUẤT BÁO CÁO BOOKING RA CSV
# =========================
@login_required
def export_booking_csv(request):
    """
    Xuất danh sách booking ra file CSV.

    Chức năng:
    - Lấy dữ liệu booking.
    - Áp dụng bộ lọc tháng/năm giống dashboard.
    - Ghi dữ liệu ra file CSV.
    - Trả file CSV về cho người dùng tải xuống.
    """

    # =========================
    # 1. Lấy tháng/năm từ URL
    # =========================
    month = request.GET.get('month')
    year = request.GET.get('year')

    # =========================
    # 2. Lấy danh sách booking
    # =========================
    bookings = Booking.objects.select_related(
        'user',
        'destination'
    ).order_by('-id')

    # =========================
    # 3. Lọc dữ liệu theo tháng/năm
    # =========================
    if month:
        bookings = bookings.filter(created_at__month=month)

    if year:
        bookings = bookings.filter(created_at__year=year)

    # =========================
    # 4. Tạo response dạng file CSV
    # =========================
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="booking_report.csv"'

    # Ghi BOM để Excel đọc tiếng Việt không bị lỗi font
    response.write('\ufeff')

    # =========================
    # 5. Tạo writer để ghi dữ liệu CSV
    # =========================
    writer = csv.writer(response)

    # Ghi dòng tiêu đề
    writer.writerow([
        'ID',
        'Khách hàng',
        'Địa điểm',
        'Ngày đi',
        'Số người',
        'Tổng tiền',
        'Ngày tạo'
    ])

    # =========================
    # 6. Ghi từng booking vào file CSV
    # =========================
    for booking in bookings:
        writer.writerow([
            booking.id,
            booking.user.username,
            booking.destination.name,
            booking.start_date,
            booking.people,
            booking.total_price,
            booking.created_at.strftime('%d/%m/%Y %H:%M')
        ])

    # =========================
    # 7. Trả file CSV về trình duyệt
    # =========================
    return response


# =========================
# XUẤT HÓA ĐƠN BOOKING RA PDF
# =========================
@login_required
def export_booking_pdf(request, booking_id):
    """
    Xuất hóa đơn PDF cho một booking cụ thể.

    Chức năng:
    - Lấy booking theo ID.
    - Kiểm tra booking có thuộc người dùng hiện tại không.
    - Render template hóa đơn HTML.
    - Chuyển HTML thành file PDF.
    - Lưu PDF vào thư mục media/reports.
    - Chuyển hướng người dùng sang file PDF vừa tạo.
    """

    # =========================
    # 1. Lấy booking cần xuất PDF
    # =========================
    # user=request.user giúp đảm bảo người dùng chỉ xuất được hóa đơn của chính họ.
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    # =========================
    # 2. Render template hóa đơn thành chuỗi HTML
    # =========================
    html_string = render_to_string(
        'reports/booking_invoice.html',
        {
            'booking': booking
        }
    )

    # =========================
    # 3. Cấu hình đường dẫn wkhtmltopdf theo hệ điều hành
    # =========================
    if platform.system() == 'Windows':
        config = pdfkit.configuration(
            wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        )
    elif platform.system() == 'Linux':
        config = pdfkit.configuration(
            wkhtmltopdf='/usr/bin/wkhtmltopdf'
        )
    else:
        config = pdfkit.configuration(
            wkhtmltopdf='/usr/local/bin/wkhtmltopdf'
        )

    # =========================
    # 4. Tạo thư mục media/reports nếu chưa có
    # =========================
    folder_report = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(folder_report, exist_ok=True)

    # =========================
    # 5. Tạo tên file và đường dẫn lưu PDF
    # =========================
    file_name = f'booking_{booking.id}.pdf'
    path_report = os.path.join(folder_report, file_name)

    # =========================
    # 6. Chuyển HTML thành PDF
    # =========================
    pdfkit.from_string(
        html_string,
        path_report,
        configuration=config
    )

    # =========================
    # 7. Chuyển hướng người dùng sang file PDF
    # =========================
    return redirect(settings.MEDIA_URL + 'reports/' + file_name)