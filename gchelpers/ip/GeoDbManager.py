#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import imp
import collections
import time
import logging
import geoip2
import geoip2.database
from geoip2.errors import AddressNotFoundError
import json

# logging.basicConfig(level=logging.INFO)

class GeoDbManager():
    def __init__(self):
        self.DB_ATTACHED = False
        import pkg_resources
        package_dir = None
        
        try:
            package_dir = pkg_resources.resource_filename('geodb','.')
        except Exception as error:
            logging.warn(u'{}'.format(error))
            
            if os.path.isdir(u'../geodb'):
                package_dir = u'../geodb'
            else:
                logging.warn(u'No GeoDB found. Use GeoDbManager.AttachGeoDbs(geodb_path)')
        
        self.AttachGeoDbs(package_dir)
    
    def AttachGeoDbs(self,geodb_path):
        self.geodb_path = geodb_path
        self.city_reader = None
        
        # logging.info('geodb_path: {}'.format(self.geodb_path))
        for root, subdirs, files in os.walk(self.geodb_path):
            for filename in files:
                # logging.info('filename: {}'.format(filename))
                if filename == 'GeoLite2-City.mmdb':
                    city_db = os.path.join(self.geodb_path,'GeoLite2-City.mmdb')
                    # logging.info('city_db: {}'.format(city_db))
                    self.city_reader = geoip2.database.Reader(city_db)
                    self.DB_ATTACHED = True
    
    def GetIpInfo(self,ip_address):
        ip_info = collections.OrderedDict([])
        if self.city_reader:
            try:
                city_info = self.city_reader.city(ip_address)
                ip_info['ip'] = ip_address
                ip_info['continent'] = city_info.continent.names['en']
                ip_info['country'] = city_info.country.names['en']
                ip_info['iso_code'] = city_info.country.iso_code
            except AddressNotFoundError:
                ip_info['ip'] = ip_address
            
        return ip_info