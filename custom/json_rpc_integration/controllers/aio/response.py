def error_response(status, odoo_error):
    return {
        "isFullFilled": False,
        "statusCode": status,
        "message": odoo_error
    }


def success_list_response(status: int = 200, **data):
    return {
        "isFullFilled": True,
        "statusCode": status,
        "count": len(data),
        "data": data
    }


def success_response(status: int = 200, **data):
    """
    :param status:
    :param data:
    :return: dict
    """
    return {
        "isFullFilled": True,
        "statusCode": status,
        "data": data
    }


def success_message_response(status: int, message):
    """
    :param status:
    :param data:
    :return: dict
    """
    return {
        "isFullFilled": True,
        "statusCode": status,
        "message": message
    }
