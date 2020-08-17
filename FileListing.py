from os import listdir
from os.path import isfile, join
import os
import os.path
from shutil import copyfile, copy

class PathExplorer(object):
    """Explore the current Path"""

    #constructor
    #folder_src: source directory
    #filters: extensions to take into consideration
    #display_path: int used to tell us if we print the full path or not
    #check_naming: int used to tell us if we check the naming convention
    #command_progress: handles the progress bar progression
    #is_execute: if true execute command, otherwise write command file
    def __init__(self, folder_src, filters, display_path, check_naming, command_progress, is_execute):
        self.folder_src = folder_src
        self.filters = filters
        self.file_dico = dict()
        self.display_path = display_path
        self.check_naming = check_naming
        self.command_progress = command_progress
        self.is_execute = is_execute

    #output_file_name full path of the output file (if string is empty then print in the console)
    def PrintFiles(self, output_file_name):
        if len(self.file_dico) == 0:
            self.__GetInternalFiles("", self.folder_src)
        self.__PrintResult(output_file_name)

    #destination_path: full path to the destionation folder
    def Classify(self, destination_path, output_file_name):
        if len(self.file_dico) == 0:
            self.__GetInternalFiles("", self.folder_src)
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        self.__create_structure(destination_path, output_file_name)

    def __create_structure(self, destination_path, output_file_name):
        file_dico_keys = self.file_dico.keys()
        nb_dico_items = len(file_dico_keys)
        nb_element_handled = 0
        if self.is_execute:
            output_full_path = ""
        else:
            if len(output_file_name) > 0:
                output_full_path = output_file_name + ".bat"
            else:
                output_full_path = "command.bat"
            output_full_path = join(destination_path, output_full_path)
        with Writer(output_full_path) as writer:
            for file_name in file_dico_keys:
                nb_element_handled += 1
                last_occurence = file_name.rfind('-')
                if last_occurence<1:
                    continue
                directory_name = file_name[0:last_occurence-1].strip()
                full_source = self.file_dico[file_name][0]
                full_destination = join(destination_path, directory_name)
                if not os.path.exists(full_destination):
                    self.__make_directory(full_destination, writer)
                self.__copy_file(full_source, full_destination, writer)
                self.command_progress.set(100 * nb_element_handled / nb_dico_items)

    def __make_directory(self, full_path, writer):
        if self.is_execute:
            os.mkdir(full_path)
        else:
            writer.write("mkdir \"{0}\"\n".format(full_path))

    def __copy_file(self, full_source, full_destination, writer):
        if self.is_execute:
            copy(full_source, full_destination)
        else:
            writer.write("copy \"{0}\" \"{1}\"\n".format(full_source, full_destination))

    def __PrintResult(self, file_name):
        duplicated_files = []
        wrong_named_files = []
        sorted_files = sorted(iter(self.file_dico.keys()))
        #with behaves like the using statement in C#
        with Writer(file_name) as writer:
            for key in sorted_files:
                writer.write(key+"\n")
                self.__check_file_name(wrong_named_files, key)
                index = 0
                for value in self.file_dico[key]:
                    index += 1
                    if self.display_path:
                        writer.write("\t" + value + "\n")
                    if index > 1:
                        duplicated_files.append(key)

            self.__bad_file_name_warning(writer, wrong_named_files)
            self.__duplicated_file_warning(writer, duplicated_files)

    def __bad_file_name_warning(self, writer, wrong_named_files):
        if len(wrong_named_files) > 0:
            writer.write("\n")
            writer.write("MAUVAIS NOMMAGE:\n")
            writer.write("\n")
            for file_name in wrong_named_files:
                writer.write(file_name + "\n")

    def __duplicated_file_warning(self, writer, duplicated_files):
        if len(duplicated_files) > 0:
            writer.write("\n")
            writer.write("FICHIERS DUPLIQUÉS:\n")
            writer.write("\n")
            for file_name in duplicated_files:
                writer.write(file_name + "\n")
                for value in self.file_dico[file_name]:
                    writer.write("\t" + value + "\n")

    def __check_file_name(self, wrong_named_files, file_name):
        if self.check_naming:
            last_occurence = file_name.rfind('-')
            if last_occurence == -1 or last_occurence == len(file_name)-1:
                wrong_named_files.append(file_name)

    def __GetInternalFiles(self, currentDir, path):
        itemList = listdir(path)
        for item in itemList:
            fullPath = join(path, item)
            nextDir = join(currentDir,item)
            if isfile(fullPath):
                if len(self.filters) == 0 or self.__GetExtension(item) in self.filters:
                    if item in self.file_dico:
                        self.file_dico[item].Add(fullPath)
                    else:
                        self.file_dico[item] = [fullPath]
            else:
                self.__GetInternalFiles(nextDir, fullPath)

    def __GetExtension(self, file_name):
        last_occurence = file_name.rfind('.')
        return file_name[last_occurence+1:]


class Writer(object):
    """Write data in the console or in a file"""

    def __init__(self, file_name):
        self.file_name = file_name
        self.store_file = len(file_name) > 0

    #called when declaring the with statement. It must return the instance of an object
    def __enter__(self):
        if self.store_file:
            self.file = open(self.file_name, "w")
        return self

    #called when exiting the with statement
    def __exit__(self, type, value, traceback):
        if self.store_file:
            self.file.close()

    def write(self, text):
        if self.store_file:
            self.file.write(text)
        else:
            print(text)


class FilePath(object):
    """Store information about the file"""

    def __init__(self, path, file_name):
        self.file_name = file_name
        self.path = path

    #used to format the class into a string
    def __str__(self):
        return self.GetFullPath()

    #used to represent the data content of the class
    def __repr__(self):
        return self.__str__()

    def GetFullPath(self):
        return join(self.path, self.file_name)