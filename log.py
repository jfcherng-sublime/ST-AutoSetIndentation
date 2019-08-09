import sublime

PLUGIN_NAME = __package__


def msg(message: str) -> str:
    """
    @brief Generate plugin message.

    @param message The message

    @return The plugin message.
    """

    return "[{plugin}] {message}".format(plugin=PLUGIN_NAME, message=message)


def print_msg(message: str, show_message: bool = True) -> None:
    """
    @brief Print plugin message to ST's console.

    @param message      The message
    @param show_message Whether to print the message
    """

    if show_message:
        print(msg(message))


def show_status_message(message: str, show_message: bool = True) -> None:
    """
    @brief Shows message in the status bar.

    @param message      The message
    @param show_message Whether to show the message
    """

    from .settings import get_setting

    if show_message and get_setting("show_status_message"):
        sublime.status_message(message)
