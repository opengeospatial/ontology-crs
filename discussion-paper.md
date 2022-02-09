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
This kind of serialization work for the purposes of GeoSPARQL 1.0, i.e. to allow comparisons between geometry representations, but overly complicate certain seemingly simple queries:
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
In almost all triple store implementations nowadays, proper CRS support is not 


### Linked data-aware SRS registries

### Federated queries and unknown coordinate reference systems



## Proposed Use Case 2

# Prior Art

## GOM

## ISO 19111 Abstract Spec

# Next Steps

## Who is best placed to create the Ontology

## Which groups must be consulted/involved
