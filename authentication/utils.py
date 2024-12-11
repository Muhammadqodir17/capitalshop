from django.core.exceptions import ValidationError


def phone_validation(phone_number):
    if len(phone_number) != 13:
        raise ValidationError('phone_number length must be 13.')
    if phone_number[:4] != '+998':
        raise ValidationError('phone_number must be uzbek and start with "+998".')
    if not phone_number[1:13].isdigit():
        raise ValidationError('phone_number must be number like [1, 2, 3, 4, 5, 6, 7, 8, 9, 0].')
