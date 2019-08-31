# AutoSetIndentation


## 1.6.1

- Introduce `mypy` for static analysis.


## 1.6.0

- Add and utilize the `typing` module.
- Changed plugin directory structure.


## 1.5.5

- Always use tab indentation for `Makefile` syntax.


## 1.5.4

There is no bug fix. Just some source codes maintenances.

- Put menu files to `menus/`.
- Split out `AutoSetIndentationCommand.py` from `AutoSetIndentation.py`.
- Add some type hinting to source codes.
- Source codes are formatted with [black](https://github.com/psf/black).


## 1.5.3

- Fix default indentation (fallback) is not used in some cases.


## 1.5.2

- Show more details about how the indentation is determined.


## 1.5.1

- Disable event-triggered auto set if `EditorConfig` has set the indentation.


## 1.5.0

- Respect the indentation settings in `.editorconfig` files.
- Implement a dirty hack for `on_load_async` is not triggered on starting.
- Fix a typo: `patse` -> `paste`.


## 1.4.0

- Add back the `on_post_paste` event listener.
- Indentation could be re-detected again after a view goes blank.
- Remove setting: `enabled`. (Just disable this package from Package Control)
- Remove (maybe) useless event listeners:

  - on_activated_async
  - on_clone_async
  - on_modified_async
  - on_new_async
  - on_pre_save_async


## 1.3.1

- Add the command to the command palette.
- Fix `show_message` is ignored in `auto_set_indentation` command.
- Update the menu.


## 1.3.0

- Add setting: `show_status_message`.
- Remove useless event listener: `on_post_paste`.


## 1.2.0

- Add setting: `default_indentation`.
- Code tidy.


## 1.1.0

- Add setting: `hijack_st_detect_indentation`.
- Add the missing open settings from ST's menu.
- Remove useless codes.


## 1.0.2

- Code tidy.


## 1.0.1

- Fix plugin name.
- Convert some plugin files' line endings to `LF`.


## 1.0.0

- Initial release.
