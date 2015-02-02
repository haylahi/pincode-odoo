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

from openerp import fields,models,api
import os
import random
import string
from datetime import datetime


class pincode_type(models.Model):
    _name='pincode.type'

    name=fields.Char(required=True,string='Description',translate=True)
    length=fields.Integer(required=True,string='Pin code length')
    time_validity=fields.Float(required=True,string='Validity time',help="Validity time of pincode\nFormat : HH:MM")
    format=fields.Selection( [('numeric', "Numeric"),
                              ('alpha', "Alpha"),
                              ('numeric&alpha', "Numeric & Alpha")]
                            ,required=True,default="numeric&alpha")
    action=fields.Many2one('base.action.rule','Action server',required=True)

class pincode_log(models.Model):
    _name='pincode.log'

    date=fields.Datetime(string='Date and time')
    pincode=fields.Char(string='Pin code')
    ipuser=fields.Char(string="Ip user")
    states=fields.Selection([('not_used', "Not used"),
                              ('used', "In used"),
                              ('wrong', "Wrong"),
                              ('outdated', " Used but outdated")]
                            ,required=True,default="not_used")
    user_id=fields.Many2one('res.users',string='Users')
    _order='date desc'


class pincode_config(models.Model):
    _name='pincode.config'
    name=fields.Char(required=True,string='Description',translate=True)
    type_id=fields.Many2one('pincode.type',string='Configuration')
    sequence=fields.Integer(string='Sequence')
    active=fields.Boolean(default=False)

    def generate_pins(self,length,format):

        if format=='numeric' :
            chars=string.digits
        if format=='alpha' :
            chars=string.ascii_uppercase + string.ascii_lowercase
        if format=='numeric&alpha' :
            chars=string.ascii_uppercase + string.ascii_lowercase + string.digits

        return ''.join(random.choice(chars) for x in range(0,length))
