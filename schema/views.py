# Create your views here.
#---------------------------------------------------------------------------
# Author: Richard J. Marini <richardjmarini@gmail.com>
# Date: 2014-07-07
# Description: Responsible for serving up JSON schemas
#---------------------------------------------------------------------------

from os import path
from pprint import pprint
from json import dumps, loads
from logging import getLogger

from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import views
from rest_framework import generics
from rest_framework import status
from jsonref import JsonRef, loads as jrloads, JsonRefError, dumps as jrdumps
from jsonschema import Draft4Validator, SchemaError


logger= getLogger(__name__)


class SchemaStore:
    """Responsible for retrieving schema from the store"""

    def __init__(self, schema_dir= "./schemas", schema_type= "json"):
        """Initalizes the schema store.

        :param name: schema_dir.
        :param type: str.
        :param schema_dir: path to the schema store.

        :param name: schema_type
        :param type: str.
        :param schema_type: format for objects in the schema store.
        """

        self.schema_dir= schema_dir
        self.schema_type= schema_type

    def get(self, schema):
        """Fetch schema from the store.

        :param name: schema.
        :param type: str.
        :param schmea: schema name to fetch from the store.

        :returns: dict -- the schmea.
        """
   
        # build the path to the schema file within the schema-store
        schema_file= path.join(self.schema_dir, "%s.%s" % (schema, self.schema_type))

        # read the schema file from the schema-store
        fh= open(schema_file, "r")
        schema_data= fh.read()
        fh.close()

        return schema_data


class SchemaView(views.APIView):
    """Generates schema view."""

    def get(self, request, schema_name, format= None):
        """Fetches schema from the schema-store and generates the view.

        :param name: schema_name.
        :param type: str.
        :param schema_name: name of schema to generate view for.

        :param name: format.
        :param type: str.
        :param format: format to generate the view in ("json"|"api")

        :returns: json -- the schema view.
        """

        # fetch the JSON schema 
        try:
            schema= SchemaStore(settings.SCHEMA_DIR, settings.SCHEMA_TYPE)
            version= request.QUERY_PARAMS.get('version')
            if version:
               schema_name= path.join(version, schema_name)
            schema_data= loads(schema.get(schema_name))
        except IOError, e:
            return Response(str(e), status= status.HTTP_404_NOT_FOUND)

        try:
            Draft4Validator.check_schema(schema_data)
        except SchemaError, e:
            return Response(str(e), status= status.HTTP_417_EXPECTATION_FAILED)

        return Response(schema_data, status= status.HTTP_200_OK)
