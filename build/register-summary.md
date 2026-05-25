# SRS Ontology

Building blocks for implementation of the OGC SRS ontology

Each building block defines a reusable JSON schema that is mapped to the equivalent SRS Ontology concept.

Each fragment allows for transparent and validatable use of JSON-LD contexts to map schema elements to equivalent terms from the GeoSPARQL ontology. 

 _These components are under review by the GeoSPARQL SWG as candidate canonical implementations._ 

 Each building block allows for examples transformed to RDF, which in turn allows for the use of SHACL rules to enforce the semantics of the GeoSPARQL specifications.


## Building Blocks

### `ogc.geosrs.app` — SRS Ontology - Application module

**Type:** model

A building block defining SRS Ontology Application Module

### `ogc.geosrs.co` — SRS Ontology - Coordinate Operation module

**Type:** model

A building block defining SRS Ontology Coordinate Operation Module

### `ogc.geosrs.cs` — SRS Ontology - Coordinate System module

**Type:** model

A building block defining SRS Ontology Coordinate System Module

### `ogc.geosrs.datum` — SRS Ontology - Datum module

**Type:** model

A building block defining SRS Ontology Datum Module

### `ogc.geosrs.planet` — SRS Ontology - Planet module

**Type:** model

A building block defining SRS Ontology Planet Module

### `ogc.geosrs.projection` — SRS Ontology - Projection module

**Type:** model

A building block defining SRS Ontology Projection Module

### `ogc.geosrs.srs` — SRS Core Ontology

**Type:** model

A building block defining the SRS Core Ontology

