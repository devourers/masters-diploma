from concurrent.futures import process
from re import I
from signal import raise_signal
import tqdm
import pandas as pd
import subprocess

def load_config(bundle_path, exe_path):
    """
    May be use as a config class for some additional options
    """
    return [bundle_path, exe_path]

def form_command(image_path, config):
    return ""
    '''
    config[0] + ' -i' + image_path + ....
    '''

def process_reject_data(path):
    return ""
    '''
    with open(path_to_reject_data) as f:
        #do smth
        return reject_data
    '''

def process_picture(image_path, config):
    proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    command = form_command(image_path, config)
    stdout, stderr = "", "" #proc.communicate(command)
    path_to_reject_data = ""
    doctype = "" #get doctype from stdout or stderr or file
    rejected_data = False #process_reject_data(path_to_reject_data)
    return doctype, rejected_data


def process_sample(df, bundle_path, exe_path):
    config = load_config(bundle_path, exe_path)
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

