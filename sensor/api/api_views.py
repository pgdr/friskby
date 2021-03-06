import json
import requests
import time
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.views import View
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework import status

import json
import sensor.models as models
from sensor.api.serializers import *
from sensor.api.info_serializers import *


def authenticate(device, api_key):
    """Raises an exception unless the device's key matches the provided api_key.
    """
    if not device.valid_post_key(api_key):
        raise KeyError('Invalid post key "%s" for device "%s".' % (api_key, device.id))



class MeasurementTypeListView(generics.ListCreateAPIView):
    queryset = models.MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer



class MeasurementTypeView(generics.RetrieveAPIView):
    queryset = models.MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer


#################################################################


class DeviceTypeListView(generics.ListCreateAPIView):
    queryset = models.DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceTypeView(generics.RetrieveAPIView):
    queryset = models.DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer

#################################################################

class DeviceView(View):
    #queryset = models.Device.objects.all()
    #serializer_class = DeviceSerializer


    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            key = None
            if "key" in request.GET:
                key = request.GET["key"]
            return self.get_detail( request , kwargs["pk"], key)
        else:
            return self.get_list( request )


    def get_list(self, request):
        data = []
        for dev in models.Device.objects.all():
            location_name = "-------"
            if dev.location:
                location_name = dev.location.name
            data.append( (dev.id , location_name ))

        return JsonResponse( data , status = status.HTTP_200_OK , safe = False )




    def get_detail(self , request , device_id, key):
        try:
            device = Device.objects.get( pk = device_id )
        except Device.DoesNotExist:
            return HttpResponse("The device id: %s is invalid" % device_id , status = status.HTTP_404_NOT_FOUND)

        serial = DeviceSerializer( data = device , context = {"key" : key})

        # Here we actually lock the device after a successfull
        # GET, to ensure that the device will not be dangling in
        # an open state. Should in addition have a scheduled job
        # locking all open devices.
        device.lockDevice( )

        return JsonResponse( serial.get_data( ) )



    def put(self , request , *args, **kwargs):
        device_id = kwargs["pk"]
        try:
            device = Device.objects.get( pk = device_id )
        except Device.DoesNotExist:
            return HttpResponse("The device id: %s is invalid" % device_id , status = status.HTTP_404_NOT_FOUND)

        data = json.loads( request.body )
        if "key" in data:
            if not device.valid_post_key( data["key"] ):
                return HttpResponse("Invalid key: %s for device:%s " % (data["key"], device_id) ,
                                    status = status.HTTP_403_FORBIDDEN )
        else:
            return HttpResponse("Missing key for device: %s" % device_id ,
                                status = status.HTTP_403_FORBIDDEN )

        if "git_ref" in data:
            device.client_version = data["git_ref"]
            device.save( )
            return HttpResponse("Client version set to: %s" % device.client_version, status = status.HTTP_200_OK )
        else:
            return HttpResponse("Empty payload?" , status = status.HTTP_204_NO_CONTENT)







#################################################################

class LocationListView(generics.ListCreateAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer


class LocationView(generics.RetrieveAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer

class LocationCreator(View):

    def get(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        device_data = DeviceSerializer(data=device)
        if 'key' not in request.GET:
            raise KeyError('Missing API-key "key".  Needed to authenticate.')
        authenticate(device, request.GET['key'])

        for k in ('latitude', 'longitude', 'name'):
            if k not in request.GET:
                raise KeyError('Missing key %s' % k)
        payload = {'key': request.GET['key'],
                   'latitude': request.GET['latitude'],
                   'longitude': request.GET['longitude'],
                   'name': request.GET['name'],
                   'altitude': 0,  # optional, set if exists
        }
        if 'altitude' in request.GET:
            payload['altitude'] = request.GET['altitude']
        loc = Location.create(payload)
        device.location = loc
        device.save()
        red = reverse("view.device.info", kwargs={'pk':device.id})
        return HttpResponseRedirect(red)

#################################################################


class DataTypeListView(generics.ListCreateAPIView):
    queryset = models.DataType.objects.all()
    serializer_class = DataTypeSerializer


class DataTypeView(generics.RetrieveAPIView):
    queryset = models.DataType.objects.all()
    serializer_class = DataTypeSerializer


#################################################################


class TimeStampListView(generics.ListCreateAPIView):
    queryset = models.TimeStamp.objects.all()
    serializer_class = TimeStampSerializer


class TimeStampView(generics.RetrieveAPIView):
    queryset = models.TimeStamp.objects.all()
    serializer_class = TimeStampSerializer


#################################################################


class SensorListView(generics.ListCreateAPIView):
    queryset = models.Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorView(generics.RetrieveAPIView):
    queryset = models.Sensor.objects.all()
    serializer_class = SensorSerializer


#################################################################

class SensorTypeListView(generics.ListCreateAPIView):
    queryset = models.SensorType.objects.all()
    serializer_class = SensorTypeSerializer


class SensorTypeView(generics.RetrieveAPIView):
    queryset = models.SensorType.objects.all()
    serializer_class = SensorTypeSerializer


#################################################################


class SensorInfoView(APIView):
    def get(self , request , sensor_id = None):
        if sensor_id is None:
            sensor_list = models.Sensor.objects.all()
        else:
            try:
                sensor_list = [ models.Sensor.objects.get( sensor_id = sensor_id ) ]
            except models.Sensor.DoesNotExist:
                return Response("The sensorID:%s is not found" % sensor_id , status.HTTP_404_NOT_FOUND)

        result = []
        for sensor in sensor_list:
            serialized = SensorInfoSerializer( sensor )
            data = serialized.data

            result.append( data )

        if sensor_id is None:
            return Response( result , status = status.HTTP_200_OK )
        else:
            return Response( result[0] , status = status.HTTP_200_OK )


class ReadingView(APIView):

#    def cleanPayload(self , data):
#        if "sensorid" in data:
#            sensorid = data["sensorid"]
#        else:
#            return (status.HTTP_400_BAD_REQUEST , "Missing 'sensorid' field in payload")
#
#
#        if "value" in data:
#            value = data["value"]
#        else:
#            return (status.HTTP_400_BAD_REQUEST , "Missing 'value' field in payload")
#
#        if not "timestamp" in data:
#            return (status.HTTP_400_BAD_REQUEST , "Missing 'timestamp' field in payload")
#
#        try:
#            sensor = models.Sensor.objects.get( pk = sensorid )
#            if not sensor.valid_input( value ):
#                return (status.HTTP_400_BAD_REQUEST , "The value:%s for sensor:%s is invalid" % (value , sensorid))
#
#            if sensor.parent_device.location is None:
#                if not "location" in data:
#                    return (status.HTTP_400_BAD_REQUEST , "Sensor:%s does not have location - must supply in post" % sensorid)
#
#        except models.Sensor.DoesNotExist:
#            return (status.HTTP_404_NOT_FOUND , "The sensorID:%s is not found" % sensorid)
#
#        return (True , "")



    def post(self , request , format = None):
        try:
            raw_data = RawData.create( request.data )
        except ValueError as e:
            return Response(str(e) , status = status.HTTP_400_BAD_REQUEST )

        rd        = raw_data[0]
        value     = rd.value
        timestamp = rd.timestamp_data
        location  = None
        sensor = rd.sensor

        if not sensor.valid_input( value ):
            return Response("The value:%s for sensor:%s is invalid" % (value , rd.sensor) , status.HTTP_400_BAD_REQUEST)
        value = float(value)

        if sensor.parent_device.location is None:
            if not "location" in request.data:
                return Response("Sensor:%s does not have location - must supply in post" % rd.sensor , status.HTTP_400_BAD_REQUEST)
            location = request.data["location"]


        if sensor.on_line:
            sensor.last_value = value
            sensor.last_timestamp = timestamp
            sensor.save()

            for rd in raw_data:
                rd.parsed = True
                rd.save( )

            return Response(1 , status.HTTP_201_CREATED)
        else:
            return Response("Sensor: %s is offline - rawdata created and stored" % rd.sensor_id )



    def get(self , request , sensor_id = None):
        if sensor_id is None:
            return Response("Must supply sensorid when querying" , status = status.HTTP_400_BAD_REQUEST )

        try:
            if "num" in request.GET:
                num = int(request.GET["num"])
            else:
                num = None

            if "start" in request.GET:
                start = models.TimeStamp.parse_datetime( request.GET["start"] )
            else:
                start = None

            sensor = models.Sensor.objects.get( sensor_id = sensor_id )
            ts = sensor.get_ts( num = num , start = start )
            return Response(ts , status = status.HTTP_200_OK )
        except models.Sensor.DoesNotExist:
            return Response("No such sensor:%s" % sensor_id , status = status.HTTP_404_NOT_FOUND )





class CurrentValueView(APIView):
    # Data which is older than the timeout is not considered
    # 'current'; and None is returned for the value.
    DEFAULT_TIMEOUT = 3600


    def get(self , request , sensor_id = None):
        if "mtype" in request.GET:
            mtype_id = int(request.GET["mtype"])
            try:
                mtype = models.MeasurementType.objects.get( pk = mtype_id )
            except models.MeasurementType.DoesNotExist:
                return Response("No such measuremenent type id:%s" % mtype_id , status = status.HTTP_404_NOT_FOUND )
        else:
            mtype = None

        timeout = CurrentValueView.DEFAULT_TIMEOUT
        if "timeout" in request.GET:
            timeout = int( request.GET["timeout"])

        if not sensor_id is None:
            try:
                sensor = models.Sensor.objects.get( sensor_id = sensor_id )
            except models.Sensor.DoesNotExist:
                return Response("No such sensor:%s" % sensor_id , status = status.HTTP_404_NOT_FOUND )

            if not mtype is None:
                if sensor.sensor_type.measurement_type != mtype:
                    return Response("Measurement type mismatch" , status = status.HTTP_400_BAD_REQUEST )

            data = sensor.get_current( timeout )
            if data is None:
                return Response("No current data" , status = status.HTTP_404_NOT_FOUND)
            else:
                return Response( data )
        else:
            if mtype is None:
                sensor_list = models.Sensor.objects.all( )
            else:
                sensor_list = models.Sensor.objects.filter( sensor_type__measurement_type = mtype )

            data = []
            for sensor in sensor_list:
                sensor_data = sensor.get_current( timeout )
                if sensor_data is None:
                    sensor_data = {"sensorid" : sensor.sensor_id }
                data.append( sensor_data )

            return Response( data )


class RawDataView(APIView):

    def get(self , request , sensor_id = None):
        try:
            sensor = models.Sensor.objects.get( sensor_id = sensor_id )
        except models.Sensor.DoesNotExist:
            return Response("The sensorID:%s is not found" % sensor_id , status = 404)#status.HTTP_404_NOT_FOUND)

        query = models.RawData.objects.filter( sensor = sensor )
        data = []
        for row in query:
            data.append( (row.timestamp_data , row.value ))

        return Response( data )

#################################################################

class ClientLogView(APIView):

    def post(self , request):
        data = request.data
        try:
            api_key = data["key"]
            device_id = data["device_id"]
            msg = data["msg"]
        except KeyError:
            return Response("Invalid log data" , status = 400)

        try:
            device = Device.objects.get( pk = device_id )
        except Device.DoesNotExist:
            return Response("Invalid device id:%s" % device_id , status = 400)

        if device.valid_post_key( api_key ):
            log_entry = ClientLog.objects.create( device = device,
                                                  msg = msg )
            if "long_msg" in data:
                log_entry.long_msg = data["long_msg"]

            log_entry.save()
            return Response(1 , status.HTTP_201_CREATED )
        else:
            return Response("Invalid key :%s" % api_key , status = 403)


    def get(self, request):
        data = []
        for log_entry in ClientLog.objects.filter( ):
            node = {"device"    : log_entry.device.id,
                    "timestamp" : log_entry.timestamp,
                    "msg"       : log_entry.msg ,
                    "long_msg"  : ""}

            if log_entry.long_msg:
                node["long_msg"] = log_entry.long_msg

            data.append( node )

        return Response( data )
