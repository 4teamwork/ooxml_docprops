ooxml_docprops
==============

This package allows to update custom DocProperties in OOXML based documents.

Usage
-----

Command-Line Helper (for easy testing):

`update-properties <document> <metadata_json> [--debug]`

- <document>: Path to an OOXML document
- <metadata_json>: Path to a JSON file containing properties to be updated / added


Public API:

This package exposes one public function::

    update_properties(document, metadata, debug=False)

The file specified by the path `document` will be **modified in place**, by
updating / adding the metadata from the dictionary `metadata`.

Example::

    from ooxml_docprops.properties import update_properties

    update_properties('./example.docx', {'MyProperty': 12345})