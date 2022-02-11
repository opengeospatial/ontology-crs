# Intro

# Benefits of an Ontology

## Proposed Use Case: GeoSPARQL and Triple Store Integration

### Integration of CRS into the GeoSPARQL query language

The GeoSPARQL 1.0 specification allows the integration of coordinate reference system definitions in the literals describing the content of a geo:Geometry.
For example, the following excerpt describes a WKT-serialized Geometry in the GeoSPARQL 1.0 vocabulary:

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . 
@prefix sf: <http://www.opengis.net/ont/sf#> . 
@prefix ex: <http://example.org/> . 
ex:mypolygon rdf:type sf:Polygon .
ex:mypolygon geo:asWKT "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> Polygon((-83.6 34.1, -83.2 34.1, -83.2 34.5, -83.6 34.5, -83.6 34.1))"^^geo:wktLiteral .
```
The coordinate reference system of this geometry is described inside the literal description using a URI.
This kind of serialization works for the purposes of GeoSPARQL 1.0, i.e. to allow comparisons between geometry representations, but overly complicate certain seemingly simple queries:

**Query 1: Give me all WKT geometries encoded in a specific coordinate reference system**
```sparql
SELECT ?geom_wkt WHERE {
  ?item geo:hasGeometry ?geom .
  ?geom geo:asWKT ?geom_wkt .
  FILTER(CONTAINS(?geom_wkt,"http://www.opengis.net/def/crs/OGC/1.3/CRS84"))
}
```
While this query works for WKT literals with a URI for CRS84 as stated here, it might not work with equivalent representations of the same URI and would need to be adjusted with filter statements for other defined literal types if needed.

While this first example may be simply seen as an inconvenience, the next example is currently not possible with GeoSPARQL 1.0:

**Query 2: Check whether all geometries in the given knowledge graph are in their respective CRS area of use**

This query might be resolved in at least the two following ways:
* Definition of a new query function for the GeoSPARQL query language which returns the area of use of a CRS
```sparql
SELECT ?geom_wkt WHERE {
  ?item geo:hasGeometry ?geom .
  ?geom geo:asWKT ?geom_wkt .
  FILTER(geof:sfContains(geof:crsAreaOfUse(?geom_wkt),?geom_wkt))
}
```
* Creation of an RDF representation of the CRS system using the URI it was defined as and accessing the area of use from this RDF representation.
```turtle
SELECT ?geom_wkt WHERE {
  ?item geo:hasGeometry ?geom .
  ?geom geo:asWKT ?geom_wkt .
  ?geom geo:inSRS ?geom_crs .
  ?geom_crs geocrs:areaOfUse ?areaofuse .
  FILTER(geof:sfContains(?areaofuse,?geom_wkt))
}
```

The second representation has many advantages compared to the first representation:
* It does not depend on the definition of SPARQL extension functions
* It may be used to retrieve any attribute of a coordinate reference system once an RDF representation has been agreed upon
* It even allows the filtering of geometries by CRS in a simple SPARQL 1.0 query engine which does not support GeoSPARQL

### Representation of CRS systems within geospatial-aware triple stores 
In probably all geospatial-aware triple store implementations nowadays, proper CRS support is not achieved by encoding CRS definitions in an RDF graph, but rather by keeping an additional database of CRS definitions (such as the EPSG database) along with the triples store implementation.
This additional database is merely used to deference the URIs found in literal types to a Well-Known Text representation of the given coordinate reference system.
In essence, this can be seen as a relict of relational geospatial databases such as PostGIS in which a special database table is used to store coordinate reference system definitions.

The representation of coordinate reference systems in this way comes with certain disadvantages:
* Only a selected amount of coordinate reference systems can be included in the given triple store, courtesy of the triple store developer
* It is usually impossible or requires special knowledge to add new coordinate reference system definitions to the additional database shipped with the triple store
* Federated queries on geospatial data are only possible if the local database of CRS systems includes the CRS system definition of the encoded geometries

A better solution for triple store implementers would be to encode coordinate reference systems directly in RDF.
Not only could they be saved in e.g. a special named graph of coordinate reference system definitions, but also they could be shared to other triple stores in a federated query scenario.
In addition, it would enable any data provider to easily encode, also non-commonly used coordinate reference system definitions (e.g. along with their data in an RDF graph).

### Linked data-aware SRS registries

Many CRS reqistries allow the definition of own types of coordinate reference systems. While these registries allow to access these resources for example in WKT, they usually do not support sharing these kinds of data in a linked data compatible way, i.e. as a SPARQL endpoint or as an RDF dump which could be referred to.
One reason for this might be that no vocabulary in RDF exists to share CRS definitions. 
This does not necessarily warrant the definition of a CRS RDF vocabulary, one could simply share coordinate reference system definitions as simple RDF graphs with WKT literals.  

### Federated queries and unknown coordinate reference systems


## Representation of coordinate systems for non-georeferenced data

Increasingly, 3D models are subject to be shared in online repositories, such as [heidICON](https://heidicon.ub.uni-heidelberg.de/).
To filter and describe 3D models and their provenance, vocabularies have been defined recently [(Homburg et.al., 2021)](http://doi.org/10.1186/s40494-021-00561-w) which capture the measurement process, scanners and people involved in creating the respective scan.

This representation necessarily also contains a description of the coordinate system in WKT in which the 3D model has been defined, a property often absent even in 3D sharing formats such as PLY or OBJ.
Yet, a WKT string can only serve as a description of the whole coordinate system and not expose its attributes.

Queries such as:
**Give me all 3D models which are encode in coordinate systems defined in millimeters**
are unnecessarily complex and could be simplified in a representation of coordinate systems in RDF.
This would allow the sharing of metadata of 3D objects in linked data repositories as backends of 3D model online repositories with extended filter capabilities.


## Proposed Use Case 2

# Prior Art

## GOM

## ISO 19111 Abstract Spec

https://docs.opengeospatial.org/as/18-005r4/18-005r4.html

### Software libraries implementing CRS support according to ISO 19111



PROJ: https://proj.org

## Datalift Project

The first ontology to describe spatial reference systems was created in the datalift project ([Troncy et.al ](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.708.2684&rep=rep1&type=pdf)).
This ontology was used as a proof of concept to refer to coordinate reference systems using more general 

# Next Steps

## Who is best placed to create the Ontology

## Which groups must be consulted/involved
