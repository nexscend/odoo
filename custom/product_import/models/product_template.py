# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Mohammed Shahil MP @cybrosys(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
import base64
import certifi
import requests
import urllib3
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import os


class ProductTemplate(models.Model):
    """Inherit the model to add fields and function"""
    _inherit = 'product.template'

    image_url = fields.Char(string='Image URL', help='Image URL or Path')
    image_added = fields.Binary("Image (1920x1920)",
                                compute='_compute_image_added', store=True)

    @api.depends('image_url')
    def _compute_image_added(self):
        """ Function to load an image from URL or local file path """
        image = False
        for rec in self:
            if rec.image_url:
                cwd = os.getcwd()
                if rec.image_url.startswith(('http://', 'https://')):
                    # Load image from URL
                    try:
                        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                                   ca_certs=certifi.where())

                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                        }

                        r = requests.get(rec.image_url, headers=headers)
                        c = r.content
                        # image_response = http.request('GET', self.image_url)
                        # print("__image_response__http",image_response.data)
                        image = base64.b64encode(c)
                    except Exception as e:
                        # Handle URL loading errors
                        raise UserError(
                            _(f"Error loading image from URL: {str(e)}"))
                else:
                    try:
                        folder_path = os.path.join(os.getcwd(), 'custom/product_import/static/img/', rec.image_url)
                        with open(folder_path, 'rb') as image_file:
                            image = base64.b64encode(image_file.read())
                    except Exception as e:
                        # Handle local file loading errors
                        raise UserError(
                            _(f"Error loading image from local path: {str(e)}"))
            image_added = image
            if image_added:
                rec.image_1920 = image_added
