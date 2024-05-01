#!/opt/libreoffice/program/python
#
# KeyParaStocX - the module unit test
#
# Copyright (C) 2024 Bogdan 'bogdro' Drozdowski, bogdro (at) users . sourceforge . net
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

import os
import pytest
import time
import uno

from components.Config import *

def test_load():
	pidfile_name = 'office.pid'
	# Start the office suite in the background:
	os.system("/opt/libreoffice/program/soffice '--accept=socket,host=127.0.0.1,port=2345;urp;' --nologo --invisible --headless --pidfile="
		+ pidfile_name + " --writer &")
	localContext = uno.getComponentContext()
	resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext)
	ctx = None

	# Wait until the office suite starts and is connected:
	while ctx is None:
		try:
			ctx = resolver.resolve(
				'uno:socket,host=127.0.0.1,port=2345;urp;StarOffice.ComponentContext')
			time.sleep(1)
		except:
			pass

	k = KeyParaStocXConfig(ctx)
	k.loadData()

	print('k.configuration: ' + str(k.configuration))
	print('k.def_cfg: ' + str(k.def_cfg))
	print('default_configuration: ' + str(default_configuration))

	assert str(k.def_cfg['head1']['key']['en-US']) == 'Part'
	assert str(k.def_cfg['head2']['key']['en-US']) == 'Book'
	assert str(k.def_cfg['head3']['key']['en-US']) == 'Title'
	assert str(k.def_cfg['head4']['key']['en-US']) == 'Section'
	assert str(k.def_cfg['head5']['key']['en-US']) == 'Chapter'
	assert str(k.def_cfg['head6']['key']['en-US']) == 'Subchapter'
	assert str(k.def_cfg['head7']['key']['en-US']) == 'Art\\.'
	for n in range(1, 8):
		assert str(k.def_cfg['head' + str(n)]['style']['en-US']) == 'Heading ' + str(n)

	# Stop the office suite:
	if os.path.exists(pidfile_name):
		os.system("cat " + pidfile_name + " | xargs kill -2")
	else:
		os.system("ps -Af | /bin/grep -i soffice | /bin/grep headless | /bin/grep -v grep | awk '{print $2}' | xargs kill -2")
