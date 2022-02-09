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
* **Give me all WKT geometries encoded in a specific coordinate reference system**
```sparql
SELECT ?geom_wkt WHERE {
  ?item geo:hasGeometry ?geom .
  ?geom geo:asWKT ?geom_wkt .
  FILTER(CONTAINS(?geom_wkt,"http://www.opengis.net/def/crs/OGC/1.3/CRS84"))
}
```
While this query works for WKT literals with a URI for CRS84 as stated here, it might not work with equivalent representations of the same URI and would need to be adjusted with filter statements for other defined literal types if needed.

While this first example may be simply seen as an inconvenience, the next example is currently not possible with GeoSPARQL 1.0:
* **Check whether all geometries in the given knowledge graph are in their respective CRS area of use**

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

Many CRS reqist

### Federated queries and unknown coordinate reference systems


## Representation of coordinate systems for non-georeferenced data



## Proposed Use Case 2

# Prior Art

## GOM

## ISO 19111 Abstract Spec

# Next Steps

## Who is best placed to create the Ontology

## Which groups must be consulted/involved
