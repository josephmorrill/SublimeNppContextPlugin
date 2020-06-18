# Joseph Morrill
# https://github.com/josephmorrill/SublimeNppTabContextPlugin
import sublime
import sublime_plugin
from Default.send2trash import send2trash
import os
import sys
import subprocess

class NpptcCloseTabsLeftCommand( sublime_plugin.WindowCommand ):
	def run( self, group = -1, index = -1 ):
		for i in range( 0, index + 1 ):
			self.window.run_command(
				"close_by_index", {
					"group" : group,
					"index" : 0
				}
			)
		
	def is_enabled( self, group = -1, index = -1 ):
		# Only show if there is a tab to the left (index will be 0 if tab is left-most tab)
		return ( index > 0 )

class NpptcPluginTextCommand( sublime_plugin.TextCommand ):
	def getTargetView( self, group, index ):
		result = self.view
		if group > -1 and index > -1:
			window = self.view.window()
			groupViews = window.views_in_group( group )
			result = groupViews[index]
		return result

	def getSetting( self, key ):
		settings = sublime.load_settings( "NppTabContext.sublime-settings" )
		return settings.get( key )

	def getOsSetting( self, key ):
		result = None

		settings = sublime.load_settings( "NppTabContext.sublime-settings" )
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

	def runExternalCommand( self, commandTemplate, targetFilePath, debug = False ):
		command = None
		useShell = False
		if "use_shell" in commandTemplate.keys():
			useShell = commandTemplate["use_shell"]

		replacements = {
			"filePath" : targetFilePath,
			"fileName" : os.path.basename( targetFilePath ),
			"dirPath" : os.path.dirname( targetFilePath )
		}

		if isinstance( commandTemplate["command"], list ):
			command = []
			for ( index, templateValue ) in enumerate( commandTemplate["command"] ):
				value = sublime.expand_variables( templateValue, replacements )
				print( value )
				command.append( value )
		else:
			command = "" + commandTemplate["command"]
			command = sublime.expand_variables( command, replacements )

		externalProcess = subprocess.Popen( command, shell = useShell )
		if debug:
			externalCommand = externalProcess.args
			if isinstance( externalCommand, list ):
				externalCommand = " ".join( externalCommand )
			print( "External command: " + externalCommand )

class NpptcRenameCommand( NpptcPluginTextCommand ):
	def run( self, edit, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		oldFilePath = targetView.file_name()
		if oldFilePath:
			targetView.window().run_command( "prompt_save_as", {
				"group" : group,
				"index" : index
			} )
			try:
				os.remove( oldFilePath )
			except:
				sublime.error_message( "Failed to delete old file (" + oldFilePath + ") - check Sublime console for error information" )

	def is_enabled( self, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		return ( targetView.file_name() is not None )

class NpptcDeleteCommand( NpptcPluginTextCommand ):
	def run( self, edit, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		targetFilePath = targetView.file_name()
		if targetFilePath:
			send2trash( targetFilePath )
			targetView.set_scratch( True )
			targetView.close()

	def is_enabled( self, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		return ( targetView.file_name() is not None )

class NpptcOpenContainingFolderFileExplorerCommand( NpptcPluginTextCommand ):
	def run( self, edit, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		targetFilePath = targetView.file_name()
		if targetFilePath:
			fileExplorerTemplate = self.getOsSetting( "file_explorer" )
			debug = self.getSetting( "debug" )
			self.runExternalCommand( fileExplorerTemplate, targetFilePath, debug = debug )

	def is_enabled( self, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		return ( targetView.file_name() is not None )

class NpptcOpenContainingFolderTerminalCommand( NpptcPluginTextCommand ):
	def run( self, edit, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		targetFilePath = targetView.file_name()
		if targetFilePath:
			terminalTemplate = self.getOsSetting( "terminal" )
			debug = self.getSetting( "debug" )
			self.runExternalCommand( terminalTemplate, targetFilePath, debug = debug )

	def is_enabled( self, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		return ( targetView.file_name() is not None )

class NpptcOpenDefaultViewerCommand( NpptcPluginTextCommand ):
	def run( self, edit, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		targetFilePath = targetView.file_name()
		if targetFilePath:
			if os.name == "nt":
				os.startfile( targetFilePath, "open" )
			elif sys.platform == "darwin":
				subprocess.check_call( [ "open", targetFilePath ] )
			else:
				subprocess.check_call( [ "xdg-open", targetFilePath ] )

	def is_enabled( self, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		return ( targetView.file_name() is not None )

class NpptcCopyFilePathCommand( NpptcPluginTextCommand ):
	def run( self, edit, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		targetFilePath = targetView.file_name()
		if targetFilePath:
			sublime.set_clipboard( targetFilePath )

	def is_enabled( self, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		return ( targetView.file_name() is not None )

class NpptcCopyFilenameCommand( NpptcPluginTextCommand ):
	def run( self, edit, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		targetFilePath = targetView.file_name()
		if targetFilePath:
			targetFilename = os.path.basename( targetFilePath )
			sublime.set_clipboard( targetFilename )

	def is_enabled( self, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		return ( targetView.file_name() is not None )

class NpptcCopyDirectoryPathCommand( NpptcPluginTextCommand ):
	def run( self, edit, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		targetFilePath = targetView.file_name()
		if targetFilePath:
			targetParentPath = os.path.dirname( targetFilePath )
			sublime.set_clipboard( targetParentPath )

	def is_enabled( self, group = -1, index = -1 ):
		targetView = self.getTargetView( group, index )
		return ( targetView.file_name() is not None )