from django.core.exceptions import ValidationError


def validate_uz_phone_number(phone_number: str):
    phone_number = phone_number.replace(' ', '')
    if len(phone_number) != 13:
        raise ValidationError("Telefon raqamining uzuznligi 13 bo`lishi kerak!")
    if not phone_number.startswith('+998'):
        raise ValidationError("Telefon raqami +998 bilan boshlanishi kerak!")
    if not phone_number[1:].isdigit():
        raise ValidationError("Telefon raqami faqat butun sonlar(0,1,2,3,4,5,6,7,8,9) iborat bo`lishi kerak!")
