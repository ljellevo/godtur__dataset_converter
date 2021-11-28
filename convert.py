# -*- coding: utf-8 -*-
# Old convertion code
import codecs
import xml.etree.ElementTree as ET
import simplejson as json
import pyproj




f = codecs.open("posisjoner.json", "w", encoding='utf8')
running_id = 0
print("Parsing file")
context = ET.iterparse("stedsnavn.gml", events=("start", "end"))
context = iter(context)
lokasjon = {}
priority = {}
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
      elif tag == '{http://skjema.geonorge.no/SOSI/produktspesifikasjon/StedsnavnForVanligBruk/20181115}sortering':
        priority = {"id": running_id, "priority": value}
        
    if "id" in lokasjon and "id" in posisjon and "id" in priority: 
      if lokasjon["id"] == posisjon["id"] == priority["id"]:
        p = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
        northing = float(posisjon["posisjon"].split(" ")[1])
        easting = float(posisjon["posisjon"].split(" ")[0])
        y, x = p(easting,northing,inverse=True)
        lokasjoner.append({"id": running_id, "location": lokasjon["lokasjon"], "latitude": x, "longitude": y, "priority": priority["priority"]})
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
