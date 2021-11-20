# -*- coding: utf-8 -*-

import codecs
import xml.etree.ElementTree as ET
# import json
from transform_service import transform_entity
from utils import parse_json_stream, entities_to_json
import simplejson as json


def generate(entities):
  yield "["
  for index, entity in enumerate(entities):
    if index > 0:
      yield ","

    # Transit decode
      
          
    entity = transform_entity(entity)
    yield entities_to_json(entity)
  yield "]"

    # get entities from request
  # req_entities = parse_json_stream(entities)

    # Generate the response

# f = open("posisjoner.json", "w")
f = codecs.open("posisjoner.json", "w", encoding='utf8')
running_id = 0
print("Parsing file")
context = ET.iterparse("stedsnavn.gml", events=("start", "end"))
context = iter(context)
lokasjon = {}
posisjon = {}
lokasjoner = []
print("File parsed")
print("Converting...")
for event, elem in context:
  tag = elem.tag
  value = elem.text
  if event == 'start' :
    if value and tag is not None:

      if tag == "{http://skjema.geonorge.no/SOSI/produktspesifikasjon/StedsnavnForVanligBruk/20181115}lokalId":
        running_id += 1
        
      if tag == "{http://www.opengis.net/gml/3.2}pos" :
        posisjon = {"id": running_id, "posisjon": value}
      elif tag == '{http://skjema.geonorge.no/SOSI/produktspesifikasjon/StedsnavnForVanligBruk/20181115}komplettskrivemåte':
        lokasjon = {"id": running_id, "lokasjon": value}
    
    if "id" in lokasjon and "id" in posisjon: 
      if lokasjon["id"] == posisjon["id"]:
        json_pos = generate([{ "_id": lokasjon["id"], "northing": posisjon["posisjon"].split(" ")[0], "easting": posisjon["posisjon"].split(" ")[1], "zone": "33"}])
        # curl -s -XPOST 'http://localhost:5001/transform' -H "Content-type: application/json" -d '[{ "_id": "jane", "northing": "12344", "easting": "6543", "zone": "32"}]' | jq -S .
        # print(list(json_pos)[1][lat])
        res = json.dumps(json_pos, iterable_as_array=True)
        lokasjoner.append({"id": running_id, "lokasjon": lokasjon["lokasjon"], "latitude": res.split(",")[5].split(": ")[1], "longitude": res.split(",")[6].split(": ")[1].replace('}"', "")})
        lokasjon = {}
        posisjon = {} 

  elem.clear()
print("Finished converting")
print("Writing to file")
f.write(json.dumps(lokasjoner, ensure_ascii=False))
f.close()
print("Done")

# EUREF89 UTM sone 33, 2d
# Må ta med sortering. A er lav pri, også går det høyere og høyere, viktighetI er høyest
# Multipoint
# Støtt geografiske områder
