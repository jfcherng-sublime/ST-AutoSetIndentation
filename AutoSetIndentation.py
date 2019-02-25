from .IndentFinder.indent_finder import IndentFinder
import re
import sublime
import sublime_plugin


PLUGIN_NAME = __package__
PLUGIN_DIR = 'Packages/%s' % PLUGIN_NAME
PLUGIN_SETTINGS = '%s.sublime-settings' % PLUGIN_NAME


def plugin_message(message):
    return '[{0}] {1}'.format(PLUGIN_NAME, message)


def print_plugin_message(message, show_message=True):
    if show_message:
        print(plugin_message(message))


def show_status_message(message, show_message=True):
    if show_message:
        sublime.status_message(message)


class AutoSetIndentationCommand(sublime_plugin.TextCommand):
    """Examines the contents of the buffer to determine the indentation settings."""

    def run(self, edit, show_message=True, sample_length=2**16):
        """
        @brief Run the command.

        @param self         The object
        @param edit         The edit
        @param show_message The show message
        """

        sample = self.view.substr(sublime.Region(0, min(self.view.size(), sample_length)))
        indent_tab, indent_space = self.guess_indentation_from_string(sample)

        # more like mixed-indented
        if indent_tab > 0 and indent_space > 0:
            self.set_mixed_indentation(indent_tab, indent_space)
            return

        # tab-indented
        if indent_tab > 0:
            self.set_tab_indentation(indent_tab)
            return

        # space-indented
        if indent_space > 0:
            self.set_space_indentation(indent_space)
            return

    def guess_indentation_from_string(self, string):
        """
        @brief Guess the indentation of the given string.

        @param self   The object
        @param string The string

        @return (int, int) A tuple in the form of (indent_tab, indent_space)
        """

        indent_finder = IndentFinder()
        indent_finder.parse_string(string)

        # possible outputs:
        #   - space X
        #   - tab Y
        #   - mixed tab Y space X
        result = str(indent_finder)

        indent_tab = re.search(r'\btab\s+([0-9]+)', result)
        indent_tab = int(indent_tab.group(1)) if indent_tab else 0

        indent_space = re.search(r'\bspace\s+([0-9]+)', result)
        indent_space = int(indent_space.group(1)) if indent_space else 0

        return (indent_tab, indent_space)

    def set_mixed_indentation(self, indent_tab=4, indent_space=4, show_message=True):
        self.set_tab_indentation(indent_tab, False)
        show_status_message(
            plugin_message('Indentation: tab/%d space/%d (mixed)' % (indent_tab, indent_space)),
            show_message
        )

    def set_tab_indentation(self, indent_tab=4, show_message=True):
        self.view.settings().set('translate_tabs_to_spaces', False)
        self.view.settings().set('tab_size', indent_tab)
        show_status_message(
            plugin_message('Indentation: tab/%d' % indent_tab),
            show_message
        )

    def set_space_indentation(self, indent_space=4, show_message=True):
        self.view.settings().set('translate_tabs_to_spaces', True)
        self.view.settings().set('tab_size', indent_space)
        show_status_message(
            plugin_message('Indentation: space/%d' % indent_space),
            show_message
        )


class AutoSetIndentationEventListener(sublime_plugin.EventListener):
    def on_activated_async(self, view):
        if self.can_trigger_event_listener('on_activated_async'):
            self.auto_set_indentation(view)

    def on_clone_async(self, view):
        if self.can_trigger_event_listener('on_clone_async'):
            self.auto_set_indentation(view)

    def on_load_async(self, view):
        if self.can_trigger_event_listener('on_load_async'):
            self.auto_set_indentation(view)

    def on_modified_async(self, view):
        if self.can_trigger_event_listener('on_modified_async'):
            self.auto_set_indentation(view)

    def on_new_async(self, view):
        if self.can_trigger_event_listener('on_new_async'):
            self.auto_set_indentation(view)

    def on_post_paste(self, view):
        if self.can_trigger_event_listener('on_post_paste'):
            self.auto_set_indentation(view)

    def on_pre_save_async(self, view):
        if self.can_trigger_event_listener('on_pre_save_async'):
            self.auto_set_indentation(view)

    def auto_set_indentation(self, view):
        """
        @brief Set the indentation for the current view.

        @param self The object
        @param view The view
        """

        is_at_front = view.window() is not None and view.window().active_view() == view
        view.run_command('auto_set_indentation', {'show_message': is_at_front})

    def can_trigger_event_listener(self, event):
        """
        @brief Check if a event listener is allowed to be triggered.

        @param self  The object
        @param event The event

        @return True if able to trigger event listener, False otherwise.
        """

        settings = sublime.load_settings(PLUGIN_SETTINGS)

        return settings.get('enabled', False) and self.is_event_listener_enabled(event)

    def is_event_listener_enabled(self, event):
        """
        @brief Check if a event listener is enabled.

        @param self  The object
        @param event The event

        @return True if event listener enabled, False otherwise.
        """

        settings = sublime.load_settings(PLUGIN_SETTINGS)

        try:
            return settings.get('event_listeners', {})[event]
        except KeyError:
            print_plugin_message(
                '"event_listeners[%s]" is not set in user settings (assumed false)' %
                event
            )

            return False
