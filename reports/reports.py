#ill do it tomorrow :)

import json
from json2html import *

def txt_to_json():
    filename = "global_console_output.txt"

    dict1 = {}
    
    # creating dictionary
    with open(filename) as fh:
    
        for line in fh:
    
            # reads each line and trims of extra the spaces 
            # and gives only the valid words
            if not line.isspace():
                command, description = line.strip().split(None, 1)
                dict1[command] = description.strip()
    
    # creating json file
    # the JSON file is named as test1
    out_file = open("RMS_console_output.json", "w")
    json.dump(dict1, out_file, indent = 4, sort_keys = False)
    out_file.close()

#txt_to_json()
with open("result.json") as f:
    d = json.load(f)
    scanOutput = json2html.convert(json=d)
    scanOutput = scanOutput.replace('<td>False</td>', '<td class="red">False</td>')
    htmlReportFile = "output.html"
    with open(htmlReportFile, 'w') as htmlfile:
        htmlfile.write(str(scanOutput))
        print("Json file is converted")

