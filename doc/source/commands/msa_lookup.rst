msa-lookup
==========

SYNOPSIS
--------

.. code:: bash

   msa-lookup -h | --help
   msa-lookup --page=<uri>
       [--regexp=<expression>]

DESCRIPTION
-----------

The MSA lookup captures the request metrics, request_date,
response_time, status_code and optionally if the content
matches a given regular expression for the specified page.
The information is stored in a kafka message broker for
later use.

OPTIONS
-------

--page

  Web URI

--regexp=<expression>

  Optional expression to match against the page content.

EXAMPLE
-------

.. code:: bash

   $ msa-lookup --page https://www.google.de --regexp .*Google
