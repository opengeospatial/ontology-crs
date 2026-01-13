
# SRS Ontology - Application module (Model)

`ogc.geosrs.app` *v0.1*

A building block defining SRS Ontology Application Module

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## SRS Ontology Application Module

This module describes how to model an SRS application entity using the SRS ontology vocabulary.

SRS Application classes and properties are described under the namespace https://w3id.org/geosrs/application/

![SRS Ontology Application Module](assets/application.png)
## Examples

### SRS Ontology SRS Application Module Example
#### ttl
```ttl
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix geosrs_app:<https://w3id.org/geosrs/application/> .
@prefix exsrs: <https://w3id.org/example-data-srs#> .

exsrs:mysrs geosrs_app:
```

## Sources

* [Sample source document](https://example.com/sources/1)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/opengeospatial/ontology-crs](https://github.com/opengeospatial/ontology-crs)
* Path: `_sources/app`

