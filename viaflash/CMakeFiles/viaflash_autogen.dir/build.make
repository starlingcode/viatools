# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.9

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CMake.app/Contents/bin/cmake

# The command to remove a file.
RM = /Applications/CMake.app/Contents/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/willmitchell/Documents/wavetablegentools/viaflash

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/willmitchell/Documents/wavetablegentools/viaflash

# Utility rule file for viaflash_autogen.

# Include the progress variables for this target.
include CMakeFiles/viaflash_autogen.dir/progress.make

CMakeFiles/viaflash_autogen: /usr/local/Cellar/qt5/5.6.1/lib/QtWidgets.framework/QtWidgets
CMakeFiles/viaflash_autogen: ui_mainwindow.h
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/willmitchell/Documents/wavetablegentools/viaflash/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Automatic MOC for target viaflash"
	/Applications/CMake.app/Contents/bin/cmake -E cmake_autogen /Users/willmitchell/Documents/wavetablegentools/viaflash/CMakeFiles/viaflash_autogen.dir "Debug Release"

ui_mainwindow.h: mainwindow.ui
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/willmitchell/Documents/wavetablegentools/viaflash/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Generating ui_mainwindow.h"
	/usr/local/Cellar/qt5/5.6.1/bin/uic -o /Users/willmitchell/Documents/wavetablegentools/viaflash/ui_mainwindow.h /Users/willmitchell/Documents/wavetablegentools/viaflash/mainwindow.ui

viaflash_autogen: CMakeFiles/viaflash_autogen
viaflash_autogen: ui_mainwindow.h
viaflash_autogen: CMakeFiles/viaflash_autogen.dir/build.make

.PHONY : viaflash_autogen

# Rule to build all files generated by this target.
CMakeFiles/viaflash_autogen.dir/build: viaflash_autogen

.PHONY : CMakeFiles/viaflash_autogen.dir/build

CMakeFiles/viaflash_autogen.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/viaflash_autogen.dir/cmake_clean.cmake
.PHONY : CMakeFiles/viaflash_autogen.dir/clean

CMakeFiles/viaflash_autogen.dir/depend:
	cd /Users/willmitchell/Documents/wavetablegentools/viaflash && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/willmitchell/Documents/wavetablegentools/viaflash /Users/willmitchell/Documents/wavetablegentools/viaflash /Users/willmitchell/Documents/wavetablegentools/viaflash /Users/willmitchell/Documents/wavetablegentools/viaflash /Users/willmitchell/Documents/wavetablegentools/viaflash/CMakeFiles/viaflash_autogen.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/viaflash_autogen.dir/depend

