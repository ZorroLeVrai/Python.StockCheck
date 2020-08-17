import sys
import os
import os.path
from os.path import join
import tkinter
from tkinter import filedialog
from tkinter import ttk
import FileListing

############# Get command line arguments ##############
#argument_length = len(sys.argv)

#if argument_length>1:
#    current_path = sys.argv[1]

#filters = []
#index = 2
#while index < argument_length:
#    filters.append(sys.argv[index])
#    index += 1

#print(current_path)
#print(filters)

############## Variables golbales ##############

current_path = os.getcwd()
destination_path = join(current_path, "Result")

############## Gestion des commandes de l'interface graphique ##############

def browse_directory(folder_src, folder_dest, is_source):
    options = {}
    if (not is_source) and os.path.exists(folder_dest.get()):
        initial_dir = folder_dest.get()
    else:
        initial_dir = folder_src.get()
    options['initialdir'] = initial_dir
    options['title'] = "Répertoire source" if is_source else "Répertoire de destination" 
    new_dir = filedialog.askdirectory(**options)
    if len(new_dir) > 0:
        if is_source:
            folder_src.set(new_dir)
        else:
            folder_dest.set(new_dir)

def execute_command():
    try:
        control_button.config(state="disabled")
        print("############################################")
        print("lancement de la commande")
        command_progress.set(0)
        filter_list = []
        filter_value = filters.get()
        if len(filter_value) > 0:
            filter_list = filter_value.split(',')
        explorer = FileListing.PathExplorer(folder_src.get(), filter_list, display_path.get(), check_naming.get(), command_progress, command_option.get())
        output_file = file_output.get()
        if len(output_file) > 0:
            output_file = join(folder_dest, output_file)
        explorer.PrintFiles(output_file)
        if organise_files.get():
            explorer.Classify(folder_dest.get(), output_file)
        print("commande exécutée")
    finally:
        control_button.config(state="normal")

############## Creation de l'interface graphique ##############

main_window = tkinter.Tk()
main_window.title("Organisateur de music")
screen_x = main_window.winfo_screenwidth()
screen_y = main_window.winfo_screenheight()
window_x = 830
window_y = 240

pos_x = (screen_x - window_x) // 2
pos_y = (screen_y - window_y) // 2

main_window.geometry("{0}x{1}+{2}+{3}".format(window_x, window_y, pos_x, pos_y))
main_window.resizable(False, False)

folder_src = tkinter.StringVar()
folder_dest = tkinter.StringVar()
filters = tkinter.StringVar()
file_output = tkinter.StringVar()
display_path = tkinter.IntVar()
check_naming = tkinter.IntVar()
organise_files = tkinter.IntVar()
command_option = tkinter.IntVar()
command_progress = tkinter.DoubleVar()

entry_frame = tkinter.Frame(main_window)
entry_frame.grid(row = 0, column = 0)

options_frame = tkinter.Frame(main_window)
options_frame.grid(row = 1, column = 0, sticky="we")

options_command_frame = tkinter.LabelFrame(main_window, text="Actions", borderwidth=2)
options_command_frame.grid(row = 2, column = 0, sticky="we")

progress_frame = tkinter.Frame(main_window)
progress_frame.grid(row = 3, column = 0)

action_frame = tkinter.Frame(main_window)
action_frame.grid(row = 4, column = 0)

label_src = tkinter.Label(entry_frame, text="Répertoire source")
entry_src = tkinter.Entry(entry_frame, width=80, textvariable=folder_src)
folder_src.set(current_path)
button_src = tkinter.Button(entry_frame, text="Répertoire", command=lambda:browse_directory(folder_src, folder_dest, True))

label_dest = tkinter.Label(entry_frame, text="Répertoire de destination")
entry_dest = tkinter.Entry(entry_frame, width=80, textvariable=folder_dest)
folder_dest.set(destination_path)
button_dest = tkinter.Button(entry_frame, text="Répertoire", command=lambda:browse_directory(folder_src, folder_dest, False))

label_filters = tkinter.Label(entry_frame, text="Choisir les types de fichier")
entry_filters = tkinter.Entry(entry_frame, width=80, textvariable=filters)
filters.set("mp3,wma")

label_output = tkinter.Label(entry_frame, text="Fichier de sortie")
entry_output = tkinter.Entry(entry_frame, textvariable=file_output)
file_output.set("")

checkbox_display_path = tkinter.Checkbutton(options_frame, text="Afficher les noms des répertoires", variable=display_path)
checkbox_check_naming = tkinter.Checkbutton(options_frame, text="Vérifier le nommage", variable=check_naming)
display_path.set(0)
check_naming.set(0)

checkbox_organise_files = tkinter.Checkbutton(options_command_frame, text="Organiser les fichiers dans le répertoire de sortie", variable=organise_files)
organise_files.set(0)
radio_create_command = tkinter.Radiobutton(options_command_frame, text="Fichier de commandes", value = 0, variable=command_option)
radio_execute_command = tkinter.Radiobutton(options_command_frame, text="Exécuter les commandes", value = 1, variable=command_option)
command_option.set(1)

progress_button = tkinter.ttk.Progressbar(progress_frame, orient="horizontal", length=(window_x-10), variable=command_progress)
command_progress.set(0)

control_button = tkinter.Button(action_frame, text="Lancer la commande", command=execute_command)

label_src.grid(row = 0, column = 0, sticky="w")
entry_src.grid(row = 0, column = 1)
button_src.grid(row = 0, column = 2)

label_dest.grid(row = 1, column = 0, sticky="w")
entry_dest.grid(row = 1, column = 1)
button_dest.grid(row = 1, column = 2)

label_filters.grid(row = 2, column = 0, sticky="w")
entry_filters.grid(row = 2, column = 1)

label_output.grid(row = 3, column = 0, sticky="w")
entry_output.grid(row = 3, column = 1, sticky="w")

checkbox_display_path.grid(row = 0, column = 0, sticky="w")
checkbox_check_naming.grid(row = 0, column = 1, sticky="w")

checkbox_organise_files.grid(row=0, column = 0, columnspan=2, sticky="w")
radio_create_command.grid(row=1, column=0, sticky="w")
radio_execute_command.grid(row=1, column=1, sticky="w")

progress_button.grid(row = 0, column = 0, padx = 5, sticky="w")

control_button.grid(row = 0, column = 0, padx = 5, sticky="we")

#Launch main screen
main_window.mainloop()