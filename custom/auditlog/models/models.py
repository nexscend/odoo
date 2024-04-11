# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, models


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    # ------------------------------------------------------------
    # FIELDS HELPERS
    # ------------------------------------------------------------

    @classmethod
    def _patch_method(cls, name, method):
        """ Monkey-patch a method for all instances of this model. This replaces
            the method called ``name`` by ``method`` in the given class.
            The original method is then accessible via ``method.origin``, and it
            can be restored with :meth:`~._revert_method`.

            Example::

                def do_write(self, values):
                    # do stuff, and call the original method
                    return do_write.origin(self, values)

                # patch method write of model
                model._patch_method('write', do_write)

                # this will call do_write
                records = model.search([...])
                records.write(...)

                # restore the original method
                model._revert_method('write')
        """
        origin = getattr(cls, name)
        method.origin = origin
        # propagate decorators from origin to method, and apply api decorator
        wrapped = api.propagate(origin, method)
        wrapped.origin = origin
        setattr(cls, name, wrapped)

    @classmethod
    def _revert_method(cls, name):
        """ Revert the original method called ``name`` in the given class.
            See :meth:`~._patch_method`.
        """
        method = getattr(cls, name)
        setattr(cls, name, method.origin)