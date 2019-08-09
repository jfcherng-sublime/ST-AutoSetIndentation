import sublime
import sublime_plugin
from .log import msg, print_msg
from .settings import get_setting, show_status_message


def plugin_loaded() -> None:
    # https://github.com/SublimeTextIssues/Core/issues/5#issuecomment-476225021
    # A dirty fix for "on_load_async" is not trigger on starting

    for window in sublime.windows():
        for view in window.views():
            if not view.is_loading() and is_event_listener_enabled("on_load_async"):
                set_indentation_for_view(view)


def is_view_at_front(view: sublime.View) -> bool:
    return view.window() is not None and view.window().active_view() == view


def is_view_only_invisible_chars(view: sublime.View) -> bool:
    return view.find(r"[^\s]", 0).begin() < 0


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


class AutoSetIndentationEventListener(sublime_plugin.EventListener):
    def on_load_async(self, view: sublime.View) -> None:
        if is_event_listener_enabled("on_load_async"):
            set_indentation_for_view(view)

    def on_modified_async(self, view: sublime.View) -> None:
        # when the view is left only invisible chars (\s),
        # we assume the indentation of this view has not been detected yet
        if is_view_only_invisible_chars(view):
            view.settings().set("ASI_is_indentation_detected", False)

    def on_text_command(self, view: sublime.View, command_name: str, args: dict):
        """
        @brief Replace Sublime Text's "detect_indentation" command with this plugin's.

        @param self         The object
        @param view         The view
        @param command_name The command name
        @param args         The arguments

        @return (str, dict) A tuple in the form of (command, arguments)
        """

        if command_name != "detect_indentation" or not get_setting("hijack_st_detect_indentation"):
            return

        print_msg('"%s" command hijacked' % command_name)

        return ("auto_set_indentation", {"show_message": is_view_at_front(view)})

    def on_post_text_command(self, view: sublime.View, command_name: str, args: dict) -> None:
        """
        @brief Set the indentation when the user pastes.

        @param self         The object
        @param view         The view
        @param command_name The command name
        @param args         The arguments
        """

        if (
            view.settings().get("ASI_is_indentation_detected", False)
            or not is_event_listener_enabled("on_post_paste")
            or (command_name != "paste" and command_name != "paste_and_indent")
        ):
            return

        set_indentation_for_view(view)
