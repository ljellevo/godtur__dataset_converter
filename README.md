# Converter for Norwegian map data
This program converts the dataset provided by Kartverket into a more managable dataset used for the GodTur app. The dataset provided from Kartverket introduced two problems when it comes to utilizing the data on solutions adaped for global location handling.
 
First of all, this program converts the GML file into a more managable JSON file with only the relevant fields for the app:
- Location
- Alternative names
- Latitude
- Longitude
- Unique identifier
- Priority

Secondly, the norwegian map coordinate standard is EUREF89. This is not widely supported by map libraries. A conversion is therefore made from EUREF89 to WGS84.

The result is a easy to manage JSON file with compatible coordinates.


To run:  
Change GML file to correct file.  
Ensure the tags are compatible with the relevant GML file.  
Specify JSON file for which the result should be stored..  
```
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
python convert.py
```

