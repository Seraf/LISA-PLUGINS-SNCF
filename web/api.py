from tastypie import authorization
from django.conf.urls.defaults import *
from tastypie import resources
from tastypie.utils import trailing_slash
import json
try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

class SNCF(object):
    def __init__(self):
        return None

class SNCFResource(resources.Resource):
    class Meta:
        resource_name = 'sncf'
        allowed_methods = ()
        authorization = authorization.Authorization()
        object_class = SNCF
        extra_actions = [
            {
                'name': 'gettraffic',
                'summary': 'Give the current traffic of the SNCF Transilien',
                'http_method': 'GET',
                'fields': {}
            },
        ]

    def base_urls(self):
        return [
            url(r"^plugin/(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^plugin/(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_schema'), name="api_get_schema"),
            # Will be accessible by http://127.0.0.1:8000/api/v1/plugin/sncf/gettraffic/
            url(r"^plugin/(?P<resource_name>%s)/gettraffic%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('gettraffic'), name="api_plugin_sncf_gettraffic"),
        ]

    def gettraffic(self, request, **kwargs):
        from tastypie.http import HttpAccepted
        from SNCF.modules.sncf import SNCF

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'content': json.loads(SNCF().getTrains())}, HttpAccepted)
