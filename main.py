import os
import winshell
import winsound
import PySimpleGUI as sg
from delete_function import delete_dir_contents


# variables
font_size = 15
temp_path = r"C:\Windows\Temp"
temp_percent_path = os.path.join(os.path.expanduser('~'), "AppData\Local\Temp")

help_text = """
Hello there! You can use me to clean any temporary files on your Windows machine!
temp is for cleaning Windows temporary files.
%temp% is for cleaning user temporary files (AppData folder).
You can also clean the recycle bin.
"""


def create_window(theme):
    sg.theme(theme)
    sg.set_options(font=f"* {font_size}")

    menu_layout = [

        ["Theme", ["Light", "Dark"]],
        ["Help", ["How to Use?"]],

    ]

    layout = [

        [sg.Menu(menu_layout)],
        [sg.Text("temp --->          "), sg.Button("Clean", key="CLEAN-TEMP")],
        [sg.Text("%temp% --->    "), sg.Button("Clean", key="CLEAN-%TEMP%")],
        [sg.Text("recycle bin ---> "), sg.Button("Clean", key="CLEAN-RECYCLE-BIN")],
        [sg.VPush()],
        [sg.HorizontalSeparator()],
        [sg.VPush()],
        [sg.Button("Clean All!", key="CLEAN-ALL")],

    ]

    return sg.Window("Temp Cleaner",
                    layout,
                    size=(400, 200),
                    element_justification="center")

window = create_window("graygraygray")

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
            try:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            except Exception as e:
                winsound.PlaySound("*", winsound.SND_ASYNC)
                sg.popup_error(f"An Error Occured! It may be your recycle bin is already empty!\nException: {e}")

    elif (event == "How to Use?"):
        sg.popup_ok(help_text)
    
    elif (event == "Dark"):
        window.close()
        window = create_window("Dark")
    
    elif (event == "Light"):
        window.close()
        window = create_window("graygraygray")


window.close()
