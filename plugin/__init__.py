import os
import sublime
import sys
from .functions import is_event_listener_enabled, set_indentation_for_view
from .log import print_msg
from .utils import is_view_normal_ready

# stupid python module system
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))


def set_up() -> None:
    """ plugin_loaded """

    if int(sublime.version()) >= 4050:
        print_msg(
            "As of Sublime Text 4, the dev team has been use test cases from this plugin "
            "to improve the built-in indentation detection and it works quite well. "
            "So, you probably no longer needs this plugin in Sublime Text 4."
        )

    # A dirty fix for "on_load_async" is not trigger on starting
    # @see https://github.com/SublimeTextIssues/Core/issues/5#issuecomment-476225021
    for window in sublime.windows():
        for view in window.views():
            # oops! view is already ready before plugin has been loaded
            if is_view_normal_ready(view) and is_event_listener_enabled("on_load_async"):
                set_indentation_for_view(view)


def tear_down() -> None:
    """ plugin_unloaded """

    pass
