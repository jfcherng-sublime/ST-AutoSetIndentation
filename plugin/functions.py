import sublime
from .settings import get_setting
from .log import msg, print_msg, show_status_message


def is_view_at_front(view: sublime.View) -> bool:
    return view and view.window() and view.window().active_view() == view


def is_view_only_invisible_chars(view: sublime.View) -> bool:
    return view and view.find(r"[^\s]", 0).begin() < 0


def is_view_set_by_editorconfig_plugin(view: sublime.View) -> bool:
    EDITORCONFIG_PLUGIN_MARKER = "editorconfig"

    return bool(view.settings().get(EDITORCONFIG_PLUGIN_MARKER, False))


def is_event_listener_enabled(event: str) -> bool:
    """
    @brief Check if a event listener is enabled.

    @param event The event

    @return True if event listener enabled, False otherwise.
    """

    try:
        return bool(get_setting("event_listeners", {})[event])
    except KeyError:
        print_msg('"event_listeners[%s]" is not set in user settings (assumed false)' % event)

        return False


def set_indentation_for_view(view: sublime.View, args: dict = {}) -> None:
    """
    @brief Set the indentation for the current view.

    @param view The view
    @param args The arguments
    """

    _args = {"show_message": is_view_at_front(view)}
    _args.update(args)

    if is_view_set_by_editorconfig_plugin(view):
        show_status_message(msg("EditorConfig detected indentation"), _args["show_message"])
    else:
        view.run_command("auto_set_indentation", _args)

    view.settings().set("ASI_is_indentation_detected", True)
