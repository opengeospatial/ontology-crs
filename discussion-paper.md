# Intro

# Benefits of an Ontology
## Authoritative CRS registries as Web data

# Use cases

## Linking a local CRS to a broader CRS
Coordinates within a building or an archaeological site can be expressed as (cartesian) coordinates with respect to a local origin. It may be useful to have those coordinates available with respect to a broader CRS, for example a global or national CRS.

## Coordinate transformation
When coordinate based spatial data are available from multiple sources, chances are that not all data use the same CRS.
An official CRS ontology and related CRS registry could help making the paramaters that are needed for coordinate transformation available to web-based procedures.

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
