MSA - Web Check
===============

.. |GitHub CI Action| image:: https://github.com/schaefi/msa/workflows/CILint/badge.svg
   :target: https://github.com/schaefi/msa/actions

|GitHub CI Action|

Web Check, monitor page metrics


Prepare from Source
-------------------

To prepare the system to run from a virtual python
environment, follow these steps:

.. code:: shell-session

   $ cd ~/
   $ git clone https://github.com/schaefi/msa.git
   $ pip install tox
   $ tox


Setup Service Configurations
----------------------------

MSA sends metrics to a kafka message broker and stores this
information in a￼PostgreSQL database. Therefore two config
files including the access credentials to these services needs
to be created as follows

.. code:: shell-session

   $ mkdir ~/.config/msa
   
For accessing the database create:

.. code:: shell-session

   $ vi ~/.config/msa/db.yml

.. code:: yaml

   db_uri: "postgres://..."

For accessing the kafka service create:

.. code:: shell-session

   $ vi ~/.config/msa/kafka.yml

.. code:: yaml

   host: server-name:port
   topic: topic-name
   ssl_cafile: ca.pem
   ssl_certfile: service.cert
   ssl_keyfile: service.key

.. note::

   Please checkout your service provider console to fetch
   the needed access credentials


Start Web Checker(s)
--------------------

The most simple way to add web checkers is via the users
crontab. This can be done as follows:

.. code:: shell-session

   $ crontab -e

   */5 * * * * $HOME/msa/run msa-lookup --page https://www.google.de

Will run a web check for Google every 5 minutes. Add more
checkers as you see fit

Start Database Store
--------------------

TODO
