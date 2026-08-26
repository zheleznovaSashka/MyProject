from django.core.exceptions import ValidationError

def validate_strong_password(value):
    # Если хочешь ВРЕМЕННО отключить — просто закомментируй проверку
    # if len(value) < 8:
    #     raise ValidationError('Пароль должен быть длиннее 8 символов')
    pass  # пока ничего не делает