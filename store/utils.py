import qrcode
import json
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.utils.translation import get_language
from functools import wraps


def test_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            language = request.path[1:3]  # Get current language (e.g., 'uz', 'ru', 'en')
            current_path = request.get_full_path()  # Get current path with query parameters
            login_url = f'/{language}/auth/login/?next={current_path}'
            return redirect(login_url)
        return view_func(request, *args, **kwargs)

    return wrapper


def generate_qr_code(order):
    qr_data = {
        "order_id": order.id,
        "uuid": str(order.uuid)
    }

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    order.qr_code.save(f"order_{order.id}_qr.png", ContentFile(buffer.read()), save=False)
    buffer.close()
    order.save()
