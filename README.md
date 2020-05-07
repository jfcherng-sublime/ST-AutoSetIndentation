# ST-AutoSetIndentation

[![Travis (.org) branch](https://img.shields.io/travis/jfcherng-sublime/ST-AutoSetIndentation/master?style=flat-square)](https://travis-ci.org/jfcherng-sublime/ST-AutoSetIndentation)
[![Package Control](https://img.shields.io/packagecontrol/dt/AutoSetIndentation?style=flat-square)](https://packagecontrol.io/packages/AutoSetIndentation)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/jfcherng-sublime/ST-AutoSetIndentation?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-AutoSetIndentation/tags)
[![Project license](https://img.shields.io/github/license/jfcherng-sublime/ST-AutoSetIndentation?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-AutoSetIndentation/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jfcherng-sublime/ST-AutoSetIndentation?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-AutoSetIndentation/stargazers)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal)](https://www.paypal.me/jfcherng/5usd)

This Sublime Text 3 plugin automatically detects and sets the indentation for you, by default, when a file is loaded.

## Important Notice

Since ST 4050, the `detect_indentation` command has done quite a great job so you probably no longer needs this plugin.

## Why Do I Make This

Sublime Text detects the indentation when a file is loaded
if `detect_indentation` is set to `true`, which is the default settings.

However, its detection is wrong sometimes.
You could give following cases a try!

- Files under the [problem_files/](https://github.com/jfcherng-sublime/ST-AutoSetIndentation/tree/master/problem_files)
- https://forum.sublimetext.com/t/detect-indentation-with-3-spaces-is-broken/45143
- https://github.com/SublimeTextIssues/Core/issues/1459
- https://github.com/SublimeTextIssues/Core/issues/1640

I find that [Indent Finder](http://www.freehackers.org/Indent_Finder) detects
above files correctly so I make it into this plugin.

## Notes

- Abbreviations

  - ST = Sublime Text
  - ASI = AutoSetIndentation (this plugin)

- ASI respects indentation settings from `.editorconfig` files.

- If you don't want to replace ST's `detect_indentation` command with ASI's,
  set the plugin setting `hijack_st_detect_indentation` to `false`.

- Even if `hijack_st_detect_indentation` is set to `true` by default, ST will
  still detects the indentation internally before ASI is ready to work.
  After that, ASI will detects the indentation **again**
  hence ST's result will be overridden but the detection is done **twice**.
  Therefore, you may want to set `detect_indentation` to `false` to skip ST's.

## Installation

This package is available on Package Control by the name of
[AutoSetIndentation](https://packagecontrol.io/packages/AutoSetIndentation).

## Settings

To edit settings, go to `Preferences` » `Package Settings` » `AutoSetIndentation` » `Settings`.

I think the [settings file](https://github.com/jfcherng-sublime/ST-AutoSetIndentation/blob/master/AutoSetIndentation.sublime-settings)
is self-explanatory. But if you still have questions, feel free to open an issue.

## Commands

You may disable all `event_listeners` in your user settings
and add a key binding to auto set the indentation whenever you want.

```javascript
{ "keys": ["ctrl+alt+s", "ctrl+alt+i"], "command": "auto_set_indentation" },
```

## Acknowledgment

- [editorconfig](https://github.com/editorconfig/editorconfig-core-py)
- [Indent Finder](http://www.freehackers.org/Indent_Finder)
