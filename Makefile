# KeyParaStocX Makefile
#
# Copyright (C) 2023-2024 Bogdan 'bogdro' Drozdowski, bogdro (at) users . sourceforge . net
#
# This file is part of KeyParaStocX (Keyword-based Paragraph Styling and
#  Table of Contents eXtension), an OpenOffice / LibreOffice extension that
#  searches for the configured keywords in a text, changes their style and
#  builds a Table of Contents for them.
#
# Project homepage: https://keyparastocx.sourceforge.io/
#
# This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

NAME = KeyParaStocX
IDENTIFIER = vnd.bogdandrozdowski.keyparastocx
VER = 1.0.1

RMDIR = /bin/rm -fr
# when using '-p', no error is generated when the directory exists
MKDIR = /bin/mkdir -p
COPY = /bin/cp -pRf
SED = /bin/sed
SED_OPTS = -i
GREP = /bin/grep
AWK = /usr/bin/awk

PYTHON = /usr/bin/python
PYTEST = /usr/bin/pytest

# Use the GNU tar format
# ifneq ($(shell tar --version | grep -i bsd),)
# PACK1_GNUOPTS = --format gnutar
# endif
PACK1 = /bin/tar $(PACK1_GNUOPTS) -vcf
PACK1_EXT = .tar

PACK2 = /usr/bin/gzip -9 -f
PACK2_EXT = .gz

OFFICE_PACK = zip -r -9
OFFICE_PACK_EXT = .oxt

ifeq ($(OFFICEDIR),)
OFFICEDIR = /opt/openoffice
endif

UNOPKG = $(OFFICEDIR)/program/unopkg

EXTENSION_FILES = $(NAME) Addons.xcu components description.xml icons \
	KeyParaStocX-dialog META-INF Office pkg-desc registration COPYING
DIST_FILES = $(EXTENSION_FILES) AUTHORS ChangeLog INSTALL Makefile NEWS \
	README test
TESTS = test/test_load.py

TMP_CFG_FILE = KeyParaStocX-dialog/config-data-tmp.xcu
SUBST_VERSION = $(SED) $(SED_OPTS) "s/@@VERSION@@/$(VER)/g"
SUBST_ID = $(SED) $(SED_OPTS) "s/@@IDENTIFIER@@/$(IDENTIFIER)/g"

all:	dist

dist:	dist-bin dist-src

dist-bin: $(NAME)-$(VER)$(OFFICE_PACK_EXT)

$(NAME)-$(VER)$(OFFICE_PACK_EXT): $(shell find $(EXTENSION_FILES) -type f) \
		Makefile
	$(RMDIR) $(NAME)-$(VER) $(NAME)-$(VER)$(OFFICE_PACK_EXT)
	$(MKDIR) $(NAME)-$(VER)
	$(COPY) $(EXTENSION_FILES) $(NAME)-$(VER)
	find $(NAME)-$(VER) -name .gitignore -exec $(RMDIR) '{}' \;
	find $(NAME)-$(VER) -type f -exec $(SUBST_VERSION) '{}' \;
	find $(NAME)-$(VER) -type f -exec $(SUBST_ID) '{}' \;
	$(COPY) KeyParaStocX-dialog/config-data.xcu $(TMP_CFG_FILE)
	$(SED) $(SED_OPTS) 's/$$/\\/' $(TMP_CFG_FILE)
	$(SED) $(SED_OPTS) '/p.Parse(/ r $(TMP_CFG_FILE)' $(NAME)-$(VER)/components/Config.py
	$(RMDIR) $(TMP_CFG_FILE)
	cd $(NAME)-$(VER) && $(OFFICE_PACK) ../$(NAME)-$(VER)$(OFFICE_PACK_EXT) .
	$(RMDIR) $(NAME)-$(VER)

dist-src: $(NAME)-$(VER)$(PACK1_EXT)$(PACK2_EXT)

$(NAME)-$(VER)$(PACK1_EXT)$(PACK2_EXT): $(shell find $(DIST_FILES) -type f) \
		Makefile
	$(RMDIR) $(NAME)-$(VER) $(NAME)-$(VER)$(PACK1_EXT)$(PACK2_EXT)
	$(MKDIR) $(NAME)-$(VER)
	$(COPY) $(DIST_FILES) $(NAME)-$(VER)
	find $(NAME)-$(VER) -name .gitignore -exec $(RMDIR) '{}' \;
	$(PACK1) $(NAME)-$(VER)$(PACK1_EXT) $(NAME)-$(VER)
	$(PACK2) $(NAME)-$(VER)$(PACK1_EXT)
	$(RMDIR) $(NAME)-$(VER)

install: $(NAME)-$(VER)$(OFFICE_PACK_EXT)
	$(UNOPKG) add $(NAME)-$(VER)$(OFFICE_PACK_EXT)

check:
	PYTHONPATH=`$(PYTHON) -m sysconfig | $(GREP) purelib | $(AWK) '{print $$3}' | $(SED) 's/"//g'`:. \
		$(OFFICEDIR)/program/python $(PYTEST) $(TESTS)

uninstall:
	$(UNOPKG) remove $(IDENTIFIER)

verify-install:
	$(UNOPKG) list $(IDENTIFIER)

.PHONY: all check dist dist-bin dist-src install uninstall verify-install
