import os
import winshell
import winsound
import PySimpleGUI as sg
import json
from delete_function import delete_dir_contents


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
        [sg.Push(), sg.Button("Apply"), sg.Button("Close"), sg.Push()]
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

            user_settings["settings"]["font_size"] = font_size
            user_settings["settings"]["clean_all_recycle_bin"] = clean_all_recycle_bin

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
    "theme": "graygraygray",
    "settings": {
        "font_size": 15,
        "clean_all_recycle_bin": True,
    }
}
temp_path = r"C:\Windows\Temp"
temp_percent_path = os.path.join(os.path.expanduser('~'), "AppData\Local\Temp")

help_text = """
Hello there! You can use me to clean any temporary files on your Windows machine!
temp is for cleaning Windows temporary files.
%temp% is for cleaning user temporary files (AppData folder).
You can also clean the recycle bin.
"""


def create_window():
    global user_settings
    global apply_settings

    if (apply_settings == True):
        apply_settings = False

    if(os.path.isdir(save_file_dir)):
        with open(save_file_location) as f:
            user_settings = json.load(f)

    font_size = user_settings["settings"]["font_size"]
    theme = user_settings["theme"]

    sg.theme(theme)
    sg.set_options(font=f"* {font_size}")

    options_layout = ["Themes", ["Light", "Dark"],
                        "Settings"]

    menu_layout = [

        ["Options", options_layout],
        ["Help", ["How to Use?"]],

    ]

    layout = [

        [sg.Menu(menu_layout)],
        [sg.Text("temp ➩          "), sg.Button("Clean", key="CLEAN-TEMP")],
        [sg.Text("%temp% ➩    "), sg.Button("Clean", key="CLEAN-%TEMP%")],
        [sg.Text("recycle bin ➩  "), sg.Button("Clean", key="CLEAN-RECYCLE-BIN")],
        [sg.VPush()],
        [sg.HorizontalSeparator()],
        [sg.VPush()],
        [sg.Button("Clean All!", key="CLEAN-ALL")],

    ]

    return sg.Window("Temp Cleaner",
                    layout,
                    size=(400, 200),
                    element_justification="center")

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
                sg.popup_error(f"Something went wrong!\nException: {exception}")

    elif (event == "CLEAN-%TEMP%"):
        user_input = sg.popup_ok_cancel(f"Are you sure to clean %temp%?")
        if (user_input == "OK"):
            # cleaning %temp%
            exception = delete_dir_contents(temp_percent_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}")

    elif (event == "CLEAN-RECYCLE-BIN"):
        user_input = sg.popup_ok_cancel(f"Are you sure to clean the recycle bin?")
        if (user_input == "OK"):
            # cleaning the recycle bin
            try:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            except Exception as e:
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"An Error Occured! It may be your recycle bin is already empty!\nException: {e}")
    
    elif (event == "CLEAN-ALL"):
        user_input = sg.popup_ok_cancel(f"Are you sure to clean all temp, %temp% and the recycle bin?")
        if (user_input == "OK"):
            # temp
            exception = delete_dir_contents(temp_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}")
            # %temp%
            exception = delete_dir_contents(temp_percent_path)
            if (exception is not None):
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"Something went wrong!\nException: {exception}")
            # recycle bin
            if (user_settings["settings"]["clean_all_recycle_bin"]):
                try:
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                except Exception as e:
                    winsound.PlaySound("*", winsound.SND_ASYNC)
                    sg.popup_error(f"An Error Occured! It may be your recycle bin is already empty!\nException: {e}")

    elif (event == "Settings"):
        open_settings()

        if (apply_settings == True):
            window.close()
            window = create_window()

    elif (event == "How to Use?"):
        sg.popup_ok(help_text)
    
    elif (event == "Dark"):
        user_settings["theme"] = "dark"
        save_user_settings()

        window.close()
        window = create_window()
    
    elif (event == "Light"):
        user_settings["theme"] = "graygraygray"
        save_user_settings()

        window.close()
        window = create_window()


window.close()
