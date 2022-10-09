import os
import winshell
import winsound
import PySimpleGUI as sg
import json
from functions import *


def get_size(content):
    """
    content -> "temp", "%temp%" or "recyclebin"
    """
    def get_folder_size(folder):
        total_size = os.path.getsize(folder)

        for item in os.listdir(folder):
            itempath = os.path.join(folder, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += get_folder_size(itempath)
        
        return total_size
    
    size = 0
    folders_in_recycle_bin = False
    if (content == "temp"):
        size = get_folder_size(temp_path)
    
    elif (content == "%temp%"):
        for item in os.listdir(temp_percent_path):
            size = get_folder_size(temp_percent_path)
    
    elif (content == "recyclebin"):
        rb_items = winshell.recycle_bin()
        for item in rb_items:
            try:
                size += item.getsize()
            except Exception as e:
                folders_in_recycle_bin = True
                print("Exception:", e)
    elif (content == "prefetch"):
        for item in os.listdir(prefetch_path):
            size = get_folder_size(prefetch_path)

    if (folders_in_recycle_bin):
        return f"({get_readable_size(size)}+) "
    else:
        return f"({get_readable_size(size)}) "


def save_user_settings():
    # creating the directory if it does not exist
    if(os.path.isdir(save_file_dir)):
        pass
    else:
        os.makedirs(save_file_dir)
    
    # writing to file
    with open(save_file_location, "w") as f:
        json.dump(user_settings, f, indent=2)


def open_settings():
    global apply_settings

    default_font_value = ""

    if (user_settings["settings"]["font_size"] == 10):
        default_font_value = "Small"
    else:
        default_font_value = "Large"

    layout = [
        [sg.Text("Font Size:    "), sg.Combo(["Small", "Large"], default_value=default_font_value, readonly=True, key="FONT_SIZE")],
        [sg.Checkbox("Clear Recycle bin when Clean All button is pressed.", default=user_settings["settings"]["clean_all_recycle_bin"], key="CLEAN_RECYCLE_BIN")],
        [sg.Checkbox("Show sizes of the files to be cleaned.", default=user_settings["settings"]["show_sizes"], key="SHOW_SIZES")],
        [sg.Push(), sg.Button("Apply"), sg.Button("Close"), sg.Push()],
    ]

    window = sg.Window("Settings", layout, margins=(30, 30), modal=True)

    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED or event == "Close"):
            break

        elif (event == "Apply"):
            # updating user_settings
            if (values["FONT_SIZE"] == "Large"):
                font_size = 15
            else:
                font_size = 10
            
            clean_all_recycle_bin = values["CLEAN_RECYCLE_BIN"]
            show_sizes = values["SHOW_SIZES"]

            user_settings["settings"]["font_size"] = font_size
            user_settings["settings"]["clean_all_recycle_bin"] = clean_all_recycle_bin
            user_settings["settings"]["show_sizes"] = show_sizes

            save_user_settings()

            # applying changes
            apply_settings = True
            break
    
    window.close()


# variables
save_file_dir = os.path.join(os.path.expanduser ('~'), "AppData", "Local", "TempCleaner")
save_file_location = os.path.join(save_file_dir, "user_settings.json")
apply_settings = False
user_settings = {
    "theme": "GrayGrayGray",
    "settings": {
        "font_size": 10,
        "clean_all_recycle_bin": True,
        "show_sizes": True,
    }
}
temp_path = r"C:\Windows\Temp"
temp_percent_path = os.path.join(os.path.expanduser('~'), "AppData\Local\Temp")
prefetch_path = r"C:\Windows\Prefetch"

help_text = """
Hello there! You can use me to clean any unnecessary and temporary files on your Windows machine!

1. temp is for cleaning Windows temporary files.
2. %temp% is for cleaning user temporary files (AppData folder).
3. prefetch is for cleaning files created by Windows for faster startup of the PC and apps.
4. You can also clean the recycle bin.

"""
about_text = """
Hello! Thanks for using Temp Cleaner (V2.0)! Made with PySimpleGUI in Python!
Created by: Vaibhav Kumar

Special Thanks to: Jan Pales (Discord ID: Derian#2429)
"""


def create_window(cleaning=False):
    global user_settings
    global apply_settings
    global total_size

    if (apply_settings == True):
        apply_settings = False

    if(os.path.isdir(save_file_dir)):
        with open(save_file_location) as f:
            user_settings = json.load(f)

    font_size = user_settings["settings"]["font_size"]
    theme = user_settings["theme"]
    show_sizes = user_settings["settings"]["show_sizes"]
    clean_all_recycle_bin = user_settings["settings"]["clean_all_recycle_bin"]

    if (show_sizes):
        sizes_data = [get_size(content) for content in ("temp", "%temp%", "prefetch", "recyclebin")]
        
        size_bytes = 0
        # sizes_data -> ['5.0 MB', '56.78 GB', '34.91 KB']
        for index, i in enumerate(sizes_data):
            unit = i[i.index(" ") + 1]           # M, K or G
            size = float(i[1: i.index(" ")])

            if (unit == "K"):
                size *= 1024
            elif (unit == "M"):
                size *= (1024 * 1024)
            else:
                size *= (1024 * 1024 * 1024)
            
            if (clean_all_recycle_bin == False and index == 2):
                pass
            else:
                size_bytes += size
        
        try:
            total_old_size = total_size
        except:
            pass
        
        total_size = get_readable_size(size_bytes)

        if (cleaning):
            print(total_old_size.split()[0])
            print(total_size.split()[0])

            cleaned_size = float(total_old_size.split()[0]) - float(total_size.split()[0])
            sg.popup_auto_close(f"Successfully cleared {round(cleaned_size, 1)} of unnecessary files! That's more free storage for you!", no_titlebar=True)

    else:
        sizes_data = ["" for _ in range(4)]
        total_size = ""

    sg.theme(theme)
    sg.set_options(font=f"* {font_size}")

    options_layout = ["Refresh (F2)",
                     f"Themes ({theme})", sg.theme_list(),
                        "Settings"]

    menu_layout = [

        ["Options", options_layout],
        ["Help", ["How to Use? (F1)", "About Temp Cleaner"]],

    ]

    layout = [

        [sg.Menu(menu_layout)],
        [sg.Text(f"{sizes_data[0]}temp ➩          "), sg.Button("Clean", key="CLEAN-TEMP")],
        [sg.Text(f"{sizes_data[1]}%temp% ➩    "), sg.Button("Clean", key="CLEAN-%TEMP%")],
        [sg.Text(f"{sizes_data[2]}recycle bin ➩  "), sg.Button("Clean", key="CLEAN-RECYCLE-BIN")],
        [sg.Text(f"{sizes_data[3]}prefetch ➩       "), sg.Button("Clean", key="CLEAN-PREFETCH")],
        [sg.VPush()],
        [sg.HorizontalSeparator()],
        [sg.VPush()],
        [sg.Button("Clean All!", key="CLEAN-ALL")],
        [sg.Text(f"{total_size}")]

    ]

    return sg.Window("Temp Cleaner",
                    layout,
                    size=(400, 250),
                    element_justification="center",
                    return_keyboard_events=True)

window = create_window()

while True:
    event, values = window.read()

    # reading events
    if (event == sg.WIN_CLOSED):
        break

    elif (event == "CLEAN-TEMP"):
        user_input = sg.popup_ok_cancel(f"Are you sure to clean temp?")
        if (user_input == "OK"):
            # cleaning temp
            exception = delete_dir_contents(temp_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}", title="Oops!")
            
            window.close()
            window = create_window()

    elif (event == "CLEAN-%TEMP%"):
        user_input = sg.popup_ok_cancel(f"Are you sure to clean %temp%?")
        if (user_input == "OK"):
            # cleaning %temp%
            exception = delete_dir_contents(temp_percent_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}", title="Oops!")
            
            window.close()
            window = create_window()

    elif (event == "CLEAN-RECYCLE-BIN"):
        user_input = sg.popup_ok_cancel(f"Are you sure to clean the recycle bin?")
        if (user_input == "OK"):
            # cleaning the recycle bin
            try:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            except Exception as e:
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"An Error Occured! It may be your recycle bin is already empty!\nException: {e}", title="Oops!")

            window.close()
            window = create_window()
    elif (event == "CLEAN-PREFETCH"):
        user_input = sg.popup_ok_cancel(f"Are you sure to clean prefetch?")
        if (user_input == "OK"):
            # cleaning prefetch
            exception = delete_dir_contents(prefetch_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}", title="Oops!")
            
            window.close()
            window = create_window()

    elif (event == "CLEAN-ALL"):
        if (user_settings["settings"]["clean_all_recycle_bin"] == True):
            user_input = sg.popup_ok_cancel(f"Are you sure to clean all temp, %temp% and the recycle bin?")
        else:
            user_input = sg.popup_ok_cancel(f"Are you sure to clean all temp and %temp%?")
        if (user_input == "OK"):
            # temp
            exception = delete_dir_contents(temp_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}", title="Oops!")
            # %temp%
            exception = delete_dir_contents(temp_percent_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}", title="Oops!")
            exception = delete_dir_contents(prefetch_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}", title="Oops!")
            # recycle bin
            if (user_settings["settings"]["clean_all_recycle_bin"]):
                try:
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                except Exception as e:
                    winsound.PlaySound("*", winsound.SND_ASYNC)
                    sg.popup_error(f"An Error Occured! It may be your recycle bin is already empty!\nException: {e}", title="Oops!")

            window.close()
            window = create_window(cleaning=True)

    elif (event == "Refresh (F2)" or event == "F2:113"):
        window.close()
        window = create_window()

    elif (event == "Settings"):
        open_settings()

        if (apply_settings == True):
            window.close()
            window = create_window()

    elif (event == "How to Use? (F1)" or event == "F1:112"):
        sg.popup_ok(help_text)
    
    elif (event == "About Temp Cleaner"):
        sg.popup_ok(about_text)
    
    # theme events
    for theme_name in sg.theme_list():
        if (event == theme_name):
            user_settings["theme"] = event
            save_user_settings()

            window.close()
            window = create_window()


window.close()
