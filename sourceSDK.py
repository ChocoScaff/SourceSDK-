import string
import tkinter as tk


class SourceSDK():
    selected_folder : string
    bin_folder : string
    executable_game : string
    game_name : string
    first_init : bool
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
    text_widget : tk.Text
    vpk_path : string
    root : tk.Tk

    def __init__(self):
        self.first_init = 0



