#!/usr/bin/env python

from uuid import uuid1
from jsonschema import Draft4Validator, SchemaError, RefResolver
from json import loads
from os import path
from sys import exit, argv, stderr, stdout
from optparse import OptionParser, make_option
from csv import DictReader
from urllib2 import urlopen

class Validator(Draft4Validator):

   __data_violation__= """
      ========================================
      Violation Id: %(violation_id)s
      Line Number: %(line_number)s
      Offset: %(offset)s
      Description: %(description)s
      Schema Path: %(schema_path)s
      Data Path: %(data_path)s
      Data Value: %(data_value)s
      Expected Value: %(expected_value)s
   """

   def __init__(self, schema, output= stdout):

      super(Validator, self).__init__(schema)
      self.output= output

   def run(self):

      line_number= 0
      for line in DictReader(opts.data):

         ints= ["Location_ID", "ACtion_ID"]
         floats= ["Location_Lat", "Location_Long", "Active_Discount"]

         line.update([(name, int(line.get(name))) for name in ints if line.get(name) not in ('', None)])
         line.update([(name, float(line.get(name))) for name in floats if line.get(name) not in ('', None)])
         #line.update([(k, None) for k, v in line.iteritems() if v == ''])

         line_number+= 1
         offset= opts.data.tell()

         for error in validator.iter_errors(line):

            violation= dict(
               violation_id= str(uuid1()),
               line_number= line_number,
               offset= offset,
               description= error.message,
               schema_path= list(error.schema_path),
               data_path= list(error.path),
               data_value= "''" if type(error.instance) in (str, unicode) and len(error.instance) == 0 else error.instance,
               expected_value= error.validator_value
            )

            print >> self.output, self.__data_violation__ % violation


def parse_args(argv):
   
   opt_args= []

   opt_parser= OptionParser()
   map(opt_parser.add_option, [
      make_option("-p", "--dir", default= None, help= "path to schema file"),
      make_option("-u", "--url", default= "http://localhost:8000/schema/", help= "url to schema"),
      make_option("-n", "--name", default= "action" , help="schema name"),
      make_option("-d", "--data", default= None, help= "path to data file"),
      make_option("-o", "--output", default= stdout, help= "path to output file"),
      make_option("-t", "--type", default= "all", help= "'schema' | 'data' | 'all' (default)")
   ])

   opt_parser.set_usage("%prog --schema=<schema file> --data=<data file>")
   (opts, args)= opt_parser.parse_args()

   if opts.type not in ("schema", "data", "all"):
      print >> stderr, "ERROR: invalid validation type"
      opt_parser.print_usage()
      exit(-1)

   if opts.type in ("schema", "all"):
      if opts.dir:
         if not path.exists(path.join(opts.dir, opts.name)):
            print >> stderr, "ERROR: schema file does not exist"
            exit(-1)
         else:
            opts.schema= open(path.join(opts.dir, opts.name), "r").read()
      elif opts.url:
         request= urlopen(opts.url + opts.name)
         opts.schema= request.read()

   if opts.type in ('data', 'all'):
      if opts.data == None:
         print >> stderr, "ERROR: no data file"
         opt_parser.print_usage()
         exit(-1)
      else:
         if not path.exists(opts.data):
            print >> stderr, "ERROR: data file does not exist"
            exit(-1)
         else:
            opts.data= open(opts.data, "r")


   if opts.output != stdout:
      opts.output= open(opts.output, "w")

   return opts


if __name__ == "__main__":

   opts= parse_args(argv)

   try:
      schema= loads(opts.schema)
   except Exception, e:
      print >> stderr, "ERROR: schema is invalid json", str(e)
      exit(-1)

   validator= Validator(schema)

   if opts.type in ("schema", "all"):
      try:
         validator.check_schema(schema)
      except SchemaError, e:
         print >> stderr, "ERROR: ", str(e)
         exit(-1)

   if opts.type in ("data", "all"):
      validator.run()
