msa-init
========

SYNOPSIS
--------

.. code:: bash

   msa-init -h | --help
   msa-init
       [--init-db]
       [--verbose]

DESCRIPTION
-----------

For MSA to work correctly a kafka and a PostgreSQL service are required.

Make sure you have created the `topic-name` configured
in `~/.config/msa/kafka.yml` on the kafka admin console.

The MSA init process currently does not create the kafka topic.
For the database to work correctly an initial table layout is
required. The MSA init process creates this table layout and checks
the connectivity to all services.


OPTIONS
-------

--init-db

  Optional init the database. Note, this will drop the
  eventually existing table

--verbose

  Include log information from external modules

EXAMPLE
-------

.. code:: bash

   $ msa-init --init-db
