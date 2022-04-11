from concurrent.futures import process
from re import I
import json
from signal import raise_signal
import tqdm
import pandas as pd
import subprocess

def load_config(exe_path, bundle_path):
    """
    May be use as a config class for some additional options
    """
    return [exe_path, bundle_path]

def form_command(image_path, config):
    return config[0] + " -l -c " + config[1] + " -i " + image_path
    #./smartid_run -l -c ../../../data/bundle_midv500_server.json -i ../../../testdata/engine_test/images/passport_anywhere_mrz.jpg

def process_reject_data(path):
    return ""
    '''
    with open(path_to_reject_data) as f:
        #do smth
        return reject_data
    '''

def process_picture(image_path, config):
    #proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE, encoding='utf8')
    command = form_command(image_path, config)
    compl_process = subprocess.run(command.split(' '), capture_output=True)
    path_to_reject_data = ""
    doctype = "" #get doctype from stdout or stderr or file
    rejected_data = False #process_reject_data(path_to_reject_data)
    temp = compl_process.stdout.decode('utf8')
    print(temp)
    return doctype, rejected_data


def process_sample(df, exe_path, bundle_path):
    config = load_config(exe_path, bundle_path)
    img_path = []
    doctype = []
    guessed_doctype = []
    rejected = []
    i = 0
    for image in df["Image path"]:
        img_path.append(image)
        g_doctype, is_rejected = process_picture(image, config)
        guessed_doctype.append(g_doctype)
        rejected.append(is_rejected)
        doctype.append(df["Document Type"][i])
        i+=1
    res = pd.DataFrame({"Image path": img_path, "Document Type": doctype, \
        "Processed Document Type": guessed_doctype, "Is rejected": rejected})
    return res

def process_result(res):
    #TODO
    return 0

