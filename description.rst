ARCHIE: AIP Galaxy cluster catalog.
===================================
Aims
----
The aim of the project is to provide a tool to overview known data on clusters.

This document contains a brief description of the database content and interface options. Database table names are given in *italics*, while interface page names or scripts are given in **bold**.


Tables related to clusters
--------------------------
Every cluster in the database has it's unique number UID and a record in the main cluster table - *clusters*. This table contains only brief information on the unique clusters - for example, positions. When new catalog is injected into the database, its entries are cross-matched with the *clusters* table. If there is no match then a new unique cluster is added to *clusters*. Otherwise a match link is saved into *data_references* table.

All cluster catalogs are saved as individual tables with all columns and rows preserved  "as is". Such tables are named reference tables.

Metadata on each catalog is distributed in several tables:
 - *reference_tables* - contains information on each catalog table: it's  name, origin, name of the unique column (used in *data_references*),  list of columns to be presented in a 'brief' mode and some other... This information has to be provided during input via parameters or a config file. It can be partly modified afterwards.
 - *reference_tables_columns* - contains information on all columns in the catalogs, including data units, output format and comments. This information is collected automatically from the input file, but may be changed manually.
 - *reference_tables_keys* - contains information on the properties of the important values stored in the catalog, indicating catalog columns containing the important value itself, error columns and comment columns.

Important values (or 'keys')
----------------------------
Some values are considered 'important' (for example, redshift, X-ray flux or extent) as it might be useful to view, for example, redshift estimates for a given cluster in different catalogs. Important values are defined in the table *keys* that hold information on the key (with subkey defining a more precise information, for example if a redshift is a photometric or a spectroscopic one), description and output format. This table can be edited in the **key list** section.

To collect important values from the catalogs *reference_tables_keys* table is used. It indicates for each reference table a column (or columns) containing values of the key (for example, redshift values).

Another way is to define a so-called per-cluster key. This is an important value associated directly to a given cluster UID and is contained in a special table *per_cluster_keys*. They can be created, edited and deleted by users. An example use for this might be to provide values obtained in a specific observation or extracted from literature. This way have to be used with care, as not to pollute the database.

Interface
---------

Main window
    Provides main menu and lots of search options

Search results
    Lists result of a search. Clicking on the table line will open a **cluster view** for a given item. Search results can be sent via SAMP or exported to votable.

Cluster view
    Provides all available information on a single cluster. General information like positions is followed by NED/Simbad search links, links to surveys that cover the cluster area, list of important values and at the bottom - entries from the reference tables. For these entries table with *brief columns* defined for this reference table are shown. Click on the grey area below such table to drop down/collapse a larger table with full catalog record. For the list of important values there are buttons to add/delete a per-cluster key. Clicking on the per-cluster key opens edit dialog (per-cluster keys can be identified by the source column - the value for them is "User defined").

Table list
    Lists all reference tables (catalogs) in the database and provides ways for editing metadata and keys.
    
Key list
    Provides list of all defined keys. It is possible to add, edit and delete keys. **Note:** if You delete a key, all entries in *reference_tables_keys* and *per_cluster_keys* will be deleted.
    
MOCs list
    So far - just a list of MOCs with no editing allowed.
    
Scripts
-------
aipgcd.py
    Main server script

drop_table.py -t table_name
    Deletes reference table and all its traces from DB. Use with care!

importer.py
    Flexible import tool with lots of parameters
    
mocify.py 
    Tool to add a new MOC map into DB
    