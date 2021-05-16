buildroot = /
python_version = 3
python_lookup_name = python$(python_version)
python = $(shell which $(python_lookup_name))
docdir = /usr/share/doc/packages

version := $(shell \
	$(python) -c \
	'from msa.version import __version__; print(__version__)'\
)

tox:
	tox

install:
	# install plugin manual page and license/readme
	# NOTE: this file is not handled through pip because on system level
	install -d -m 755 ${buildroot}usr/share/man/man8
	gzip -f doc/build/man/8/msa::init.8
	install -m 644 doc/build/man/8/msa::init.8.gz \
		${buildroot}usr/share/man/man8
	gzip -f doc/build/man/8/msa::lookup.8
	install -m 644 doc/build/man/8/msa::lookup.8.gz \
		${buildroot}usr/share/man/man8
	gzip -f doc/build/man/8/msa::store.8
	install -m 644 doc/build/man/8/msa::store.8.gz \
		${buildroot}usr/share/man/man8
	install -d -m 755 ${buildroot}${docdir}/python-msa
	install -m 644 LICENSE \
		${buildroot}${docdir}/python-msa/LICENSE
	install -m 644 README.rst \
		${buildroot}${docdir}/python-msa/README

build: clean tox
	# create setup.py variant for rpm build.
	# delete module versions from setup.py for building an rpm
	# the dependencies to the python module rpm packages is
	# managed in the spec file
	sed -ie "s@>=[0-9.]*'@'@g" setup.py
	sed -ie "s@psycopg2-binary@psycopg2@g" setup.py
	# build the sdist source tarball
	$(python) setup.py sdist
	# restore original setup.py backed up from sed
	mv setup.pye setup.py
	# provide rpm source tarball
	mv dist/msa-${version}.tar.gz \
		dist/python-msa.tar.gz
	# update rpm changelog using reference file
	helper/update_changelog.py \
		--since package/python-msa.changes \
	> dist/python-msa.changes
	helper/update_changelog.py \
		--file package/python-msa.changes \
	>> dist/python-msa.changes
	# update package version in spec file
	cat package/python-msa-spec-template |\
		sed -e s'@%%VERSION@${version}@' \
	> dist/python-msa.spec
	# provide rpm rpmlintrc
	cp package/python-msa-rpmlintrc dist

clean:
	$(python) setup.py clean
	rm -rf doc/build
	rm -rf dist/*
