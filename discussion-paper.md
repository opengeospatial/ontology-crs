# Intro

Coordinate reference systems are an integral part of any representation of geospatial data. Coordinate reference systems help to relate coordinates of given geometry representations with actual positions on Earth or any other referencable planetoid.
Over the centuries, countries and mapping agencies have created hundreds of different coordinate reference system types which vary by their area of validity, their types (2D, 3D), their projections and various other parameters which are in common use on many map projections. 

## Definition

Essential elements of a coordinate reference system include:
* The coordinate system in which the coordinates are defined
* A reference to e.g. planetoid to which the coordinates are related

## Serializations of coordinate reference systems

The parameters of coordinate reference systems can be serialized in data formats such as Well-Known Text (WKT) [OGC WKTCRS] or proj4.

```
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.0174532925199433,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]
```

## Coordinate reference system identifiers and registries

The INSPIRE[^1] coordinate system specification assigns identifiers to the reference coordinate systems that it recommends to use [INS 09]. 
Its corresponding implementation specification [INS 14] recommends to implement a registry for the dissemination of CRS identifiers and their associated descriptions. 
In the ISO TC-211 series of standards for geographic information, a registry is an "information system on which a register is maintained"; 
a register is defined as "set of files containing identifiers assigned to items with descriptions of the associated items" [ISO 15]. 
The INSPIRE implementation specification therefore advises that the URIs proposed by OGC (Open Geospatial Consortium, see section "Who is best placed to create the ontology") should be used as identifiers for coordinate reference systems - examples of such URI can be found in the GeoSPARQL standard [OGC 2012].

### URIs to identify coordinate reference systems on the Web of data 

In order to be consistent with the Web of Data best practices, the coordinate reference system identifiers should be dereferenceable URIs, as stated in GeoSPARQL standard [OGC 12]. 
To foster the adoption of this practice, the OGC proposes URIs to identify the most commonly used reference coordinate systems on the Web, including WGS84 and the coordinate reference systems recommended by the INSPIRE Directive.
These redirect to descriptions of the corresponding reference coordinate systems extracted from the EPSG geodetic parameters registry, compliant with the ISO 19111 standard on spatial referencing by coordinates [ISO 07]. 
The ISO 19111 standard provides a conceptual model for the description of reference coordinate systems and the geodetic objects that compose them.
Thus the URI http://www.opengis.net/def/crs/EPSG/0/4326 returns the GML [OGC 07] description of the WGS84 coordinate reference system as provided by the EPSG.
However, this initiative does not cover all existing coordinate reference systems and the descriptions returned are not provided in RDF [RDF_SPEC] but in GML. 
Furthermore, the URIs proposed by OGC are based on the reference coordinate system identifiers of the EPSG registry. 
These identifiers are well known to the geographic information science community, but remain completely non-transparent to the non-experts. 
An example is the identifier "4326" which refers to the WGS84 reference coordinate system in the EPSG registry.

### State-of-the-art of CRS registries

Several Web services give access to much more comprehensive registries of coordinate reference systems. 
These include the EPSG Geodetic Parameter Registry, EPSG.io, Coordinates Reference Systems in Europe and SpatialReference.org.  

The **EPSG Geodetic Parameter Registry**[^2] is maintained by the Geomatics Committee of the International Association of Oil and Gas Producers[^3]. 
It allows queries to be made on a dataset describing the geodetic parameters of several thousand reference coordinate systems. 
The available coordinate reference systems can be retrieved by name, code, type or area covered and their descriptions are displayed directly on the service's Web page and can be exported either in WKT or in GML format.
However, no direct access by URI dereferencing and content negotiation is possible.

In contrast, the **EPSG.io service**[^4] provides access to the descriptions of the coordinate reference systems stored in the EPSG dataset using dereferenceable URIs. 
These URIs are defined based on the original identifiers of the coordinate reference systems in the EPSG register. 
Thus the description of WGS84 is provided following the URI: http://epsg.io/4326.
It can be downloaded in many different formats, but no RDF description is available for now: OGC WKT, ESRI WKT, GML, PROJ.4, USGS, GeoServer, MapServer, PostGIS, etc. 

The **European Reference Coordinate System Service**[^5] provides access to ISO 19111 compliant descriptions of the main European coordinate reference systems. 
It has the same limitations of use as the EPSG Geodetic Parameter Register: access to the data by dereferencing URIs is not possible, users have to retrieve the CRS they are interested in by means of a cartographic interface or html links. Descriptions are provided only in HTML, no other format seems to be availble. 

Finally, the **SpatialReference.org**[^6] registry also provides access to the description of many coordinate reference systems by dereferencing their URIs. 
Its underlying register has the particularity of being populated by the registry users, who can contribute to its content. 
However, like the URIs proposed by the OGC, those used by this registry remain totally opaque, including for geographic information scientists. 
As an example, the URI for the Lambert93 projected coordinate reference system within this register is written as follows: http://spatialreference.org/ref/sr-org/7527/.
Its description can also be downloaded in many different formats, but no RDF description is available for now: OGC WKT, ESRI WKT, GML, .PRJ, JSON, GeoServer, USGS, PostGIS, etc. 

The **French national mapping agency (IGN France) registry**[^7].
Consistently with the requirements of the INSPIRE Directive, IGN France publishes a register of coordinate reference systems defined and maintained by the agency. 
In this register, coordinate reference systems are identified by URIs that use short names rather than numerical codes to designate geodetic resources, i.e. coordinate reference systems, datums, ellipsoids, axes, meridians, etc.. 
For example, the "Lambert 2 étendu" projected coordinate reference system, which is based on the NTF (Nouvelle Triangulation Française) geodetic coordinate reference system, is identified by the URI: https://registre.ign.fr/ign/IGNF/crs/IGNF/NTFLAMB2E. 
The description of geodetic resources is structured according to the ISO 19111 model and provided in XML format. 
The equivalence relations between the geodetic resources described by the IGN and those provided by the EPSG register are explicitly stated in the dataset by using EPSG identifiers. 
This register is regularly updated and the way it is published has evolved over the last few years: originally available in the form of a single XML file that could be downloaded from the geodesie.ign.fr Website, its content is now directly accessible by dereferencing the URIs identifying the described geodetic resources. 
However, these descriptions are still provided in XML format, which makes it impossible to query them using SPARQL queries.

Definitions of coordinate reference systems are often assigned identifiers and registered in specialized registry portals such as the EPSG repository.
The descriptions of the parameters of the various coordinate reference systems can be downloaded in many formats commonly used in the field of geographic information (WKT, GML, XML, GeoServer, \*.PRJ, etc.), except on the European Reference Coordinate System service. 
None of these registries, however, provide the coordinate reference system descriptions in the RDF model. Accessing the coordinate reference system descriptions provided by these services using SPARQL queries is therefore impossible.
The actual definitions of CRS behind such registries, e.g. the EPSG database is often used in software libraries and database implementations to allow for conversions between geospatial data served in different coordinate reference system definitions. 
For linked data based databases, but also spatial relational databases such as PostGIS, the EPSG database as either a relational database table or as a separate provided database are state of the art tools to allow a conversions between geometries.

[^1]: See https://inspire.ec.europa.eu/inspire-directive/2 for a description of the INSPIRE European Directive.
[^2]: https://epsg.org/
[^3]: https://www.iogp.org/our-committees/geomatics/
[^4]: https://epsg.io/ 
[^5]: http://www.crs-geo.eu/
[^6]: https://spatialreference.org/
[^7]: https://registre.ign.fr/ign/IGNF/IGNF/

# Benefits of an Ontology
This section outlines benefits of an ontology in general, but with particular focus on coordinate reference systems.
Ontologies are the standard way of describing semantic data on the web, i.e. a way for semantically described data to be machine-accessible and human-accessible at the same time.

## Authoritative CRS registries as Web data
The main interest of publishing authoritative CRS registries as Web data is to allow applications that implement GeoSPARQL, especially triplestores, to be able to manipulate coordinates defined in any CRS, as long as its definition is accessible through its URI. For the moment, triplestores only handle a limited number of hard-coded coordinate systems. For users, this means that there is very little choice as to which CRS to use, and it must be chosen before transforming the data into GeoSPARQL because the possibilities of transforming from one CRS to another are very limited or non-existent.

## Publishing custom CRS as Web data
From the 18th century onwards, old maps were based on coordinate reference systems defined by the cartographers of the time (e.g. the Cassini map). Various works in digital humanities or in the history of science are trying to find the parameters of these coordinate systems in order to make the georeferencing of old data, geolocated in these coordinate systems easier (e.g. hydrographic surveys or church tower positions) and their integration into a modern coordinate reference system possible. Publishing these CRS as Web data, according to a standard ontology, would allow their reuse by a large community.

# Use cases

This section wants to highlight possible use cases for a CRS ontology which are currently not possible using semantic web technologies.

## Linking a local CRS to a broader CRS
Coordinates within a building or an archaeological site can be expressed as (cartesian) coordinates with respect to a local origin. It may be useful to have those coordinates available with respect to a broader CRS, for example a global or national CRS. The same case can be made for building information management (BIM) approaches.

## Coordinate transformation
When coordinate based spatial data are available from multiple sources, chances are that not all data use the same CRS.
An official CRS ontology and related CRS registry could help making the paramaters that are needed for coordinate transformation available to web-based procedures.

## Seamless selection of relevant spatial functions
The main CRS supported by the triplestores implementing GeoSPARQL is WGS84. In GIS software, there are different functions to perform spatial calculations like distance or area, depending on the type of coordinates used in the data (geographic ou plane coordinates): it is up to the user to be careful to use the right function. But often, in the implementations of GeoSPARQL, there is only one function, and it is sometimes difficult to know if you can really use it without risk of error with WGS84 coordinates. Allowing applications implementing GeoSPARQL to decide which function to apply depending on the type of CRS used would remove this difficulty for users.

## Application-specific and location-specific coordinate system recommendations
Choosing a suitable coordinate system requires expertise. Indeed, depending on the area covered by the data and the applications for which they are intended (precision spatial measurements, spatial statistics, cartography, etc.), different choices are possible and some are better than others. For example, when working with geographical data on a European scale, the INSPIRE Directive recommends different reference coordinate systems depending on their intended use: for analyses requiring exact surface representations, the (https://spatialreference.org/ref/epsg/3035/)[ETRS89-LAEA] system is recommended, while pan-European mapping applications at scales smaller than 1: 500,000 should use the (https://spatialreference.org/ref/epsg/3034/)[ETRS89-LCC] projected coordinate system and those at scales larger than 1:500,000 should use the ETRS89-TMzn Transverse Mercator projected coordinate system, where "zn" is the projection area number. [INS 09] Publishing CRS descriptions as Web data could foster the development of application-specific and location-specific CRS recommendation systems.

## Proposed Use Case: GeoSPARQL and Triple Store Integration

This section describes how a CRS ontology can be integrated to be used in the GeoSPARQL query language.

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
In probably all geospatial-aware triple store implementations nowadays, proper CRS support is not achieved by encoding CRS definitions in an RDF graph, but rather by keeping an additional database of CRS definitions (such as the [EPSG database](https://epsg.org/)) along with the triple store implementation.
This additional database is merely used to dereference the URIs found in literal types to a Well-Known Text representation of the given coordinate reference system.
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

Federated queries in the semantic web using the SPARQL query language allow for the execution on SPARQL queries on different semantic web resources, hosted in different SPARQL endpoints. For example, it might be possible to query the triple store of a national mapping agency and the triple store of the national bureau of statistics in order to retrieve building data and statistics on these individual buildings.
For this purpose, both triple stores might host geospatial data in different coordinate reference systems and the receiving triple store needs to be able to interpret even coordinate reference system definitions which are not hosted in its own database.
If every triple store implementation can be expected to include an EPSG database one could assume that geospatial queries using these CRS identifiers will work. 
In practice, custom CRS definitions make this assumption not a reality and currently, there is not defined way of expressing customized coordinate references systems in RDF, potentially rendering federated queries to triple stores with such definitions unresolvable.


## Representation of coordinate systems for non-georeferenced data

Increasingly, 3D models are subject to be shared in online repositories, such as [heidICON](https://heidicon.ub.uni-heidelberg.de/).
To filter and describe 3D models and their provenance, vocabularies have been defined recently [(Homburg et.al., 2021)](http://doi.org/10.1186/s40494-021-00561-w) which capture the measurement process, scanners and people involved in creating the respective scan.

This representation necessarily also contains a description of the coordinate system in WKT in which the 3D model has been defined, a property often absent even in 3D sharing formats such as PLY or OBJ.
Yet, a WKT string can only serve as a description of the whole coordinate system and not expose its attributes.

Queries such as:
**Give me all 3D models which are encoded in coordinate systems defined in millimeters**
are unnecessarily complex and could be simplified in a representation of coordinate systems in RDF.
This would allow the sharing of metadata of 3D objects in linked data repositories as backends of 3D model online repositories with extended filter capabilities.


# Prior Art

Prior to this publication, there have been several authoritative and not authoritative approaches to create an ontology model for coordinate reference systems. Authoritative approaches have been derived from official specification from ISO or OGC and non-authoriative approaches have been the work of research projects of of software libraries which implemented converters from EPSG databases to RDF.

## GOM

## ISO 19111 Abstract Spec

The ISO 19111 UML model [ISO 07] has been automatically converted to OWL ontologies. They are available at https://def.isotc211.org/ontologies/iso19111/.

### shortcomings of the ISO 19111 ontologies
Some shortcomings of the ISO 19111 ontologies that can be observered:

. Many URIs, including the ontology URIs, can not be resolved
. URI do not have the right data type
. Language tags for text literals are missing
. Content negotiation does not seem supported
. Separation in multiple ontologies seems unnecessary
. UML constraints are not translated (to SHACL [SHACL_SPEC], for example)
. Notes are not separate resources (and are not preceded by a space)
. Not all terms have definitions
. Blank nodes with an unclear meaning were generated
. Existing applicable web ontologies are not used (e.g. OWL Time [OWL_TIME], GeoSPARQL)

## The CRS ontology and CRS registry of IGN France

As part of the **Datalift** project[^8], two main vocabularies, compliant with GeoSPARQL, have been proposed to publish geographic vector data on the Web. 
They have been designed to represent structured geometries on the Web [HAM 14], to associate them with any coordinate reference system identified by a URI and to describe this coordinate reference system in RDF. 
The former vocabulary is thus dedicated to structured geometries (http://data.ign.fr/def/geometrie#) and the latter to geodetic resources (http://data.ign.fr/def/ignf#). 
This latter vocabulary adopts the main concepts of the ISO 19111 model to describe geodetic resources and uses, as much as possible, concepts and properties from other well-known vocabularies for the less specialised aspects of the description of these resources such as units of measure.
However, as it has been designed to publish IGN France geodetic register, only the concepts and properties useful to represent this register data have been included in the vocabulary. 
As an example, the concept of "Engineering coordinate reference system", which is part of ISO 19111 model but not used in IGN France geodetic register, is not included in the vocabulary yet.

As a use case, these two vocabularies have been used to publish IGN France's reference data on French administrative units and IGN's register of reference coordinate systems according to the good practices of the Web of Data [ATE 14]. 
The interest in publishing this register of coordinate reference systems is twofold. 
Firstly, it makes it possible to identify the French coordinate reference systems defined and maintained by the IGN, some of which, although old, are still used for very specific applications, or cover very small areas, and do not necessarily appear in the general registries presented in section "State-of-the-art of CRS registries" in order to associate them with the geometries of vector geographic data published on the Web of data. 
In addition, it allows this register to be queried using SPARQL queries and thus to access its contents without having to process the original XML files. 

The register data was converted into RDF and published using the Datalift platform. Some changes have been introduced to avoid any confusion between the official IGN France coordinate reference system register and this version published as a use case of a research project: the original URIs of the geodetic resources were replaced by URIs in http://data.ign.fr/id/ignf/. 
Thus, the entire register is now acessible in the following named graph : http://data.ign.fr/id/ignf/ It is also directly queryable via this SPARQL endpoint: http://data.ign.fr/id/sparql. As an example, the following URI provides access to the RDF description of the "Lambert 2 étendu" projected coordinate reference system: http://data.ign.fr/id/ignf/crs/NTFLAMB2E. 


[^8]: funded by the French National Research Agency under grant number ANR-10-CORD-009

## proj4rdf

The proj4rdf project tried to extract an RDF vocabulary from existing libraries which implement and extend the ISO 19111 model.
Several extensions of the ISO 19111 ontology are part of proj4rdf:
- Integration of a class hierarchy of projections
- Integration of interstellar bodies and links to spheroids
- 

https://docs.opengeospatial.org/as/18-005r4/18-005r4.html

### Software libraries implementing CRS support according to ISO 19111

Several software libraries have implementated support for ISO 19111 defintions of coordinate reference systems. One of the most promiment software libraries it the [PROJ library](https://proj.org), which has implementations in [Java (Proj4J)](https://github.com/locationtech/proj4j), [Python (PyProj)](https://github.com/pyproj4/pyproj)

## Datalift Project

Actually, this work has been carried out on the CRS register published by IGN France : it is the same work as described in section "IGNF CRS ontology and CRS registry". I suggest to group both descriptions and to delete this section.

The first ontology to describe spatial reference systems was created in the datalift project ([Troncy et.al ](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.708.2684&rep=rep1&type=pdf)).
This ontology was used as a proof of concept to refer to coordinate reference systems using more commonly understood identifiers than EPSG codes.
However, it did not encode every parameters which is usually found in a coordinate reference system definition.


# Next Steps
In this section we will outline the next steps we think the community needs to be taking towards the creation of a CRS ontology.

## Who is best placed to create the ontology
We believe that a CRS ontology should at best be created with an organization which is recognized as an authority in at least one of the following communities:
* GIS community
* Semantic Web Community
Typical organizations which create standards for these communities are the [Open Geospatial Consortium (OGC)](https://www.ogc.org) and the [World Wide Web Consortium (W3C)](https://www.w3c.org). Both organizations share a joined interest group, the OGC GeoSemanticsDWG and the W3C Spatial Data On The Web Working Group.

## Which groups must be consulted/involved

## Should the ontology be modular? If so, how?
While this publication mainly focused on coordinate reference systems which describe positions on Earth, there are other forms of coordinate reference system types which one could consider.
Coordinate refefence systems might relate to other planets in the solar system, such as Mars Rover positions on planet Mars. 
Also, coordinates are used in coordinate systems which describe interstellar positions, not necessarily with a plantoid to relate to.

Finally, there are forms of spatial references which do not rely on coordinates, i.e. cannot be represented as coordinate reference systems. These more general spatial reference systems [ISO 03] may use geocoding approaches, addresses or other forms of spatial references which might need to be considered in the ontology model, but do not form the core of what a coordinate reference system ontology aims to represent.

For all of these aforementioned reasons it might make sense to create a modular ontology model which may be used to represent these further items and which might be ready for further extensions.

# References

[ATE 14] Ghislain Auguste Atemezing, Nathalie Abadie, Raphaël Troncy and Bénédicte Bucher. Publishing Reference Geodata on the Web : Opportunities and Challenges for IGN France. Terra Cognita 2014, 6th International Workshop on the Foundations, Technologies and Applications of the Geospatial Web. 2014, Riva del Garda, Italy.

[HAM 14] Fayçal Hamdi, Nathalie Abadie, Bénédicte Bucher, Abdelfettah Feliachi. GeomRDF: A Geodata Converter with a Fine-Grained Structured Representation of Geometry in the Web. 1st International Workshop on Geospatial Linked Data (GeoLD 2014). In Conjunction with the 10th International Conference on Semantic Systems, 2014, Leipzig, Germany.

[INS 09] INSPIRE Thematic Working Group on Coordinate Reference Systems & Geographical Grid Systems. Guidelines INSPIRE Specification on Coordinate Reference Systems [online]
http://inspire.ec.europa.eu/documents/Data_Specifications/INSPIRE_Specification_CRS_v3.0.pdf. Accessed on 31/05/22. 2009.

[INS 14] INSPIRE Thematic Working Group Coordinate Reference Systems & Geographical Grid Systems. D2.8.I.1 Data Specification on Coordinate Reference Systems – Technical Guidelines. [online] 
http://inspire.ec.europa.eu/documents/Data_Specifications/INSPIRE_DataSpecification_RS_v3.2.pdf. Accessed on 31/05/22. 2014.

[ISO 03] International Organization for Standardization. ISO 19112. Geographic information - Spatial referencing by geographic identifiers. International Standard. February 1st, 2019.

[ISO 07] International Organization for Standardization. ISO 19111. Geographic information - Referencing by coordinates. International Standard. January 1st, 2019.

[ISO 15] International Organization for Standardization. ISO 19135-1. Geographic information — Procedures for item registration — Part 1: Fundamentals. International Standard. First edition. October 1st, 2015.

[OGC 07] Open Geospatial Consortium. OGC 07-036. OpenGIS Geography Markup Language (GML) Encoding Standard. Version 3.2.1., 2007.

[OGC 12] Open Geospatial Consortium. OGC 11-052r4. OGC GeoSPARQL - A Geographic Query Language for RDF Data. Version 1.0., 2012.

[OGC WKTCRS] Open Geospatial Consortium. OGC 18-010r7. Geographic information — Well-known text representation of coordinate reference systems., 2018.

[OWL_TIME] World Wide Web Consortium. W3C Canidate Recommendation and OGC 16-071r3. Time Ontology in OWL., 2020. [online]
https://www.w3.org/TR/owl-time/

[RDF_SPEC] RDF 1.1 Concepts and Abstract Syntax. W3C Recommendation, 2014. [online]
https://www.w3.org/TR/rdf11-concepts/

[SHACL_SPEC] Shapes Constraint Language (SHACL). W3C Recommendation, 2017. [online]
https://www.w3.org/TR/shacl/

