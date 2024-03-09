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

## Benefits
- An official CRS ontology will enable the specification of coordinate reference systems on the Semantic Web and make the OGC CRS model available to web developers.
- An official CRS ontology will allow CRS registries to be made available on the Web.
  - CRS registries on the Web will allow direct lookups of relevant CRS data by both human users and machine algorithms; spatial data can have a seamless link to data that specify how coordinates should be interpreted.
- An official CRS ontology allows publication of a standard OGC CRS registry as Web data.
  - An official OGC CRS registry allows existing Web practices to be underpinned with shared semantics (for example: [HTML5 Geolocation](https://www.w3.org/TR/geolocation/), [W3C basic geo](https://www.w3.org/2003/01/geo/), [schema.org GeoCoordinates](https://schema.org/GeoCoordinates)).
  - A standard CRS registry can provide well-known CRS IRIs to be used as an alternative to EPSG codes. These IRIs provide direct access to CRS descriptions that can be presented in human readable form or machine readable form.
  - A standard CRS registry providing well-known CRS IRIs can help finding and filtering spatial data on the web by means of the CRS used.
- A CRS Ontology will allow custom CRSs to be published on the Web with proper semantic foundation.
  - Users of data stores that support GeoSPARQL are now limited to a limited collection of CRSs supported by the data store.
- Semantics for spatial data on the Web, [GeoSPARQL](https://www.ogc.org/standard/geosparql/) for example, are incomplete at the moment, because there is no official web ontology for interpreting the coordinates of geometry.
- [GeoSPARQL](https://www.ogc.org/standard/geosparql/) at the moment has no way to encode geometry in RDF. It relies on non-RDF serialisations to express geometry. An official CRS ontology would contain definitions of the **coordinate** and **coordinate reference system** concepts, which are two basic components of the definition of **Geometry**. So an official CRS ontology could help development of a defintion of geometry in GeoSPARQL in RDF only.
- Stand-alone systems that do not publish data on the Web can benefit from access to up-to-data CRS data, without the need for local copies that run the risk of being outdated.
- An official CRS ontology based on [OGC Abstract Specification Topic 2: Referencing by coordinates](https://docs.opengeospatial.org/as/18-005r4/18-005r4.html), which only covers geography, will allow ontological extensions to be published. Extensions to the model could provide means to define extraterrestial CRSs, or other CRSs that do not have a direct connection with the Earth's surface.
- An official CRS ontology will enable development of coordinate validation tools, for example based on [SHACL](https://www.w3.org/TR/shacl).
- An official CRS ontology can help linking a local CRS to a global CRS, for example georeferencing a construction site.
- An official CRS ontology can help interoperability between all knowledge domains that use coordinate based spatial data.

