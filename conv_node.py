# coding=utf-8

import re
from lxml import etree
import codecs
import simplejson as json
import pyproj
import sys, getopt

from utils import findPosition, findAlternativeNames, convertImportance
from api import deleteData, getToken, uploadData


def parseGML(tree): 
  location_type_object = json.load(open('posisjoner_type.json'))
  print("Finished parsing, getting root")
  root = tree.getroot()
  print("Got root")
  name = ""
  app = "{http://skjema.geonorge.no/SOSI/produktspesifikasjon/StedsnavnForVanligBruk/20181115}"
  gml = "{http://www.opengis.net/gml/3.2}"
  locations = []
  for featureMember in tree.findall('{http://www.opengis.net/gml/3.2}featureMember'):
    locationType = featureMember.find('.//' + app + 'navneobjekttype')
    locationType = locationType.text if locationType is not None else 'Ukjent'
    if(location_type_object[locationType] is True):
      # Find position, need to account for "multipoint" and poslist
      coordinates = findPosition(featureMember, gml, app)

      # finds name, need to account for multiple names
      # name = featureMember.find('.//' + app + 'komplettskrivemåte')
      # name = name.text if name is not None else 'No name record'
      
      språkprioriteringNode = featureMember.find('.//' + app + 'språkprioritering')
      if språkprioriteringNode is not None:
        for stedsnavn in featureMember.findall('.//' + app + 'Stedsnavn'):
          node = stedsnavn.find(app + 'språk')
          if node.text == språkprioriteringNode.text.split("-")[0]:
            name = stedsnavn.find('.//' + app + 'komplettskrivemåte').text
            
      alternative_names = findAlternativeNames(featureMember, name, gml, app)
      
      
      importance = featureMember.find('.//' + app + 'sortering')
      importance = convertImportance(importance.text) if importance is not None else -1
      
      municipality = featureMember.find('.//' + app + 'kommunenavn')
      municipality = municipality.text if municipality is not None else "Ukjent"
      # Says something about what kind of location it is

      county = featureMember.find('.//' + app + 'fylkesnavn')
      county = county.text.split(" - ")[0] if county is not None else "Ukjent"
      
      locations.append({
        "name": name, 
        "alternative_names": alternative_names, 
        "geo_json": coordinates, 
        "importance": importance if locationType != "by" else 11, 
        "location_type": locationType,
        "municipality": municipality,
        "county": county
      })
  return locations


def main(argv):
  extended = False
  locations = []
  from_cache = False
  try:
    opts, args = getopt.getopt(argv,"hec", ["extended, cache"])
  except getopt.GetoptError:
    print('conv_node.py (-e for entire dataset)')
    sys.exit(2)
    
  for opt, arg in opts:
    if opt == '-h':
      print('conv_node.py -e (for full dataset)')
      sys.exit()
    elif opt in ("-e", "--extended"):
      extended = True
    
    if opt in ("-c", "--cache"):
      from_cache = True
      
  if(extended is True):
    
    if(from_cache is True):
      f = codecs.open("posisjoner.json", "r", encoding='utf8')
      locations = f.read()
      print("Uploading parsed file")
      print("Getting token from API")
      token = getToken()
      print("Deleting old data from DB")
      deleteData(token)
      print("Uploading data")
      uploadData(token, json.dumps({"locations": locations}, ensure_ascii=False))
      f.close()
      
    else:
      f = codecs.open("posisjoner.json", "w", encoding='utf8')
      print("Starting loading GML file")
      tree = etree.parse('stedsnavn.gml')
      print("Started iterating GML tree")
      locations = parseGML(tree)
      print("Finished parsing file")
      print("Getting token from API")
      token = getToken()
      print("Deleting old data from DB")
      deleteData(token)
      print("Uploading data")
      uploadData(token, json.dumps({"locations": locations}, ensure_ascii=False))
      print("Finished iterating, dumping to file")
      f.write(json.dumps({"locations": locations}, ensure_ascii=False))
      f.close()
  else:
    
    if(from_cache is True):
      f = codecs.open("posisjoner_enkel.json", "r", encoding='utf8')
      locations = f.read()
      print("Uploading parsed file")
      print("Getting token from API")
      token = getToken()
      print("Deleting old data from DB")
      deleteData(token)
      print("Uploading data")
      uploadData(token, json.dumps({"locations": json.load(f)}, ensure_ascii=False))
      f.close()
    else:
      f = codecs.open("posisjoner_enkel.json", "w", encoding='utf8')
      print("Starting loading small GML file")
      tree = etree.parse('stedsnavn_enkel.gml')
      print("Started iterating GML tree")
      locations = parseGML(tree)
      print("Finished parsing file")
      print("Getting token from API")
      token = getToken()
      print("Deleting old data from DB")
      deleteData(token)
      print(  "Uploading data")
      uploadData(token, json.dumps({"locations": locations}, ensure_ascii=False))
      print("Finished iterating, dumping to file")
      f.write(json.dumps({"locations": locations}, ensure_ascii=False))
      f.close()
  

  

  
  
  
  # print("name=" + name + ", pos=" + pos + ", priority=" + priority)



  print("Done")
    #Need to append to array, make a json object and write to file
    #coordinates["latitude"], "longitude": coordinates["longitude"]
  return
  
  
if __name__ == "__main__":
  main(sys.argv[1:])