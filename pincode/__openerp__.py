# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) Monoyer Fabian (fabian.monoyer@gmail.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Pincode',
    'version': '1.0',
    'depends': ['base','web','mail','email_template','base_action_rule' ],
    'author': 'odoo-labs.',
    'description': """

pincode
==============

...
...
...

    """,
    'category': 'security',
    'sequence': 32,
    'data': [
        'security/ir.model.access.csv',
        'views/user_view.xml',
        'views/pincode_view.xml',
        'views/web_login_view.xml',
     ],
    'auto_install': False,
    'installable': True,
    'application': False,
}

