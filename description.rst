ARCHIE: AIP Galaxy cluster catalog.
===================================
Aims
----
The aim of the project is to provide a tool to overview known data on clusters

Table structure
---------------
Every cluster in the database has it's unique number UID and a record in the main cluster table - *clusters*. This table contains only brief information on the unique clusters - for example, positions. When new catalog is injected into the database, its entries are cross-matched with the *clusters* table. If there is no match then a new unique cluster is added to *clusters*. Otherwise a match link is saved into *data_references* table.

All cluster catalogs are saved as individual tables with all columns and rows preserved  "as is". Metadata on each catalog is distributed in several tables:
 - *reference_tables* - contains information on each catalog table: it's  name, origin, name of the unique column (used in *data_references*), 	list of columns to be presented in a 'brief' mode and some other... This information has to be provided during input via parameters or a config file. It can be partly modified afterwards.
 - *reference_tables_columns* - contains information on all columns in the catalogs, including data units, output format and comments. This information is collected automatically from the input file, but may be changed manually.
 - *reference_tables_keys* - contains information on the properties of the important values stored in the catalog, indicating catalog columns containing the important value itself, error columns and comment columns.