import logging
import functools
from ..model_definitions import models
from .response import error_response

_logger = logging.getLogger(__name__)


def check_register_models(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print("______args",args)
        print("______kwargs",kwargs)
        print("______models",models)
        if kwargs['model'] not in models:
            _logger.info("Model fields not defined...")
            return error_response(status=404, odoo_error="Model objects not found in Odoo!")
        # The code, following the decorator
        kwargs["model_definitions"] = models[kwargs['models']]
        print("_____kwargs",kwargs)
        return func(self, *args, **kwargs)

    return wrapper
