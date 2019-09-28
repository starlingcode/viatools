from patterns import Pattern

import sys
from shutil import copyfile

worker_bee = Pattern()

worker_bee.generate_gateseq_code()

if (len(sys.argv)) > 1:

    if sys.argv[1] == "copy":

        copyfile("/vagrant/viatools/generated_code/boolean_sequences.hpp",
                 "/vagrant/via_hardware_executables/hardware_drivers/Via/modules/inc/boolean_sequences.hpp")

        copyfile("/vagrant/viatools/generated_code/gateseq_pattern_init.cpp",
                 "/vagrant/via_hardware_executables/hardware_drivers/Via/modules/gateseq/gateseq_pattern_init.cpp")

