from   django.conf.urls import  url, include
from   rest_framework.urlpatterns import format_suffix_patterns
import time_series.models as models

from .api_views import *

urlpatterns = [
    url(r'^regular/(?P<ts_id>[0-9]+)/$' , RegularTimeSeriesView.as_view(), name = "api.time_series.regular"),
    #
    url(r'^sampled/(?P<ts_id>[0-9]+)/$' , SampledTimeSeriesView.as_view(), name = "api.time_series.sampled"),
]


urlpatterns = format_suffix_patterns(urlpatterns)
