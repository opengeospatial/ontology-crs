
# SRS Ontology - Coordinate System module (Model)

`ogc.geosrs.cs` *v0.1*

A building block defining SRS Ontology Coordinate System Module

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## SRS Ontology Coordinate System Module

This module describes how to model a coordinate system using the SRS ontology vocabulary.

Coordinate system classes and properties are described under the namespace https://w3id.org/geosrs/cs/

![SRS Ontology Coordinate System Module](assets/cs.png)




## Examples

### Example
#### ttl
```ttl
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/> .
@prefix geosrs_cs:<https://w3id.org/geosrs/cs#> .
@prefix exsrs: <https://w3id.org/example-data-srs#> .

exsrs:ecs rdf:type geosrs_cs:geosrs:EllipsoidalCoordinateSystem ;
          rdfs:label "My example EllipsoidalCoordinateSystem with two axis";
          geosrs_cs:axis exsrs:ecs_axis1, exsrs:ecs_axis2 .
exsrs:ecs_axis1 rdf:type geosrs_cs:Axis ;
                rdfs:label "Geodetic latitude" ;
                om:hasUnit om:degree ;
                skos:altLabel "Lat" ;
                geosrs_cs:axisDirection geosrs_cs:North .
exsrs:ecs_axis2 rdf:type geosrs_cs:Axis ;
                rdfs:label "Geodetic longitude" ;
                om:hasUnit om:degree ;
                skos:altLabel "Lon" ;
                geosrs_cs:axisDirection geosrs_cs:East .




```

#### ttl
```ttl
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/> .
@prefix geosrs_cs:<https://w3id.org/geosrs/cs#> .
@prefix exsrs: <https://w3id.org/example-data-srs#> .
exsrs:ecsc rdf:type geosrs_cs:CartesianCoordinateSystem ;
           rdfs:label "My example cartesian coordinate system with two axis";
           geosrs_cs:axis exsrs:ecsc_axis1, exsrs:excsc_axis2 .
exsrs:ecsc_axis1 rdf:type geosrs_cs:Axis ;
                 rdfs:label "Northing" ;
                 om:hasUnit om:metre ;
                 skos:altLabel "N" ;
                 geosrs_cs:axisDirection geosrs_cs:North .
exsrs:ecsc_axis2 rdf:type geosrs_cs:Axis ;
                 rdfs:label "Easting" ;
                 om:hasUnit om:metre ;
                 skos:altLabel "E" ;
                 geosrs_cs:axisDirection geosrs_cs:East .

```

## Sources

* [Sample source document](https://example.com/sources/1)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/opengeospatial/ontology-crs](https://github.com/opengeospatial/ontology-crs)
* Path: `_sources/cs`

