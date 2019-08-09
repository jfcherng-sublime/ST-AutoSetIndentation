import collections
import re
import sublime
import sublime_plugin
from .libs.editorconfig import get_properties, EditorConfigError
from .libs.IndentFinder.indent_finder import IndentFinder
from .log import msg
from .settings import get_setting, show_status_message

Indentation = collections.namedtuple("Indentation", ["type", "size"])
indentation_unknown = Indentation("unknown", -1)


def get_ASI_result_sources_for_view(view):
    return view.settings().get("ASI_result_sources", [])


def reset_ASI_result_sources_for_view(view):
    view.settings().set("ASI_result_sources", [])


def add_ASI_result_sources_for_view(view, sources):
    view.settings().set("ASI_result_sources", get_ASI_result_sources_for_view(view) + list(sources))


def merge_indentation_tuples(base, spare):
    merged = base._asdict()

    if merged["type"] == indentation_unknown.type:
        merged["type"] = spare.type

    if merged["size"] == indentation_unknown.size:
        merged["size"] = spare.size

    return Indentation(**merged)


class AutoSetIndentationCommand(sublime_plugin.TextCommand):
    """ Examines the contents of the buffer to determine the indentation settings. """

    def run(self, edit, show_message=True, sample_length=2 ** 16):
        """
        @brief Run the "auto_set_indentation" command.

        @param self         The object
        @param edit         The edit
        @param show_message The show message
        """

        reset_ASI_result_sources_for_view(self.view)

        indent = self.get_indentation_for_view(self.view, sample_length)

        # unable to determine, use the default settings
        if indent.type == indentation_unknown.type or indent.size <= 0:
            reset_ASI_result_sources_for_view(self.view)
            default_indentation = get_setting("default_indentation")
            self.use_indentation_default(self.view, default_indentation, show_message)
            return

        # tab-indented
        if indent.type == "tab":
            self.use_indentation_tab(self.view, indent.size, show_message)
            return

        # space-indented
        if indent.type == "space":
            self.use_indentation_space(self.view, indent.size, show_message)
            return

    def get_indentation_for_view(self, view, sample_length=2 ** 16):
        """
        @brief Guess the indentation for the view.
               This would first try using configs from the .editorconfig file
               and guess the indentation as the fallback otherwise.

        @param self          The object
        @param view          The view
        @param sample_length The sample length

        @return The indentation for view.
        """

        indentation_editorconfig = self.get_indentation_from_editorconfig()

        if indentation_editorconfig != indentation_unknown:
            add_ASI_result_sources_for_view(view, [".editorconfig"])

        # .editorconfig provides all needed informations
        if (
            indentation_editorconfig.type != indentation_unknown.type
            and indentation_editorconfig.size != indentation_unknown.size
        ):
            return indentation_editorconfig

        sample = view.substr(sublime.Region(0, min(view.size(), sample_length)))
        indentation_guessed = self.guess_indentation_from_string(sample)

        add_ASI_result_sources_for_view(view, ["guessing"])

        return merge_indentation_tuples(indentation_editorconfig, indentation_guessed)

    def get_indentation_from_editorconfig(self):
        """
        @brief Guess the indentation from the .editorconfig file.

        @param self   The object

        @return Indentation namedtuple
        """

        indentation = indentation_unknown._asdict()

        file_path = self.view.file_name()

        # is a new buffer so no file path
        if not file_path:
            return indentation_unknown

        try:
            options = get_properties(file_path)
        except EditorConfigError:
            return indentation_unknown

        indent_style = options.get("indent_style")
        indent_size = options.get("indent_size")

        # sanitize indent_style
        if indent_style != "space" and indent_style != "tab":
            indent_style = indentation_unknown.type

        # sanitize indent_size
        try:
            indent_size = int(indent_size)
        except (TypeError, ValueError):
            indent_size = indentation_unknown.size

        if indent_style == "space" or indent_style == "tab":
            indentation["type"] = indent_style
            indentation["size"] = indent_size

            return Indentation(**indentation)

        return indentation_unknown

    def guess_indentation_from_string(self, string):
        """
        @brief Guess the indentation of the given string.

        @param self   The object
        @param string The string

        @return Indentation namedtuple
        """

        indentation = indentation_unknown._asdict()

        indent_finder = IndentFinder(tuple(indentation_unknown))
        indent_finder.parse_string(string)

        # possible outputs:
        #   - space X
        #   - tab Y
        #   - mixed tab Y space X
        #   - unknown -1 (the default one from the constructor)
        finder_result = str(indent_finder)

        # unable to determine the indentation
        if finder_result == "{type} {size}".format(**indentation_unknown._asdict()):
            return indentation_unknown

        indent_tab = re.search(r"\btab\s+([0-9]+)", finder_result)
        indent_tab = int(indent_tab.group(1)) if indent_tab else 0

        indent_space = re.search(r"\bspace\s+([0-9]+)", finder_result)
        indent_space = int(indent_space.group(1)) if indent_space else 0

        # note that for mixed indentation, we assume it's tab-indented
        if indent_tab > 0:
            indentation["type"] = "tab"
            indentation["size"] = indent_tab

        if indent_space > 0:
            indentation["type"] = "space"
            indentation["size"] = indent_space

        return Indentation(**indentation)

    def use_indentation_default(self, view, default_indentation, show_message=True):
        """
        @brief Sets the indentation to default.

        @param self                The object
        @param view                The view
        @param default_indentation The default indentation in the form of (indent_type, indent_size)
        @param show_message        The show message
        """

        indent_type, indent_size = default_indentation
        indent_type = indent_type.lower()

        if indent_type.startswith("tab"):
            self.use_indentation_tab(view, indent_size, False)

        if indent_type.startswith("space"):
            self.use_indentation_space(view, indent_size, False)

        show_status_message(
            msg("Indentation: {}/{} (default)".format(indent_type, indent_size)), show_message
        )

    def use_indentation_tab(self, view, indent_tab=4, show_message=True):
        """
        @brief Sets the indentation to tab.

        @param self         The object
        @param view         The view
        @param indent_tab   The indent tab size
        @param show_message The show message
        """

        self.view.settings().set("translate_tabs_to_spaces", False)
        self.view.settings().set("tab_size", indent_tab)

        show_status_message(
            msg(
                "Indentation: tab/{} (by {})".format(
                    indent_tab, ", ".join(get_ASI_result_sources_for_view(view))
                )
            ),
            show_message,
        )

    def use_indentation_space(self, view, indent_space=4, show_message=True):
        """
        @brief Sets the indentation to space.

        @param self         The object
        @param view         The view
        @param indent_space The indent space size
        @param show_message The show message
        """

        self.view.settings().set("translate_tabs_to_spaces", True)
        self.view.settings().set("tab_size", indent_space)

        show_status_message(
            msg(
                "Indentation: space/{} (by {})".format(
                    indent_space, ", ".join(get_ASI_result_sources_for_view(view))
                )
            ),
            show_message,
        )
