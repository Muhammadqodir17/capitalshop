from django.core.exceptions import ValidationError
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def validate_qr_code(request):
    from store.models import Order
    qr_data = request.POST.get('qr_data')
    decoded_data = json.loads(qr_data)

    order_id = decoded_data.get('order_id')
    uuid = decoded_data.get('uuid')
    order = get_object_or_404(Order, id=order_id, uuid=uuid)

    if order:
        return JsonResponse({
            'status': 'success',
            'order_id': order.id,
            'token': order.uuid,
            'message': 'QR code is valid.'
        })
    else:
        return JsonResponse({
            'status': 'failure',
            'message': 'Invalid QR code.'
        })


def validate_uz_phone_number(phone_number: str):
    phone_number = phone_number.replace(' ', '')
    if len(phone_number) != 13:
        raise ValidationError("Telefon raqamining uzuznligi 13 bo`lishi kerak!")
    if not phone_number.startswith('+998'):
        raise ValidationError("Telefon raqami +998 bilan boshlanishi kerak!")
    if not phone_number[1:].isdigit():
        raise ValidationError("Telefon raqami faqat butun sonlar(0,1,2,3,4,5,6,7,8,9) iborat bo`lishi kerak!")
