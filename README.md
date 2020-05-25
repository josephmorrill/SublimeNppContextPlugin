# SublimeNppContextPlugin
A Sublime Text 3 plugin that adds some useful tab context menu commands from Notepad++:

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

# Settings
Depending on your setup, you may need to tweak the commands in the plugin settings to match your system's file explorer and terminal executables (especially on Linux systems). **Note:** Plugin has not yet been tested on Mac OS X.

To edit the commands, go to **Preferences** > **Package Settings** > **Notepad++ Context** > **Settings - User**. If the command doesn't do anything and doesn't report an error in the Sublime console, you may need to add a "use_shell" key to the command object and set it to **True**.

# License
"Close Tabs to the Left" command based on [CloseTabsLeft](https://github.com/deXterbed/CloseTabsLeft) plugin by deXterbed, which is licensed under the MIT license. A copy of this license can be found in [SublimeNppContextPlugin.py] file in the **NppcCloseTabsLeftCommand** class.

All other commands / classes / files fall under the GNUv3 license, which can be found in the [LICENSE] file.