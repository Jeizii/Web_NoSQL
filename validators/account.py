
from flask import request
from errors.not_found import NotFound
from errors.validation_error import ValidationError


def validate_account(func):
    def validate_account_wrapper(*args, **kwargs):
        request_body = request.get_json()
        if request_body:
            if 'username' in request_body:
                return func(*args, **kwargs)
            else:
                raise ValidationError(message='username is required')
        else:
            raise ValidationError(message='request body required')
    return validate_account_wrapper
        

