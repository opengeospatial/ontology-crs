# CRS Ontology  
      
## Introduction     
This repository is used to work toward the development of an official OGC web ontology for coordinate reference systems (CRS). 
At present, we're simply working on documenting the benefits of a CRS ontology, but we're hoping that more will come as people determine value in the work.
   
## Definitions       
**spatial reference system:** A spatial reference system (SRS) is a system for establishing spatial position. A spatial reference system can use geographic identifiers (place names, for example), coordinates (in which case it is a coordinate reference system), or identifiers with structured geometry (in which case it is a discrete global grid system). 

**coordinate system:** A coordinate system is a set of mathematical rules for specifying how coordinates are to be assigned to points.
 
**datum:**      
A datum is a parameter or set of parameters that define the position of the origin, the scale, and the orientation of a coordinate system.

**coordinate reference system:**
A coordinate reference system (CRS) is a coordinate system that is related to an object by a datum.

**CRS registry:** A CRS registry is a collection of descriptions of coordinate reference systems.

## Scope
A CRS web ontology should be usable for all kinds of data that use numerical spatial coordinates, in one, two or three spatial dimensions. It should be applicable to irrespective of location or scale of the datum. For instance, coordinates could be relative to Earth, Mars, the solar system, an archeological site, a book page, or a computer screen. 

## Benefits and use cases
Having a standard CRS ontology on the Web will have major benefits that empower many use
cases. Here, we list four benefits and the use cases that each of them makes possible.

### Provision of CRS semantics on the Web
A standard CRS ontology will provide an RDF/RDFS/OWL representation of all concepts related
to coordinate reference systems. Various data and domain models for CRS definitions have
been issued by authorities such as the OGC and ISO. Reference software packages, such as
PROJ, feature a de facto standard data model. All of these are, at best, semantically defined in
an electronic document. Web-based and dereferenceable semantic definitions of CRS concepts
and parameters would make for a relevant advancement in the communication and correct use
of CRSs.
#### Use cases
1. Provide human readable definitions of CRS elements directly from geometric data to help
understand and prevent usage errors.
2. Provide a seamless link between geometric data and how their coordinates should be
interpreted.
3. Enable reasoning on CRS elements.
4. Enable expression of custom CRSs.
5. CRS data will be usable by both people and machines/algorithms.
6. Allow the ISO-19111 model to be easily extended, for example, for extraterrestrial CRSs
or other customized extensions.
7. Allow CRS specifications to be used in dataset metadata, optionally removing the need
for specifying the CRS for individual geometries.
8. Allow all CRS elements to be used in (federated) SPARQL queries. For example, filter by
unit of measurement or by applicable area.
9. Enable CRS recommendations, based on the extent of the concerned spatial dataset and
coordinate precision.
### Enable publication of CRS registries on the Web
Once a standard CRS web ontology is brought online, expressing any CRS in RDF will be
possible. In turn, this will enable the publication of collections of RDF-based CRS definitions in
CRS registries, allowing data and datasets to use common URIs to reference CRSs.
#### Use cases
1. An official CRS registry by e.g. the OGC can be published, providing common URIs for
common CRSs that can be resolved to RDF data.
2. Remove the need to replicate and update the parameters of common CRSs to data stores.
3. Well-known official IRIs can be used to match CRSs in web searches or federated searches.
Example: find all datasets with a CRS that matches an interactive web map.
4. Official national grids can be published by national mapping and cadastral agencies.
5. Enable validation of coordinate data, e.g. via  [SHACL](https://www.w3.org/TR/shacl. For example: check if all coordinate
values are within the extreme values.
6. Allow CRS specifications to be used in metadata standards, GeoDCAT-AP25 for example.
7. Allow existing Web practices to be underpinned with shared semantics (for example: [HTML5 Geolocation](https://www.w3.org/TR/geolocation/), [W3C basic geo](https://www.w3.org/2003/01/geo/), [schema.org GeoCoordinates](https://schema.org/GeoCoordinates)).
8. Stand-alone systems that do not publish data on the Web can benefit from access to
up-to-data CRS data, without needing local copies that run the risk of being outdated.
9. Allow provision of JSON-LD contexts for established JSON-based CRS schemes.
### Complement GeoSPARQL
[GeoSPARQL](https://www.ogc.org/standard/geosparql/) is arguably the most important standard for spatial data on the Web. It offers
ways to work with geometry, which is reliant on CRS data, but the standard does not include
CRS semantics. A standard CRS ontology would, therefore, be a welcome complement to
GeoSPARQL.
#### Use cases
1. CRS registries can provide targets for a new property of the GeoSPARQL Geometry class
that identifies the CRS.
2. GeoSPARQL currently has no way to encode geometry in RDF. It relies on non-RDF
serialisations to express geometry. A standard CRS ontology would contain definitions of
the coordinate and coordinate reference system concepts, which are two basic com-
ponents of the definition of Geometry. The envisioned ontology would thus strengthen
the definition of geometries as RDF resources.
3. (Federated) GeoSPARQL queries become feasible with geometries that use a custom CRS
(a CRS not included in any CRS registry).
25https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/
geodcat-application-profile-data-portals-europe/release/101
### Increase interoperability of spatial data on the Web
Many types of spatial data, not only geographical data, use coordinates and therefore need
CRS specifications. A standard CRS ontology can provide increased semantic and operational
interoperability between all coordinate-based data.
#### Use cases
1. Geographic geometry and other types of geometry can use the same CRS semantics.
2. Facilitates georeference with local CRSs.
3. Makes coordinate transformations possible with Linked Data tools.
4. CRS semantics will be made available to knowledge domains outside of geoinformatics,
e.g. in the cultural heritage domain.
5. Historical coordinate reference systems can be published using the same semantics as
modern CRSs. For example, the CRS parameters of the Verniquet map, a large-scale map
of Paris produced on the eve of the French Revolution, could be published in RDF [ 19 ].
This would make the CRS available to the scientific community for geo-referencing with
subsequent plans of Paris, which were based on the CRS created by Edme Verniquet for
the purposes of surveying

