#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import gzip
import shutil
import imp
import collections
import time
import logging
import requests
import json
import pkg_resources
import geoip2
import geoip2.database
from geoip2.errors import AddressNotFoundError

logging.basicConfig(
    level=logging.INFO
)

class GeoDbManager():
    def __init__(self):
        self.DB_ATTACHED = False
        
        package_dir = self._GetGeoDbDirectoryName()
        self.AttachGeoDbs(package_dir)
        
        if not self.DB_ATTACHED:
            logging.warn(u'No GeoDB found. Use GeoDbManager.AttachGeoDbs(geodb_path) or see documentation. GeoIP functionality will not be available.')
            
    def _GetGeoDbDirectoryName(self):
        package_dir = None
        
        try:
            package_dir = pkg_resources.resource_filename('geodb','.')
        except Exception as error:
            logging.warn(u'No resource {}'.format(str(error)))
            
            if os.path.isdir(u'../geodb'):
                package_dir = u'../geodb'
                
        return package_dir
    
    def UpdateGoeIpDbs(self):
        ''' Download a copy of the GeoLite Database
        '''
        url_geoip_city = u'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
        path = self._GetGeoDbDirectoryName()
        logging.info(u'GeoIP Folder: {}'.format(path))
        filename_gz_geoip_city = os.path.join(
            path,
            u'GeoLite2-City.mmdb.gz'
        )
        filename_geoip_city = os.path.join(
            path,
            u'GeoLite2-City.mmdb'
        )
        
        # Print license requirement
        self._CreateLicenseLink(path)
        print('This product includes GeoLite2 data created by MaxMind, available from <a href="http://www.maxmind.com">http://www.maxmind.com</a>.')
        request = requests.get(url_geoip_city, stream=True)
        with open(filename_gz_geoip_city, 'wb') as fh:
            for chunk in request.iter_content(chunk_size=1024): 
                if chunk:
                    fh.write(chunk)
                    
            fh.close()
            
        self._DeflateFile(
            filename_gz_geoip_city,
            filename_geoip_city
        )
        
    def _CreateLicenseLink(self,path):
        content = '''
        The GeoLite2 databases are distributed under the Creative Commons Attribution-ShareAlike 4.0 International License.
        The attribution requirement may be met by including the following in all advertising and documentation mentioning
        features of or use of this database:
        This product includes GeoLite2 data created by MaxMind, available from http://www.maxmind.com.
        
        See license at https://creativecommons.org/licenses/by-sa/4.0/legalcode'''
        filename = os.path.join(
            path,
            'CreativeCommonsLisense.txt'
        )
        with open(filename, 'wb') as fh:
            fh.write(content)
        
    def _DeflateFile(self,in_file,out_file):
        with open(out_file, 'wb') as decompressed_gz:
            with gzip.open(in_file, 'rb') as compressed_gz:
                shutil.copyfileobj(
                    compressed_gz,
                    decompressed_gz
                )
    
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
            except AddressNotFoundError as error:
                ip_info['ip'] = ip_address
                ip_info['error'] = unicode(error)
            except ValueError as error:
                ip_info['ip'] = ip_address
                ip_info['error'] = unicode(error)
            
        return ip_info