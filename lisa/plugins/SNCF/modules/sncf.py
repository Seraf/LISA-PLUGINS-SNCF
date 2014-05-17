# -*- coding: UTF-8 -*-
import urllib
from bs4 import BeautifulSoup

from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os


class SNCF(IPlugin):
    def __init__(self):
        super(SNCF, self).__init__()
        self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "SNCF"})
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
            inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
        self._ = translation = gettext.translation(domain='sncf',
                                                   localedir=self.path,
                                                   fallback=True,
                                                   languages=[self.configuration_lisa['lang']]).ugettext

    def getTrains(self, jsonInput):
        #lxml improve speed but need to be installed
        #soup = BeautifulSoup(urllib.urlopen(configuration['url'],"lxml"))
        soup = BeautifulSoup(urllib.urlopen(self.configuration_plugin['configuration']['url']))
        list_problemRSS = soup.find_all("title")
        list_problem_filter = []
        for problem in list_problemRSS:
            for ligne in self.configuration_plugin['configuration']['lignes']:
                if ligne['name'] in problem.get_text() and ligne['enabled'] == 'True':
                    list_problem_filter.append(unicode(problem.get_text()))
        if not list_problem_filter:
            return {"plugin": "sncf",
                    "method": "getTrains",
                    "body": _('no_problem')
            }
        else:
            return {"plugin": "sncf",
                    "method": "getTrains",
                    "body": _(' then ').join(list_problem_filter)}