import adminfile
import os

def check_image_log(click_images_log_path):
    clicksfile = adminfile.readfile(click_images_log_path)
    clicksfile = clicksfile.replace("mouse left up", "left_up")
    clicksfile = clicksfile.replace("mouse left down", "left_down")
    clicksfile = clicksfile.replace("mouse right up", "left_up")
    clicksfile = clicksfile.replace("mouse right down", "left_down")
    clicksfile = clicksfile.replace("mouse middle down", "middle_down")
    clicksfile = clicksfile.replace("mouse middle up", "middle_up")

    pipe = 0
    comma = 0
    clicksfile_adds = ""
    for i in range(0, clicksfile.__len__()):
        char = clicksfile[i]

        if pipe == 5 and clicksfile[i-1] == "|":
            if char == "|":
                pipe += 1
                clicksfile_adds += "|"
            else:
                clicksfile_adds += char
        elif pipe == 7:
            if comma == 4:
                if char == "g":
                    temp = clicksfile[i-3] + clicksfile[i-2] + clicksfile[i-1] + char
                    if temp == ".png":
                        comma = 0
                        clicksfile_adds += char
                    else:
                        clicksfile_adds += char
                elif char == " ":
                    clicksfile_adds += "_"
                elif char == "\n":
                    clicksfile_adds += "\\n"
                else:
                    clicksfile_adds += char
            elif char == ",":
                clicksfile_adds += char
                comma += 1
            else:
                clicksfile_adds += char
        elif char == "|":
            pipe += 1
            clicksfile_adds += char
        elif char == "\n":
            pipe = 0
            clicksfile_adds += char
        else:
            clicksfile_adds += char


    if "_new" in click_images_log_path:
        adminfile.writefile(click_images_log_path, clicksfile_adds)

    else:
        click_images_log_path = click_images_log_path.replace(".txt", "_new.txt")
        adminfile.writefile(click_images_log_path, clicksfile_adds)

    return click_images_log_path