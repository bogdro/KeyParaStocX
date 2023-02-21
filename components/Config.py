#!/opt/libreoffice/program/python
#
# KeyParaStocX - the configuration dialog module handler
#
# Copyright (C) 2023 Bogdan 'bogdro' Drozdowski, bogdro (at) users . sourceforge . net
#
# This file is part of KeyParaStocX (Keyword-based Paragraph Styling and
#  Table of Contents eXtension), an OpenOffice / LibreOffice extension that
#  searches for the configured keywords in a text, changes their style and
#  builds a Table of Contents for them.
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

# Due to https://www.openoffice.org/udk/basic/ saying that components
# cannot be written in Basic, this is in Python.

import uuid

# https://wiki.openoffice.org/wiki/Python/Transfer_from_Basic_to_Python
import uno
import unohelper

# https://wiki.documentfoundation.org/Documentation/DevGuide/Extensions#Creating_the_GUI_of_the_Options_Page
from com.sun.star.awt import XContainerWindowEventHandler
from com.sun.star.container import XNameAccess

# https://wiki.openoffice.org/wiki/Documentation/DevGuide/WritingUNO/Core_Interfaces_to_Implement:
from com.sun.star.lang import XServiceInfo, XServiceName, XTypeProvider
from com.sun.star.uno import XInterface

# Doesn't work with XTypeProvider - perhaps wrong data/data types.
# Just stops after getTypes(). Fortunately, unohelper.Base provides this.
#class KeyParaStocXConfig(unohelper.Base, XContainerWindowEventHandler, XServiceInfo, XServiceName, XTypeProvider, XInterface):
class KeyParaStocXConfig(unohelper.Base, XContainerWindowEventHandler, XServiceInfo, XServiceName, XNameAccess):#, XInterface):

	def __init__ (self, ctx):
		self.ctx = ctx
		self.types = [
			XContainerWindowEventHandler,
			XServiceInfo,
			XServiceName,
			#XTypeProvider,
			XNameAccess,
			XInterface,
			]
		self.uniqid = uuid.uuid4().bytes;
		self.name = '@@IDENTIFIER@@.KeyParaStocXConfig'
		self.serviceNames = [
			'com.sun.star.comp.extensionoptions.OptionsEventHandler',
			'@@IDENTIFIER@@.KeyParaStocXConfig'
			]
		self.event_method_name = 'external_event'
		self.configuration = {}
		self.cfg_provider = ctx.ServiceManager.createInstanceWithContext(
			'com.sun.star.configuration.ConfigurationProvider', ctx)
		self.cfg_property = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
		self.cfg_property.Name = 'nodepath'
		self.cfg_property.Handle = 0
		#self.cfg_property.State = uno.getConstantByName('com.sun.star.beans.PropertyState.DIRECT_VALUE')
		self.cfg_property.State = uno.Enum('com.sun.star.beans.PropertyState', 'DIRECT_VALUE')
		# config-schema.xcs:
		self.cfg_property.Value = '/@@IDENTIFIER@@.options.KeyParaStocX/Headers'
		self.cfg_elems = ('head1', 'head2', 'head3', 'head4', 'head5', 'head6', 'head7')
		self.cfg_access = self.cfg_provider.createInstanceWithArguments(
			'com.sun.star.configuration.ConfigurationUpdateAccess', (self.cfg_property,))

	# ------------------- XContainerWindowEventHandler:
	def callHandlerMethod(self, xWindow, eventObject, methodName):
		if methodName == self.event_method_name:
			try:
				return self.handleExternalEvent(xWindow, eventObject);
			except Exception as ex:
				pass
		return False

	def getSupportedMethodNames(self):
		return (self.event_method_name, )

	# ------------------- XServiceInfo:
	def getImplementationName(self):
		return self.name

	def supportsService(self, svcName):
		return svcName in self.serviceNames

	def getSupportedServiceNames(self):
		return self.serviceNames

	# ------------------- XServiceName:
	def getServiceName(self):
		return self.name

	# ------------------- XTypeProvider:
	# Doesn't work with XTypeProvider - perhaps wrong data/data types.
	# Just stops after getTypes(). Fortunately, unohelper.Base provides this.
	#def getTypes(self):
		#ret = []
		#for t in super().getTypes():
			#ret.append(t)
		#ret.append(self)#uno.getTypeByName('KeyParaStocXConfig'))
		#return ret
		##return self.types

	#def getImplementationId(self):
		#return self.uniqid

	# ------------------- XNameAccess:
	def getByName (self, aName):
		self.loadData()
		parts = aName.split('/')
		group = parts[0]
		key = parts[1]
		return self.get_config(group, key)

	def getElementNames (self):
		self.loadData()
		ret = []
		for n in self.configuration:
			for k in self.configuration[n]:
				ret.append(n + '/' + k)
		return ret;

	def hasByName (self, aName):
		self.loadData()
		parts = aName.split('/')
		group = parts[0]
		key = parts[1]
		if group in self.configuration:
			return key in self.configuration[group]
		return False

	# ------------------- XInterface:
	#def queryInterface(self, aType):
		#if (
			   #aType == XInterface
			#or aType == XTypeProvider
			#or aType == XServiceName
			#or aType == XServiceInfo
			#or aType == XContainerWindowEventHandler
			#or aType == @@IDENTIFIER@@.KeyParaStocXConfig):
			#return (self)
		#return ()
	#def acquire(self):
		#pass
	#def release(self):
		#pass

	# -------------------
	def handleExternalEvent (self, xWindow, eventObject):
		methodName = str(eventObject).lower()
		if methodName == 'ok':
			# save data:
			if xWindow is None or xWindow.Model.Name is None:
				return False;	# work only from the GUI
			for n in self.cfg_elems:
				cfg_leaf = self.cfg_access.getByName(n)
				cfg_leaf.setPropertyValue('key', xWindow.getControl(n + '_key').getText())
				cfg_leaf.setPropertyValue('style', xWindow.getControl(n + '_style').getText())
				if xWindow.getControl(n + '_key_alt'):
					cfg_leaf.setPropertyValue('key_alt', xWindow.getControl(n + '_key_alt').getText())
				self.cfg_access.commitChanges();
		elif methodName == 'back' or methodName == 'initialize':
			# load data
			self.loadData()
			# store into controls, if any
			if xWindow and xWindow.Model.Name:
				for n in self.cfg_elems:
					if self.configuration[n]['key'] is not None:
						xWindow.getControl(n + '_key').setText(self.configuration[n]['key'])
					if self.configuration[n]['style'] is not None:
						xWindow.getControl(n + '_style').setText(self.configuration[n]['style'])
					if self.configuration[n]['key_alt'] is not None and xWindow.getControl(n + '_key_alt'):
						xWindow.getControl(n + '_key_alt').setText(self.configuration[n]['key_alt'])
		return True

	def loadData(self):
		# set an internal variable, allow access from Basic
		self.configuration = {}
		for n in self.cfg_elems:
			prop = self.cfg_access.getPropertyValue(n)
			values = {}
			values['key'] = prop.getPropertyValue('key')
			values['style'] = prop.getPropertyValue('style')
			values['key_alt'] = prop.getPropertyValue('key_alt')
			self.configuration[n] = values

	def get_config(self, group, key):
		return self.configuration[group][key]

# ------------------- Component registration:

# https://wiki.openoffice.org/wiki/UNO_component_packaging
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(KeyParaStocXConfig,
	'@@IDENTIFIER@@.KeyParaStocXConfig',
	('@@IDENTIFIER@@.KeyParaStocXConfig',),
)

# ------------------- Testing:
# https://wiki.openoffice.org/wiki/UNO_component_packaging
if __name__ == '__main__':
	import os
	import time

	# start the office process:
	os.system ("/opt/libreoffice/program/soffice '-accept=socket,host=127.0.0.1,port=2345;urp;' -writer &")

	# Get the local context:
	lctx = uno.getComponentContext ()
	resolver = lctx.ServiceManager.createInstanceWithContext(
		'com.sun.star.bridge.UnoUrlResolver', lctx)

	ctx = None

	# Wait until the office starts and is connected:
	while ctx is None:
		try:
			ctx = resolver.resolve(
				'uno:socket,host=127.0.0.1,port=2345;urp;StarOffice.ComponentContext')
			time.sleep(1)
		except:
			pass

	k = KeyParaStocXConfig (ctx)
	k.loadData()
	for n in ('head1', 'head2', 'head3', 'head4', 'head5', 'head6', 'head7'):
		print('key: "' + str(k.configuration[n]['key']) + '"')
		print('style: "' + str(k.configuration[n]['style']) + '"')
		if 'key_alt' in k.configuration[n]:
			print('key_alt: "' + str(k.configuration[n]['key_alt']) + '"')
	k.handleExternalEvent(None, 'ok')
	#print (k.configuration)
