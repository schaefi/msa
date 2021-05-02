MSA - Web Check
===============

.. |GitHub CI Action| image:: https://github.com/schaefi/msa/workflows/CILint/badge.svg
   :target: https://github.com/schaefi/msa/actions

|GitHub CI Action|

Web Check, monitor page metrics.

MSA consists out of the following tools:

`msa-init`
  Initialize the toolchain. `msa-init` is expected to be called once
  and checks for the availability of the required kafka and
  PostgreSQL database services, as well as creates the initial
  table layout in the database.

`msa-lookup`
  A tool to fetch request metrics from a web page. The collected
  information contains; The page URL, date, response time, status code
  and an optional information on the match result of a regexp applied
  to the request content. The data is stored as a message to the kafka
  service. `msa-lookup` is expected to be called often and for
  different locations.
 
`msa-store`
  A tool to read the messages from the kafka service. Only information
  which is valid against the MSA transport protocol will be taken
  into account. Valid information is stored in the PostgreSQL database.
  `msa-store` is expected to be called as a service through systemd
  but can also be used in single shot mode.

Installation
------------

MSA is provided as packages from here:

* https://build.opensuse.org/package/show/home:sax2/python-msa

Please choose the OS of your choice and install the package.
For the SUSE OS and with Leap 15.2 this can be done as follows:


.. code:: shell-session

   $ sudo zypper ar https://download.opensuse.org/repositories/home:/sax2/openSUSE_Leap_15.2/
   $ sudo zypper in python3-msa


Setup Service Configurations
----------------------------

MSA utilizes kafka and PostgreSQL services. Therefore two config
files including the access credentials to these services needs
to be created as follows:

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

Check and Initialize Services
-----------------------------

For MSA to work correctly kafka and PostgreSQL services are required.

Before calling the `msa-init` setup, check on the following pre conditions:

1. Start a kafka service
2. Start a PostgreSQL service
3. Make sure you have created the `topic-name` configured
   in `~/.config/msa/kafka.yml` on the kafka admin console.

The MSA init process currently does not create the services and the
kafka topic. Thus the above steps MUST be done manually.

For the database to work correctly an initial table layout is required.
The MSA init process creates this table layout and also checks the
connectivity to all services with the following call:

.. code:: shell-session

   $ msa-init --init-db

.. note::

   Calling msa-init with --init-db creates a table named webcheck
   and will drop that table prior creating a new one !

Start Web Checker(s)
--------------------

The most simple way to add web checkers is via the users
crontab. This can be done as follows:

.. code:: shell-session

   $ crontab -e

   * * * * * msa-lookup --page https://www.google.de

Will run a web check for Google every minute. Add more
checkers as you see fit

Start Database Store
--------------------

The collection of web checkers through `msa-lookup` causes the
creation of a collection of messages in the kafka service. With
the `msa-store` utility those messages can be stored in the
PostgreSQL database. To start the service call

.. code:: shell-session

   $ systemctl --user start msa-store

As messages are arriving in the database you can dump its
contents with:

.. code:: shell-session

   $ msa-store --dump-db

Run from Source
---------------

To prepare the system to run from a virtual python
environment, follow these steps:

.. code:: shell-session

   $ cd ~/
   $ git clone https://github.com/schaefi/msa.git
   $ pip install tox
   $ tox

.. note:: Calling from Python Venv

   Calling python code from within a virtual environment
   requires this environment be active in the calling
   console session. For this purpose a simple helper
   programm named `run` exists. Thus if you plan to
   work from source please always call the tools through
   the run helper like in the following example:

   .. code:: shell-session

      $HOME/msa/run msa-init
