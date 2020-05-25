import sublime
import sublime_plugin
from Default.send2trash import send2trash
import os
import sys
import subprocess

def plugin_loaded():
	# Check if CloseTabsLeft is installed
	closeTabsLeftInstalled = False
	for commandGroup in sublime_plugin.all_command_classes:
		for commandClass in commandGroup:
			if commandClass.__name__ == "CloseTabsLeftCommand":
				closeTabsLeftInstalled = True
				break;
		if closeTabsLeftInstalled:
			break;
	if not closeTabsLeftInstalled:
		sublime.status_message( "WARNING: CloseTabsLeft plugin is required for \"Close Tabs to the Left\" tab menu item to work" )

class NppcPluginTextCommand( sublime_plugin.TextCommand ):
	def getOsSetting( self, key ):
		result = None

		settings = sublime.load_settings( "SublimeNppContextPlugin.sublime-settings" )
		osName = os.name
		osPlatform = sys.platform

		result = settings.get( osName )
		if result is not None:
			result = result[osPlatform]
			if result is not None:
				result = result[key]
		
		if result is None:
			raise ValueError( "Settings not defined for " + osName + "/" + osPlatform + "/" + key )

		return result

	def runExternalCommand( self, commandTemplate, replacements = {} ):
		if isinstance( commandTemplate, list ):
			command = []
			for ( index, templateValue ) in enumerate( commandTemplate ):
				value = templateValue
				for replacement in replacements.keys():
					if replacement in value:
						value = value.replace( replacement, replacements[replacement] )
				command.append( value )
			subprocess.Popen( command, shell = False )
		else:
			command = "" + commandTemplate
			for replacement in replacements.keys():
				if replacement in command:
						command = command.replace( replacement, replacements[replacement] )
			subprocess.Popen( command, shell = False )


class NppcDeleteCommand( NppcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			send2trash( currentFilePath )
			self.view.set_scratch( True )
			self.window.focus_view( self.view )
			self.view.close()

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NppcOpenContainingFolderFileExplorerCommand( NppcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			currentDirectoryPath = os.path.dirname( currentFilePath )
			fileExplorerTemplate = self.getOsSetting( "file_explorer" )
			self.runExternalCommand( fileExplorerTemplate, {
				"<<PATH>>" : currentDirectoryPath
			} )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NppcOpenContainingFolderTerminalCommand( NppcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			currentDirectoryPath = os.path.dirname( currentFilePath )
			terminalTemplate = self.getOsSetting( "terminal" )
			self.runExternalCommand( terminalTemplate, {
				"<<PATH>>" : currentDirectoryPath
			} )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NppcOpenDefaultViewerCommand( NppcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			if os.name == "nt":
				os.startfile( currentFilePath, "open" )
			else:
				subprocess.check_call( [ "open", currentFilePath ] )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NppcCopyFilePathCommand( NppcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			sublime.set_clipboard( currentFilePath )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NppcCopyFilenameCommand( NppcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			currentFilename = os.path.basename( currentFilePath )
			sublime.set_clipboard( currentFilename )
		
	def is_enabled( self ):
		return ( self.view.file_name() is not None )

class NppcCopyDirectoryPathCommand( NppcPluginTextCommand ):
	def run( self, edit ):
		currentFilePath = self.view.file_name()
		if currentFilePath:
			currentDirectoryPath = os.path.dirname( currentFilePath )
			sublime.set_clipboard( currentDirectoryPath )

	def is_enabled( self ):
		return ( self.view.file_name() is not None )