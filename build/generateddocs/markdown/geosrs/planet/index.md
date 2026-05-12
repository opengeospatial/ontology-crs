
# SRS Ontology - Planet module (Model)

`ogc.geosrs.planet` *v0.1*

A building block defining SRS Ontology Planet Module

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## SRS Ontology Planet Module

This module describes how to model a planetary entity using the SRS ontology vocabulary.

Planet classes and properties are described under the namespace https://w3id.org/geosrs/planet/

![SRS Ontology Planet Module](assets/planet.png)
## Examples

### SRS Ontology Planet Module Example
#### ttl
```ttl
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix geosrs_planet:<https://w3id.org/geosrs/planet#> .
@prefix geosrs:<https://w3id.org/geosrs/srs/> .
@prefix exsrs: <https://w3id.org/example-data-srs#> .

exsrs:mysrs rdf:type geosrs:CRS ;
            geosrs_planet:isApplicableTo exsrs:myplanet .

exsrs:myplanet rdf:type geosrs_planet:Planet ;
               rdfs:label "My planet" .

```

## Sources

* [Spec Section](https://opengeospatial.github.io/ontology-crs/spec/documents/spec/document.html#planet)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/opengeospatial/ontology-crs](https://github.com/opengeospatial/ontology-crs)
* Path: `_sources/planet`

