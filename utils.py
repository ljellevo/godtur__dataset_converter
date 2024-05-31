from lxml import etree
import codecs
import simplejson as json
import pyproj

def findPosition(featureMember, gml, app):
  if featureMember.find('.//' + gml + 'MultiPoint') is not None:
    positions = featureMember.findall('.//' + gml + 'pos')
    coordinates = []
    for point in positions:
      pair = []
      p = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
      northing = float(point.text.split(" ")[1])
      easting = float(point.text.split(" ")[0])
      y, x = p(easting,northing,inverse=True)
      pair.append(y)
      pair.append(x)
      coordinates.append(pair)
    return {"type": "MultiPoint", "coordinates": coordinates}

  pos = featureMember.find('.//' + gml + 'pos')
  if pos is not None:
    p = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
    northing = float(pos.text.split(" ")[1])
    easting = float(pos.text.split(" ")[0])
    y, x = p(easting,northing,inverse=True)
    return {"type": "MultiPoint", "coordinates": [[y, x]]}
  
  pos = featureMember.find('.//' + gml + 'posList')
  if pos is not None:
    pos = pos.text.split(" ")
    coordinates = []
    for i in range(0, len(pos), 2):
      p = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
      northing = float(pos[i + 1])
      easting = float(pos[i])
      y, x = p(easting,northing,inverse=True)
      coordinates.append([y, x])
    return {"type": "MultiPoint", "coordinates": coordinates}

def findAlternativeNames(featureMember, name, gml, app):
  # Stedsnavn
  alt_names = []

  if featureMember.findall('.//' + app + 'annenSkrivemåte') is not None:
    alternative_names = featureMember.findall('.//' + app + 'komplettskrivemåte')
    for alternative_name in alternative_names:
      if alternative_name.text != name:
        alt_names.append(alternative_name.text)
    

  return alt_names
  

# A B C D E F G H I J K M N O
# 14 13 12 11 10 9 8 7 6 5 4 3 2 1
def convertImportance(featureMemeber): 
  importance_sanitized = featureMemeber.replace("viktighet", "")
  importance = ord(importance_sanitized) - 64
  return importance
  
  
  
  
