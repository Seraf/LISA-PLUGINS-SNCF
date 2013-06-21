# -*- coding: UTF-8 -*-
import urllib, json
from bs4 import BeautifulSoup
from pymongo import MongoClient
from lisa import configuration

class SNCF:
    def __init__(self):
        self.configuration_lisa = configuration
        mongo = MongoClient(self.configuration_lisa['database']['server'], \
                            self.configuration_lisa['database']['port'])
        self.configuration = mongo.lisa.plugins.find_one({"name": "SNCF"})

    def getTrains(self):
        #lxml improve speed but need to be installed
        #soup = BeautifulSoup(urllib.urlopen(configuration['url'],"lxml"))
        soup = BeautifulSoup(urllib.urlopen(self.configuration['configuration']['url']))
        list_problemRSS = soup.find_all("title")
        list_problem_filter = []
        for problem in list_problemRSS:
            for ligne in self.configuration['configuration']['lignes']:
                if ligne['name'] in problem.get_text() and ligne['enabled'] == 'True':
                    list_problem_filter.append(unicode(problem.get_text()))
        if not list_problem_filter:
            return json.dumps({"plugin": "sncf","method": "getTrains", \
                               "body": u'Miracle, aucun problème à signaler'})
        else:
            return json.dumps({"plugin": "sncf","method": "getTrains", \
                               "body": u' puis '.join(list_problem_filter)})