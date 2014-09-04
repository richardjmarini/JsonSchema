# Create your views here.
#---------------------------------------------------------------------------
# Author: Richard J. Marini <richardjmarini@gmail.com>
# Date: 2014-07-07
# Description: Responsible for transforming objects of one schema to another.
#---------------------------------------------------------------------------

from dateutil import parser
from datetime import datetime
from sys import stdout
from os import path
from pprint import pprint
from json import dumps, loads
from jsonref import loads as jrloads
from logging import getLogger
from urlparse import urlparse
from urllib2 import urlopen, HTTPError

from jsonref import JsonRef, loads as jrloads, JsonRefError

from django.conf import settings
from django.template import Template, Context, loader
from rest_framework.response import Response
from rest_framework import views
from rest_framework import generics
from rest_framework import status
from rest_framework import renderers


logger= getLogger(__name__)

class TransformView(views.APIView):
    """Generates transform view."""

    def get(self, request, schema_name, format= None):
        return Response({}, status= status.HTTP_200_OK)

    def post(self, request, schema_name, format= None):
        """creates view of a an object transformed from one schema to another"""

        document= request.DATA

        # retreive schema for payload definition
        try:
            schema_url= settings.SCHEMA_URL + settings.SCHEMA_URI + document.get("payload_type") + "/"
            response= urlopen(schema_url)
            schema=  jrloads(response.read(), jsonschema= True, base_uri= settings.SCHEMA_URL)
        except HTTPError, e:
            return Response(e.read(), status= e.code)

        # TODO: dynamically render template from schema -- using static template for now.
        template= loader.get_template(schema_name)

        # TODO: walk payload and convert values to native types for template filtering
        payload= document.get("payload")

        c= Context(payload)

        print "Schema Url:", schema_url
        print "Schema Name:", schema_name
        print "Schema", schema
        print "Transformed Data:", template.render(c)

        # render template and return transformed JSON structure
        return Response(loads(template.render(c)), status= status.HTTP_200_OK)
