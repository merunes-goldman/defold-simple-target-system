# Defold Simple Target System

## Installation
You can use **dsts** in your own project by adding this project as a [Defold library dependency](https://defold.com/manuals/libraries). Open your _game.project_ file and in the dependencies field under project add:

https://github.com/nevolin-dmitry-leonid/defold-simple-target-system/archive/refs/heads/master.zip

Or point to the ZIP file of a specific release.

## Requirements
- python 3.8+
- python3 alias in $PATH

## Editor Script
This library provides simple way to manage _game.project_ presets (targets), see _example_.

(optional) Inheritance is supported: file must start with a comment `;relative/path/to/parent.target` (extension does not matter).
It's recommended to use _.base_target_ extension for intermediate (potentially non-valid) targets.

**ATTENTION:** It's recommended to commit all your changes before running these commands.

#### Select Target
Context menu item, available for _*.target_ files, builds and replaces current _game.project_.
