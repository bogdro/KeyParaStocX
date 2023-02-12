# KeyParaStocX Makefile
#
# Copyright (C) 2023 Bogdan 'bogdro' Drozdowski, bogdro (at) users . sourceforge . net
#
# This file is part of KeyParaStocX (Keyword-based Paragraph Styling and
#  Table of Contents eXtension), an OpenOffice / LibreOffice extension that
#  searches for typical parts of old-style Polish legal acts and builds a
#  Table of Contents for them.
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
VER = 0.7.0

RMDIR = /bin/rm -fr
# when using '-p', no error is generated when the directory exists
MKDIR = /bin/mkdir -p
COPY = /bin/cp -pRf

# Use the GNU tar format
# ifneq ($(shell tar --version | grep -i bsd),)
# PACK1_GNUOPTS = --format gnutar
# endif
PACK1 = /bin/tar $(PACK1_GNUOPTS) -vcf
PACK1_EXT = .tar

PACK2 = /usr/bin/gzip -9
PACK2_EXT = .gz

OFFICE_PACK = zip -r -9
OFFICE_PACK_EXT = .oxt

ifeq ($(OFFICEDIR),)
OFFICEDIR = /opt/openoffice
endif

UNOPKG = $(OFFICEDIR)/program/unopkg

EXTENSION_FILES = $(NAME) Addons.xcu description.xml icons META-INF \
	Office pkg-desc registration COPYING
DIST_FILES = $(EXTENSION_FILES) AUTHORS ChangeLog INSTALL NEWS README

SUBST_VERSION = /bin/sed -i "s/@@VERSION@@/$(VER)/g"

all:	dist

dist:	dist-bin dist-src

dist-bin: $(NAME)-$(VER)$(OFFICE_PACK_EXT)

$(NAME)-$(VER)$(OFFICE_PACK_EXT): $(shell find $(EXTENSION_FILES) -type f) \
		Makefile
	$(RMDIR) $(NAME)-$(VER) $(NAME)-$(VER)$(OFFICE_PACK_EXT)
	$(MKDIR) $(NAME)-$(VER)
	$(COPY) $(EXTENSION_FILES) $(NAME)-$(VER)
	find $(NAME)-$(VER) -type f -exec $(SUBST_VERSION) '{}' \;
	find $(NAME)-$(VER) -name .gitignore -exec $(RMDIR) '{}' \;
	cd $(NAME)-$(VER) && $(OFFICE_PACK) ../$(NAME)-$(VER)$(OFFICE_PACK_EXT) .
	$(RMDIR) $(NAME)-$(VER)

dist-src: $(NAME)-$(VER)$(PACK1_EXT)$(PACK2_EXT)

$(NAME)-$(VER)$(PACK1_EXT)$(PACK2_EXT): $(shell find $(DIST_FILES) -type f) \
		Makefile
	$(RMDIR) $(NAME)-$(VER)
	$(MKDIR) $(NAME)-$(VER)
	$(COPY) $(DIST_FILES) $(NAME)-$(VER)
	find $(NAME)-$(VER) -name .gitignore -exec $(RMDIR) '{}' \;
	$(PACK1) $(NAME)-$(VER)$(PACK1_EXT) $(NAME)-$(VER)
	$(PACK2) $(NAME)-$(VER)$(PACK1_EXT)
	$(RMDIR) $(NAME)-$(VER)

install: $(NAME)-$(VER)$(OFFICE_PACK_EXT)
	$(UNOPKG) add $(NAME)-$(VER)$(OFFICE_PACK_EXT)

uninstall:
	$(UNOPKG) remove $(IDENTIFIER)

verify-install:
	$(UNOPKG) list $(IDENTIFIER)

.PHONY: all dist dist-bin dist-src install uninstall verify-install