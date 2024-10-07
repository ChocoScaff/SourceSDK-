import string
import tkinter as tk


class SourceSDK():
    """
    @brief SourceSDK
    """

    selected_folder : string
    bin_folder : string
    executable_game : string
    game_name : string
    first_init : bool = 0
    other_menu : tk.Menu
    texture_menu : tk.Menu
    map_menu : tk.Menu
    model_menu : tk.Menu
    menu_bar : tk.Menu
    root : tk.Tk
    game_path = []
    parent_folder : string
    background_color : string
    foreground_color : string
    secondary_background_color : string