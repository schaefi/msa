msa-store
=========

SYNOPSIS
--------

.. code:: bash

   msa-store -h | --help
   msa-store
       [--update-interval=<time_sec>]
       [--single-shot]
   msa-store --dump-db

DESCRIPTION
-----------

The MSA store tool reads from the kafka message broker and
stores the information in a PostgreSQL database. It is expected
that the stored information in kafka is the result
of `msa-lookup` calls. Messages which are malformatted will
not be stored in the database.

OPTIONS
-------

--dump-db

  Print the database

--update-interval=<time_sec>

  Optional update interval to check for messages and
  writing into the database. Default is 30sec

--single-shot

  Optionally run once, read present messages and store them
  in the database.

EXAMPLE
-------

.. code:: bash

   $ msa-store --single-shot
   $ msa-store --dump-db
