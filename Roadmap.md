# Roadmap for a CRS ontology

This road map was put together on the wake of the GeoLD 2024 conference. It
follows on the [position paper](http://ceur-ws.org/Vol-3743/paper3.pdf)
published in that workshop, setting milestones and a time line towards a CRS Web ontology and registry/vocabulary.

## Milestones

1. Ontology alignment. Starting by creating a matrix matching classes
in ISO-19111, IGN and Proj4RDF. Then do the same for the data/object
properties for each individual class. This should lead to a "common" CRS ontology, then to decide the name space. Target completion date: **end of 2024**.

2. Review. Call on other geo-semantics people to review the CRS
ontology.  Candidates: Simon Cox, Krystof Janowich, Nic Carr, ...
Target completion date: spring of 2025.

3. Proof-of-concept. This should be a programme that translates RDF
compliant with the CRS ontology to WKT and back. Most of this work
should already be done in Proj4RDF. Target completion date: **Spring of 2025**.

4. Launch GeoCRS SWG. This should happen at one of the OGC users'
meeting, as a spin-off of the GeoSemantics DWG. The meeting in Europe
might be too early, so the Asia or Americas meetings in 2025 are the
targets.

5. Dissemination. Present the ontology and the proof-of-concept in
conferences during Spring/Summer of 2025. GeoLD and FOSS4G are obvious
candidates, but could be others. This needs steps 2 and 3 to be largely completed.

6. Implementation. Get Proj and GeoTools to natively support RDF
compliant with the CRS ontology. This might fit in the Google
Summer/Winter of Code programme.  The OSGeo Foundation usually gets a
good number of slots. Target date: beginning on the second half of 2025.

7. CRS registry. Convince the OGC to host a CRS registry, ideally
containing the full Proj database converted to RDF with PRoj4RDF.
Target date: **second half of 2025**.

8. Maintenance. Develop a maintenance plan for the registry, possibly
in coordination with the proj-data stewards. Possibly needs some
governance. To start after the registry is in place, say, **end of 2025**.

