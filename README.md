# Converter for Norwegian map data
This program converts the dataset provided by Kartverket into a more managable dataset used for the GodTur app. The dataset provided from Kartverket introduced two major problems when it comes to utilizing the data on solutions adaped for global location handling.
 
First of all, this program converts the GML file into a more managable JSON file with only the relevant fields for the app:
- Location
- Latitude
- Longitude
- Unique identifier
- TODO: Priority

Secondly, the norwegian map coordinate standard is EUREF89. This is not widely supported by map libraries. A conversion is therefore made from EUREF89 to WGS84. This is done using existing code from the https://github.com/sesam-community/utm-to-latlong repository - tailored to this solution.

The result is a easy to manage JSON file with compatible coordinates.