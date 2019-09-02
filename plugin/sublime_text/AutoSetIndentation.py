import sublime
import sublime_plugin
from typing import Tuple, Dict, Optional
from ..functions import (
    is_view_at_front,
    is_view_only_invisible_chars,
    is_event_listener_enabled,
    set_indentation_for_view,
)
from ..log import print_msg
from ..settings import get_setting


class AutoSetIndentationEventListener(sublime_plugin.EventListener):
    def on_load_async(self, view: sublime.View) -> None:
        if is_event_listener_enabled("on_load_async"):
            set_indentation_for_view(view)

    def on_modified_async(self, view: sublime.View) -> None:
        # when the view is left only invisible chars (\s),
        # we assume the indentation of this view has not been detected yet
        if is_view_only_invisible_chars(view):
            view.settings().set("ASI_is_indentation_detected", False)

    def on_text_command(
        self, view: sublime.View, command_name: str, args: dict
    ) -> Optional[Tuple[str, Dict]]:
        """
        @brief Replace Sublime Text's "detect_indentation" command with this plugin's.

        @param self         The object
        @param view         The view
        @param command_name The command name
        @param args         The arguments

        @return A tuple in the form of (command, arguments)
        """

        if command_name != "detect_indentation" or not get_setting("hijack_st_detect_indentation"):
            return None

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
