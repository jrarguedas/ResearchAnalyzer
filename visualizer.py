from loginfo import LogInfo
from html_injector import *
from mixed_parser import *
import os
import json
import datetime
import webbrowser
from text_reconstruction import TextReconstructor

class Visualizer():
    def __init__(self):

        self.global_id = 0
        self.group_names = []

        self.path = os.getcwd() + "/example_log/"
        # Data from one subject.
        # LogInfo needs: - Detailed log file path.
        #                - Click images file path.
        #                - Timed screenshot file path.
        #                - System log file path.

        self.li = LogInfo(self.path + "click_images/clickimagelogfile_zxysp.txt", # Your click data file here
                     self.path + "detailed_log/detailedlogfile_zxysp.txt", # Your detailed log file here
                     self.path + "timed_screenshots/timedscreenshootlogfile_zxysp.txt", # Your timed screenshot log file here
                     self.path + "system_log/system_log_zxysp.txt") # Your system log data here

        self.injector = HTML_Injector()
        self.parse_and_inject_clicks_into_HTML()
        self.parse_and_inject_sentences_into_HTML()
        self.injector.injectIntoHTML()

        webbrowser.open("visualization/index.html",new=2)

    def parse_and_inject_clicks_into_HTML(self):
        stylized_group_names = {"left":"Left Clicks","right":"Right Clicks"}
        self.group_names.extend(["right", "left"])

        neccesary_clicks_information = []
        for clickinfo in self.li.get_click_info_for_visualization():
            self.global_id += 1

            click_type = clickinfo[0]

            splitted_image_title = clickinfo[2].split('_')
            date = datetime.datetime.strptime(splitted_image_title[0], "%Y%m%d").date()
            hour = str(datetime.datetime.strptime(splitted_image_title[1], "%H%M%S")).split(' ')[1]
            start_timestamp = str(date) + ' ' + hour
            end_timestamp = start_timestamp

            neccesary_click_information = {}
            neccesary_click_information["id"] = self.global_id
            neccesary_click_information["content"] = ""
            neccesary_click_information["start"] = start_timestamp
            neccesary_click_information["end"] = end_timestamp
            neccesary_click_information["group"] = self.group_names.index(click_type)
            neccesary_click_information["type"] = "box"
            neccesary_click_information["click_image"] =  self.path + "click_images/" + clickinfo[2]
            neccesary_clicks_information.append(neccesary_click_information)
        self.injector.prepareForHTML(json.dumps(neccesary_clicks_information),stylized_group_names.values(),"clicks")

    def parse_and_inject_sentences_into_HTML(self):
        neccesary_sentences_information = []
        stylized_group_names = {}
        for sentence_info in  self.li.get_clustered_keys():
            self.global_id += 1

            start_timestamp = sentence_info[1]
            end_timestamp = sentence_info[2]
            window_name = sentence_info[3]
            if window_name not in self.group_names:
                self.group_names.append(window_name)
                stylized_group_names[window_name] = "Sentences written in " + window_name

            neccesary_sentence_information = {}
            neccesary_sentence_information["id"] = self.global_id
            neccesary_sentence_information["content"] = ' <span style="color:#97B0F8;">' + sentence_info[0] + '</span>'
            neccesary_sentence_information["start"] = start_timestamp
            neccesary_sentence_information["end"] = end_timestamp
            neccesary_sentence_information["group"] = self.group_names.index(window_name)
            neccesary_sentence_information["type"] = "box"
            neccesary_sentences_information.append(neccesary_sentence_information)
        self.injector.prepareForHTML(json.dumps(neccesary_sentences_information),stylized_group_names.values(),"sentences")

if __name__ == "__main__":
    vis = Visualizer()
