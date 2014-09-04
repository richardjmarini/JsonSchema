# Create your views here.
#---------------------------------------------------------------------------
# Author: Richard J. Marini <richardjmarini@gmail.com>
# Date: 2014-07-07
# Description: Responsible for basic document validation against a JSON schema
#---------------------------------------------------------------------------

from uuid import uuid1
from os import path
from pprint import pprint
from json import dumps, loads
from jsonref import JsonRef, loads as jrloads
from logging import getLogger
from urllib2 import urlopen
from re import match
from urllib2 import urlopen, HTTPError

from django.conf import settings
from rest_framework.response import Response
from rest_framework import views
from rest_framework import generics
from rest_framework import status
from jsonschema import Draft4Validator, SchemaError, RefResolver, FormatChecker
from jsonref import JsonRef, loads as jrloads, JsonRefError, dumps as jrdumps


logger= getLogger(__name__)


class DocumentStore:
    """Responsible for retrieving document form the store."""

    def __init__(self, data_dir= "./data", data_type= "json"):
        """Initializes the document store.

        :param name: data_dir.
        :param type: str.
        :param data_dir: path to the data store.

        :param name: data_type
        :param type: str.
        :param data_type: format for objects in the data store.
        """

        self.data_dir= data_dir
        self.data_type= data_type

    def get(self, document_id):
        """Fetch the dcoument from the document store

        :param name: document_id.
        :param type: str.
        :param document_id: unique identifier representing the document to be retrieved.

        :returns: dict -- the JSON document
        """

        fh= open(path.join(self.data_dir, "%s.%s" % (document_id, self.data_type)), "r")
        document= loads(fh.read())
        fh.close()

        return document


class ValidatorView(views.APIView):
    """Generates the validation view."""

    @FormatChecker.cls_checks("url", raises= Exception('invalid url'))
    def validate_url(value):
        """Format handler for validating a url.

        :param name: value.
        :param type: str.
        :param value: the url to be validated.
        
        :returns: bool -- True if valid or False if invalid
        """
     
        # validate the url by tryhing to fetch it
        try:
            # TODO: handle re-directs
            request= urlopen(value)
            request.read()
        except Exception, e:
            return False
 
        return True

    def validate_document(self, schema_name, document, version= None):

        # request schema
        try:
            schema_url= settings.SCHEMA_URL + settings.SCHEMA_URI + schema_name
            if version:
               schema_url+= "?version=%s" % (version)

            response= urlopen(schema_url)
            schema=  jrloads(response.read(), jsonschema= True, base_uri= settings.SCHEMA_URL)
        except HTTPError, e:
            raise
        
        # validate our document and collect the schema violations information
        validator= Draft4Validator(schema, format_checker= FormatChecker())
        violations= []
        for error in validator.iter_errors(document):
            violation= dict(
                violation_id= str(uuid1()),
                description= error.message,
                schema_path= list(error.schema_path),
                data_path= list(error.path),
                data_value= "''" if type(error.instance) in (str, unicode) and len(error.instance) == 0 else error.instance,
                expected_value= error.validator_value
            )
            violations.append(violation)
        
        return violations

    def get(self, request, schema_name, document_id, format= None):
        """Fetches a document from the data-store, fetches a schema from 
        the schema-store and then validates the document against the schema
        and generates the validation view.

        :param name: schema_name.
        :param type: str.
        :param schema_name: name of schema to validate document against.

        :param name: document_id.
        :param type: str.
        :param schema_name: unique identifier representing a document in the data-store.

        :param name: format.
        :param type: str.
        :param format: format to generate the view in ("json"|"api").

        :returns: json -- the validation view.
        """

        # TODO: replace this with fetch document from data store
        try:
            document_store= DocumentStore(settings.DATA_DIR, settings.DATA_TYPE)
            document= document_store.get(document_id)
        except IOError, e:
            return Response(str(e), status= status.HTTP_404_NOT_FOUND)

        version= request.QUERY_PARAMS.get('version')

        try:
           violations= self.validate_document(schema_name, document, version)
        except HTTPError, e:
           return Response(e.read(), status= e.code)
        
        response_status= status.HTTP_400_BAD_REQUEST if len(violations) else status.HTTP_200_OK
        return Response(violations, status= response_status)


class ValidatorPostView(ValidatorView):

    def __init__(self):
        super(ValidatorPostView, self).__init__()

    def get(self, request, schema_name, format= None):
        """Default validation view"""

        # do nothing

        return Response({}, status= status.HTTP_200_OK)

    def post(self, request, schema_name, format= None):
        """Fetches a schema from the schema-store and then 
        validates the POST'ed document against the schema
        and generates the validation view.

        :param name: schema_name.
        :param type: str.
        :param schema_name: name of schema to validate document against.

        :param name: format.
        :param type: str.
        :param format: format to generate the view in ("json"|"api").

        :returns: json -- the validation view.
        """

        document= request.DATA
        version= request.QUERY_PARAMS.get('version')

        try:
           violations= self.validate_document(schema_name, document, version)
        except HTTPError, e:
           return Response(e.read(), status= e.code)

        response_status= status.HTTP_400_BAD_REQUEST if len(violations) else status.HTTP_200_OK
        return Response(violations, status= response_status)
    
