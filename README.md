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
A CRS web ontology should be usable for all kinds of data that use numerical spatial coordinates, in one, two or three spatial dimensions. It should be applicable to irrespective of location or scale of the datum. For instance, coordinates could be relative to Earth, Mars, the solar system, a construction site, a book page or a computer screen. 

## Benefits

- An official CRS ontology will allow CRS registries to be made available on the Web.
  - CRS registries on the web will allow direct lookups of relevant CRS data by both human users and machine algorithms.
- An official CRS ontology will make the OGC CRS model available to web developers.
- An official CRS ontology allows publication of standard OGC CRS registry as Web data.
  - An official OGC CRS registry allows existing Web practices to be underpinned with shared semantics (for example: [HTML5 Geolocation](https://www.w3.org/TR/geolocation/), [W3C basic geo](https://www.w3.org/2003/01/geo/), [schema.org GeoCoordinates](https://schema.org/GeoCoordinates)).
- A CRS Ontology will allow custom CRSs to be published on the Web with proper semantic foundation.
  - Users of data stores that support GeoSPARQL are now limited to a limited collection of CRSs supported by the data store.
- Stand-alone systems that do not publish data on the Web can benefit from access to up-to-data CRS data, without the need for local copies that run the risk of being outdated.
- An official CRS ontology based on [OGC Abstract Specification Topic 2: Referencing by coordinates](https://docs.opengeospatial.org/as/18-005r4/18-005r4.html), which only covers geography, will allow ontological extensions to be published. Extensions to the model could provide means to define extraterrestial CRSs, or other CRSs that do not have a direct connection with the Earth's surface.

