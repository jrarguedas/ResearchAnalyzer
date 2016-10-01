# !/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# ResearchAnalyzer: Data Analyzer for ResearchLogger
# Copyright (C) 2016  Roxana Lafuente <roxana.lafuente@gmail.com>
#
# ResearchAnalyzer is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# ResearchAnalyzer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################
from loginfo import LogInfo
import os

path = os.getcwd()
# Data from one subject.
# LogInfo needs: - Detailed log file path.
#                - Click images file path.
#                - System log file path.
li = LogInfo(path + "YOUR_CLICK_DATA_HERE",
             path + "YOUR_KEYSTROKE_DATA_HERE",
             path + "YOUR_SYSTEM_LOG_DATA_HERE")
# Print clicks summary info.
print "Unique pressed clicks:", li.get_unique_pressed_clicks()
print
print "In-order pressed clicks:", li.get_all_pressed_clicks()
print
print li.get_click_info()
print path + "YOUR_CLICK_DATA_HERE"
li.print_click_summary()

# Print keys summary info.
print "Unique pressed keys:", li.get_unique_pressed_keys()
print
print "In-order pressed keys:"
for f in li.get_all_pressed_keys():
    keystroke, event_type, window, window_title = f
    print window, ":\t", window_title, "\t", event_type, "\t", keystroke
for f in li.get_letter_info():
    print f
li.print_key_summary()
# Phases
print li.get_orientation_info()
print li.get_drafting_info()
print li.get_orientation_info()
print li.get_total_session_time()
li.print_phases_summary()
li.print_pauses()
li.print_pause_summary()