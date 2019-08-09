import sublime


def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    return __package__


def get_package_path() -> str:
    """
    @brief Gets the package path.

    @return The package path.
    """

    return "Packages/" + get_package_name()


def get_settings_file() -> str:
    """
    @brief Get the settings file name.

    @return The settings file name.
    """

    return "AutoSetIndentation.sublime-settings"


def get_settings_object() -> sublime.Settings:
    """
    @brief Get the plugin settings object.

    @return The settings object.
    """

    return sublime.load_settings(get_settings_file())


def get_setting(key: str, default=None):
    """
    @brief Get the plugin setting with the key.

    @param key     The key
    @param default The default value if the key doesn't exist

    @return The setting's value.
    """

    return get_settings_object().get(key, default)


def show_status_message(message, show_message=True):
    """
    @brief Shows message in the status bar.

    @param message      The message
    @param show_message Whether to show the message
    """

    if show_message and get_setting("show_status_message"):
        sublime.status_message(message)
