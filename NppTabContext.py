import sublime
import sublime_plugin
from Default.send2trash import send2trash
import os
import sys
import subprocess

class NpptcCloseTabsLeftCommand( sublime_plugin.WindowCommand ):
	""" The NpptcCloseTabsLeftCommand class is licensed under the MIT License
	and is derived from the ST2 CloseTabsLeft plugin by deXterbed
	(https://github.com/deXterbed/CloseTabsLeft/blob/master/LICENSE). The license is as follows:
	The MIT License (MIT)

	Copyright (c) 2015 Manoj Mishra

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE."""
	def run( self ):
		currentView = self.window.active_view()
		for view in self.window.views():
			if view.id() == currentView.id():
				break
			view.close()

class NpptcPluginTextCommand( sublime_plugin.TextCommand ):
	def getSetting( self, key ):
		settings = sublime.load_settings( "NppTabContext.sublime-settings" )
		return settings.get( key )

	def getOsSetting( self, key ):
		result = None

		settings = sublime.load_settings( "NppTabContext.sublime-settings" )
		osName = os.name
		osPlatform = sys.platform
		if osPlatform.startswith( "linux" ):
			osPlatform = "linux"
		elif osPlatform == "darwin":
			osPlatform = "mac"
		elif osName == "nt":
			osPlatform = "windows"

		result = settings.get( osPlatform )
		if result is not None:
			result = result[key]
		
		if result is None:
			raise ValueError( "Settings not defined for " + osPlatform + "/" + key )

		return result

	def runExternalCommand( self, commandTemplate, replacements = {}, debug = False ):
		command = None
		useShell = False
		if "use_shell" in commandTemplate.keys():
			useShell = commandTemplate["use_shell"]

		if isinstance( commandTemplate["command"], list ):
			command = []
			for ( index, templateValue ) in enumerate( commandTemplate["command"] ):
				value = templateValue
				for replacement in replacements.keys():
					if replacement in value:
						value = value.replace( replacement, replacements[replacement] )
				command.append( value )
		else:
			command = "" + commandTemplate["command"]
			for replacement in replacements.keys():
				if replacement in command:
						command = command.replace( replacement, replacements[replacement] )

		externalProcess = subprocess.Popen( command, shell = useShell )
		if debug:
			externalCommand = externalProcess.args
			if isinstance( externalCommand, list ):
				externalCommand = " ".join( externalCommand )
			print( "External command: " + externalCommand )

	def buildReplacements( self, filePath ):
		result = {}

		result["<<FILE_PATH>>"] = filePath
		result["<<FILE_NAME>>"] = os.path.basename( filePath )
		result["<<DIR_PATH>>"] = os.path.dirname( filePath )

		return result


class NpptcDeleteCommand( NpptcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			send2trash( currentFilePath )
			self.view.set_scratch( True )
			self.view.close()

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NpptcOpenContainingFolderFileExplorerCommand( NpptcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			currentDirectoryPath = os.path.dirname( currentFilePath )
			fileExplorerTemplate = self.getOsSetting( "file_explorer" )
			debug = self.getSetting( "debug" )
			self.runExternalCommand( fileExplorerTemplate, self.buildReplacements( currentFilePath ), debug = debug )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NpptcOpenContainingFolderTerminalCommand( NpptcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			terminalTemplate = self.getOsSetting( "terminal" )
			debug = self.getSetting( "debug" )
			self.runExternalCommand( terminalTemplate, self.buildReplacements( currentFilePath ), debug = debug )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NpptcOpenDefaultViewerCommand( NpptcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			if os.name == "nt":
				os.startfile( currentFilePath, "open" )
			elif sys.platform == "darwin":
				subprocess.check_call( [ "open", currentFilePath ] )
			else:
				subprocess.check_call( [ "xdg-open", currentFilePath ] )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NpptcCopyFilePathCommand( NpptcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			sublime.set_clipboard( currentFilePath )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NpptcCopyFilenameCommand( NpptcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			currentFilename = os.path.basename( currentFilePath )
			sublime.set_clipboard( currentFilename )
		
	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NpptcCopyDirectoryPathCommand( NpptcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			currentDirectoryPath = os.path.dirname( currentFilePath )
			sublime.set_clipboard( currentDirectoryPath )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )