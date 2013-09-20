#dGit Semantic Data management based on git

This is a rough prototype of wrapping git to provide git metadata in the web prov-o ontology developed in the Center for Research Computing (CRC) at the University of Notre Dame as part of the NSF Research Experiences for Undergraduates (REU) program by India Stewart and Judy Long under the direction of Charles Vardeman. An overview poster is available as part of this repository in the doc directory.

Git commands are wrapped using python to produce a provenance graph (provenance.ttl) using the W3C recommendation prov-o ontology (http://www.w3.org/TR/prov-o/) . This graph is stored in .dgit directory in the turtle serialization of RDF. Extensions were created to describe a repository file in more depth using the describe command. 