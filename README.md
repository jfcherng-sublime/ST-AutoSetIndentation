Sublime-AutoSetIndentation
==========================

This plugin automatically detects and sets the indentation for you, by default, when a file is loaded.

If you don't want to replace Sublime Text's `detect_indentation` with this plugin's,
set the plugin setting `hijack_st_detect_indentation` to `false`.


Why Do I Make This?
===================

Sublime Text detects the indentation when a file is loaded 
if `detect_indentation` is set to `true`, which is the default settings.

However, its detection is wrong sometimes.
You could give following cases a try!

- Files under the [problem_files/](https://github.com/jfcherng/Sublime-AutoSetIndentation/tree/master/problem_files)
- https://github.com/SublimeTextIssues/Core/issues/1459
- https://github.com/SublimeTextIssues/Core/issues/1640

I find that [Indent Finder](http://www.freehackers.org/Indent_Finder) detects 
above files correctly so I make it into this plugin.


Installation
============

This package is available on Package Control by the name of [AutoSetIndentation](https://packagecontrol.io/packages/AutoSetIndentation).


User Settings
=============

See [AutoSetIndentation.sublime-settings](https://github.com/jfcherng/Sublime-AutoSetIndentation/blob/master/AutoSetIndentation.sublime-settings).


Commands
========

You may disable all `event_listeners` in your user settings and add a key binding to auto set indentation.

```javascript
{ "keys": ["ctrl+alt+s", "ctrl+alt+i"], "command": "auto_set_indentation" },
```


Acknowledgment
==============

- [Indent Finder](http://www.freehackers.org/Indent_Finder)


Supporters <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ATXYY9Y78EQ3Y" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" /></a>
==========

Thank you guys for sending me some cups of coffee.
