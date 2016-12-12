#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
try:
    from gchelpers.ip.GeoDbManager import GeoDbManager
except:
    sys.path.append('..')
    from gchelpers.ip.GeoDbManager import GeoDbManager

geo_manager = GeoDbManager()
geo_manager.UpdateGoeIpDbs()

print(u'GeoIP database is updated')