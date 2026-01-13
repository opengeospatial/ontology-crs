
# SRS Ontology - Datum module (Model)

`ogc.geosrs.datum` *v0.1*

A building block defining SRS Ontology Datum Module

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## SRS Ontology Datum Module

This module describes how to model a datum using the SRS ontology vocabulary.

Datum classes and properties are described under the namespace https://w3id.org/geosrs/datum/

![SRS Ontology Datum Module](assets/datum.png)
## Examples

### SRS Ontology Datum Module Example
#### ttl
```ttl
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix geosrs_datum:<https://w3id.org/geosrs/datum/> .
@prefix exsrs: <https://w3id.org/example-data-srs#> .

exsrs:mydatum rdf:type geosrs:GeodeticDatum ;
              rdfs:label "European Datum 1950" ;
              geosrs_datum:ellipsoid exsrs:myellipsoid .
exsrs:myellipsoid rdf:type geosrs_datum:Ellipsoid ;
                  rdfs:label "International 1924" ;
                  geosrs_datum:inverseFlattening 297 ;
                  geosrs_datum:semiMajorAxis 6378388 .
```

## Sources

* [Sample source document](https://example.com/sources/1)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/opengeospatial/ontology-crs](https://github.com/opengeospatial/ontology-crs)
* Path: `_sources/datum`

