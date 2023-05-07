from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        """
                Reformats ValidationError objects into simple strings with the same information.
                This is to homogenize the output to always have an "errors" property at the top level.
                {"errors": ["old_password (incorrect) : old_password does not match the existing password"]
                {"errors": ["non_field_errors (invalid) : Error message here"]
        }
        """
        if response is not None:
            data = response.data

            if isinstance(data, list):
                # This happens if you raise a ValidationError outside a def validate_* method.
                # The issue is that there isn't a "field" associated to the ErrorDetail list
                data = {"generic": data}

            response.data = {}
            errors = []
            for field, details in data.items():  # str, List[ErrorDetail]
                # ErrorDetail objects only have one property: "code", but will return a string of the error if printed.
                for detail in details:
                    errors.append(f"{field} ({detail.__dict__['code']}) : {detail}")

            response.data['errors'] = errors

    if response is not None:
        # Check if the response contains a 'detail' key
        if 'detail' in response.data:
            response.data = {'errors': response.data}

    return response
