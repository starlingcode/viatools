import sys
import os
from shutil import copytree


def copy_and_rename(module_name, read_file, write_file):

    with open(read_file) as readFile:
        s = readFile.read()
        s = s.replace('emptyvia', module_name)
        s = s.replace('Emptyvia', module_name.title())
        s = s.replace('EMPTYVIA', module_name.upper())
        with open(write_file, "w") as file:
            file.write(s)


# Get Via firmware directory path from command line argument or use defualt
if len(sys.argv) > 1:
    firmware_project = sys.argv[1]
else:
    firmware_project = "/vagrant/via_hardware_executables/"

# Get new module name
module_name = str(input("Enter the module name in all lower case: "))

firmware_source_path = firmware_project + "/" + module_name
template_source_path = firmware_project + "/emptyvia"

copytree(firmware_project + "/emptyvia", firmware_source_path)

# firmware project metadata
filepath = firmware_source_path + "/.project"
source = template_source_path + "/.project"
copy_and_rename(module_name, source, filepath)

# headless makefile
filepath = firmware_source_path + "/makefile"
source = template_source_path + "/makefile"
copy_and_rename(module_name, source, filepath)

# main executable file
filepath = firmware_source_path + "/src/main.cpp"
source = template_source_path + "/src/main.cpp"
copy_and_rename(module_name, source, filepath)

# interrupt link
filepath = firmware_source_path + "/src/interrupt_link.cpp"
source = template_source_path + "/src/interrupt_link.cpp"
copy_and_rename(module_name, source, filepath)

# module header
filepath = firmware_project + "/hardware_drivers/Via/modules/inc/" + module_name + ".hpp"
source = firmware_project + "/hardware_drivers/Via/modules/inc/emptyvia.hpp"
copy_and_rename(module_name, source, filepath)

# module source
filepath = firmware_project + "/hardware_drivers/Via/modules/" + module_name
os.mkdir(filepath)

# ui handlers
uifilepath = filepath + "/" + module_name + "_ui_implementation.cpp"
source = firmware_project + "/hardware_drivers/Via/modules/emptyvia/emptyvia_ui_implementation.cpp"
copy_and_rename(module_name, source, uifilepath)

# mode stubs
modesfilepath = filepath + "/" + module_name + "_modes.cpp"
source = firmware_project + "/hardware_drivers/Via/modules/emptyvia/emptyvia_modes.cpp"
copy_and_rename(module_name, source, modesfilepath)

if len(sys.argv) > 2:
    rack_export = sys.argv[2]
else:
    rack_export = "/vagrant/rack_clones/"

os.makedirs(rack_export, exist_ok=True)

filepath = rack_export + "/" + module_name + ".cpp"
source = os.path.realpath(__file__) + "/module_templates/emptyvia.cpp"
copy_and_rename(module_name, source, filepath)

