# Notepad++ Tab Context Plugin
A Sublime Text 3 plugin that adds some useful commands from Notepad++:

Added to tab context menu:
- Close Tabs to the Left
- Save
- Save As...
- Rename
- Delete
- Open containing folder in file explorer
- Open containing folder in terminal
- Open in default viewer
- Copy file path
- Copy filename
- Copy directory path

Added to command palette:
- Open containing folder in file explorer
- Open containing folder in terminal
- Open in default viewer

# Settings
Depending on your setup, you may need to tweak the commands in the plugin settings to match your system's file explorer and terminal executables (especially on Linux systems).

To edit the commands, go to **Preferences** > **Package Settings** > **Notepad++ Tab Context**. If the command doesn't do anything and doesn't report an error in the Sublime console, you may need to add a "use_shell" key to the command object and set it to **True**.

You can also set the "debug" setting to true to see the executed commands in the console.

# License
This project is supplied under the GNUv3 license, which can be found in the [LICENSE] file.
