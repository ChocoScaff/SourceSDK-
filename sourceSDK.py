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
    btn_hammer : tk.Button
    btn_hammer_plus_plus : tk.Button
    btn_hlmv : tk.Button
    btn_hlfaceposer : tk.Button
    btn_qc_eyes : tk.Button
    btn_vtf_edit : tk.Button
    btn_games : tk.Button
    btn_everything : tk.Button
    btn_particle : tk.Button
    btn_Launch : tk.Button
    btn_Launch_dev : tk.Button
    other_menu : tk.Menu
    texture_menu : tk.Menu
    map_menu : tk.Menu
    model_menu : tk.Menu
    menu_bar : tk.Menu
    scrollbar : tk.Scrollbar
    listbox : tk.Listbox
    root : tk.Tk
    game_path = []



