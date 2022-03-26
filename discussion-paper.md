# Intro

# Benefits of an Ontology
## Authoritative CRS registries as Web data
The main interest of publishing authoritative CRS registries as Web data is to allow applications that implement GeoSPARQL, especially triplestores, to be able to manipulate coordinates defined in any CRS, as long as its definition is accessible through its URI. For the moment, triplestores only handle a limited number of hard-coded coordinate systems. For users, this means that there is very little choice as to which CRS to use, and it must be chosen before transforming the data into GeoSPARQL because the possibilities of transforming from one CRS to another are very limited or non-existent.

## Publishing custom CRS as Web data
From the 18th century onwards, old maps were based on coordinate reference systems defined by the cartographers of the time (e.g. the Cassini map). Various works in digital humanities or in the history of science are trying to find the parameters of these coordinate systems in order to make the georeferencing of old data, geolocated in these coordinate systems easier (e.g. hydrographic surveys or church tower positions) and their integration into a modern coordinate reference system possible. Publishing these CRS as Web data, according to a standard ontology, would allow their reuse by a large community.


# Use cases

## Linking a local CRS to a broader CRS
Coordinates within a building or an archaeological site can be expressed as (cartesian) coordinates with respect to a local origin. It may be useful to have those coordinates available with respect to a broader CRS, for example a global or national CRS.

## Coordinate transformation
When coordinate based spatial data are available from multiple sources, chances are that not all data use the same CRS.
An official CRS ontology and related CRS registry could help making the paramaters that are needed for coordinate transformation available to web-based procedures.

## Seamless selection of relevant spatial functions
The main CRS supported by the triplestores implementing GeoSPARQL is WGS84. In GIS software, there are different functions to perform spatial calculations like distance or area, depending on the type of coordinates used in the data (geographic ou plane coordinates): it is up to the user to be careful to use the right function. But often, in the implementations of GeoSPARQL, there is only one function, and it is sometimes difficult to know if you can really use it without risk of error with WGS84 coordinates. Allowing applications implementing GeoSPARQL to decide which function to apply depending on the type of CRS used would remove this difficulty for users.

## Application-specific and location-specific coordinate system recommendations
Choosing a suitable coordinate system requires expertise. Indeed, depending on the area covered by the data and the applications for which they are intended (precision spatial measurements, spatial statistics, cartography, etc.), different choices are possible and some are better than others. Publishing CRS descriptions as Web data could foster the development of application-specific and location-specific CRS recommendation systems.


# Prior Art

## GOM

## ISO 19111 Abstract Spec

The ISO 19111 UML model has been automatically converted to OWL ontologies. They are available at https://def.isotc211.org/ontologies/iso19111/.

### shortcomings of the ISO 19111 ontologies
Some shortcomings of the ISO 19111 ontologies that can be observered:

. Many URIs, including the ontology URIs, can not be resolved
. URI do not have the right data type
. Language tags for text literals are missing
. Content negotiation does not seem supported
. Separation in multiple ontologies seems unnecessary
. UML constraints are not translated (to SHACL, for example)
. Notes are not separate resources (and are not preceded by a space)
. Not all terms have definitions
. Blank nodes with an unclear meaning were generated
. Existing applicable web ontologies are not used (e.g. OWL Time, GeoSPARQL)

## IGNF CRS ontology
The national geographic institute of France (IGN France) has published an ISO-19111 based web ontology for CRS: http://data.ign.fr/def/ignf 

## proj4rdf

# Next Steps

## Who is best placed to create the ontology

## Which groups must be consulted/involved

## Should the ontology be modular? If so, how?
