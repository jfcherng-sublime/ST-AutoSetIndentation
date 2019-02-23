from .IndentFinder.indent_finder import IndentFinder
import re
import sublime
import sublime_plugin


PLUGIN_NAME = __package__
PLUGIN_DIR = 'Packages/%s' % PLUGIN_NAME
PLUGIN_SETTINGS = PLUGIN_NAME + '.sublime-settings'

settings = None


def plugin_unloaded():
    global settings

    settings.clear_on_change(PLUGIN_SETTINGS)


def plugin_loaded():
    global settings

    settings = sublime.load_settings(PLUGIN_SETTINGS)

    # when the user settings is modified
    settings.add_on_change(PLUGIN_SETTINGS, pluginSettingsListener)


def pluginSettingsListener():
    """ called when plugin's settings file is changed """

    global settings


def printPluginMessage(message):
    print(pluginMessage(message))


def pluginMessage(message):
    return '[{0}] {1}'.format(PLUGIN_NAME, message)


class AutoSetIndentationCommand(sublime_plugin.TextCommand):
    def run(self, edit, show_message=True):
        """
        @brief Examines the contents of the buffer to determine the indentation settings.

        @param self         The object
        @param edit         The edit
        @param show_message The show message
        """

        sample = self.view.substr(sublime.Region(0, min(self.view.size(), 2**14)))

        indent_finder = IndentFinder()
        indent_finder.parse_string(sample)

        # possible outputs:
        #
        #   - space X
        #   - tab Y
        #   - mixed tab Y space X
        #
        # where X and Y are integers
        result = str(indent_finder)

        indent_tab = re.search(r'\btab\s+([0-9]+)', result)
        indent_tab = int(indent_tab.group(1)) if indent_tab else 0

        indent_space = re.search(r'\bspace\s+([0-9]+)', result)
        indent_space = int(indent_space.group(1)) if indent_space else 0

        if indent_tab > indent_space:
            self.view.settings().set('translate_tabs_to_spaces', False)
            self.view.settings().set('tab_size', indent_tab)
            self.show_status_message(
                pluginMessage('Indentation: tabs'),
                show_message
            )
        else:
            self.view.settings().set('translate_tabs_to_spaces', True)
            self.view.settings().set('tab_size', indent_space)
            self.show_status_message(
                pluginMessage('Indentation: %d spaces' % indent_space),
                show_message
            )

    def show_status_message(self, message, show_message=True):
        if show_message:
            sublime.status_message(message)


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

        global settings

        return settings.get('enabled', False) and self.is_event_listener_enabled(event)

    def is_event_listener_enabled(self, event):
        """
        @brief Check if a event listener is enabled.

        @param self  The object
        @param event The event

        @return True if event listener enabled, False otherwise.
        """

        global settings

        try:
            return settings.get('event_listeners', None)[event]
        except:
            printPluginMessage(
                '"%s" is not set in user settings (assumed false)' %
                ('event_listeners.' + event)
            )

            return False
