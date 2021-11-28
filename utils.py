from lxml import etree
import codecs
import simplejson as json
import pyproj

def findPosition(featureMember, gml, app):
  if featureMember.find('.//' + gml + 'MultiPoint') is not None:
    positions = featureMember.findall('.//' + gml + 'pos')
    coordinates = []
    for point in positions:
      p = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
      northing = float(point.text.split(" ")[1])
      easting = float(point.text.split(" ")[0])
      y, x = p(easting,northing,inverse=True)
      coordinates.append({"latitude": x, "longitude": y})
    return coordinates

  pos = featureMember.find('.//' + gml + 'pos')
  if pos is not None:
    p = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
    northing = float(pos.text.split(" ")[1])
    easting = float(pos.text.split(" ")[0])
    y, x = p(easting,northing,inverse=True)
    return [{"latitude": x, "longitude": y}]
  
  pos = featureMember.find('.//' + gml + 'posList')
  if pos is not None:
    pos = pos.text.split(" ")
    coordinates = []
    for i in range(0, len(pos), 2):
      p = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
      northing = float(pos[i + 1])
      easting = float(pos[i])
      y, x = p(easting,northing,inverse=True)
      coordinates.append({"latitude": x, "longitude": y})
    return coordinates


def findAlternativeNames(featureMember, name, gml, app):
  # Stedsnavn
  alt_names = []

  if featureMember.findall('.//' + app + 'annenSkrivemåte') is not None:
    # Ikke riktig, må lage en "query" som må finne kun de komplette skrivemetodene som har parent som er annenSkrivemnåte
    alternative_names = featureMember.findall('.//' + app + 'komplettskrivemåte')
    # './Sted/stedsnavn/annenSkrivemåte/Skrivemåte/' + app + 'komplettskrivemåte'
    print(alternative_names)
    for alternative_name in alternative_names:
      if alternative_name.text != name:
        alt_names.append({"name": alternative_name.text})
        print(alternative_name.text)
    

  return alt_names
  