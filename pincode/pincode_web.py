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

import openerp

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import db_monodb, ensure_db, set_cookie_and_redirect, login_and_redirect
from openerp.modules.registry import RegistryManager
from datetime import datetime

import string
import random
import simplejson
import re


class pincode_web(http.Controller):

    @http.route('/web/pincode/', type='http', auth="public", methods=['POST'], website=True)
    def verify(self,  **kw):
        # if select database
        db= kw.pop('db', None)
        # login, password,..
        login= kw.pop('login', None)
        password = kw.pop('password', None)
        redirect = kw.pop('redirect', None)
        pincode= kw.pop('pincode', None)
        numpin= kw.pop('numpin', None)

        if not db:
            db=db_monodb()
        if not numpin:
            numpin=0

        registry = RegistryManager.get(db)
        ipuser=request.httprequest.remote_addr

        with registry.cursor() as cr:
            res_users = registry.get('res.users')
            #check password/login for user => return l'id or false
            iduser=res_users.authenticate(db, login, password,user_agent_env=None)
            cr.commit()
            if iduser<>False :
                user=res_users.browse(cr,SUPERUSER_ID,iduser,context=None)
                if int(numpin)>0 :
                    #verify pin, if error return login/password
                    auth_log = registry.get('pincode.log')
                    auth_log=user.pincode_log_id[0]
                    if pincode<>auth_log.pincode:
                        vals=dict()
                        vals['states']="wrong"
                        vals['ipuser']=ipuser
                        authen_log = registry.get('pincode.log')
                        idlog=authen_log.write(cr,SUPERUSER_ID,user.pincode_log_id[0].id,vals)
                        return http.request.render('web.login', {'error':'Wrong pincode '})
                    else:
                        # if ok pincode
                        # is outdated ??
                        interval=str(datetime.now()-datetime.strptime(auth_log.date+".000000","%Y-%m-%d %H:%M:%S.%f")).split(".")
                        interval_sec=sum(int(x) * 60 ** i for i,x in enumerate(reversed(interval[0].split(":"))))
                        time_validity_sec=(user.pincode_id[int(numpin)-1].type_id.time_validity)*60*60 # in seconde
                        user.pincode_id[int(numpin)-1].type_id.time_validity
                        if interval_sec>time_validity_sec:
                              vals=dict()
                              vals['states']='outdated'
                              vals['ipuser']=ipuser
                              authen_log = registry.get('pincode.log')
                              idlog=authen_log.write(cr,SUPERUSER_ID,user.pincode_log_id[0].id,vals)
                              return http.request.render('web.login', {'error':'pincode outdated'})
                        else:
                              vals=dict()
                              vals['states']="used"
                              vals['ipuser']=ipuser
                              authen_log = registry.get('pincode.log')
                              idlog=authen_log.write(cr,SUPERUSER_ID,user.pincode_log_id[0].id,vals)
             
                if user.pincode_id and int(numpin)==0:
                    self.create_pincode(cr,registry,user.pincode_id[0],user.id)
                    return http.request.render('pincode.pincode', {
                            'login': login,
                            'password':password,
                            'db':db,
                            'redirect':redirect,
                            'numpin':1,
                        })
             
                # Login ok , pin ok => menu !
                url="/web"
                credentials=(cr.dbname, login, password)
                return login_and_redirect(*credentials, redirect_url=url)

        #if error return login
        return http.request.render('web.login', {'error':'Wrong login/password '})


    def generate_pins(self,length,format):
        if format=='numeric' :
            chars=string.digits
        if format=='alpha' :
            chars=string.ascii_uppercase + string.ascii_lowercase
        if format=='numeric&alpha' :
            chars=string.ascii_uppercase + string.ascii_lowercase + string.digits

        return ''.join(random.choice(chars) for x in range(0,length))

    def create_pincode(self,cr,registry,auth,userid):
        format=str(auth.type_id.format)
        pincode=self.generate_pins(int(auth.type_id.length),format)
        vals=dict()
        vals['date']=str(datetime.now())
        vals['pincode']=pincode
        vals['user_id']=userid
        authen_log = registry.get('pincode.log')
        idlog=authen_log.create(cr,SUPERUSER_ID,vals)
