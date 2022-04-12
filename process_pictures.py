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
    temp = compl_process.stdout.decode('utf8')
    temp_json = json.loads(temp)
    doctype = temp_json["type"]
    conf = 0.0
    is_rejected = True
    for key in temp_json["match"]["templates"]:
        try:
            conf = temp_json["match"]["templates"][key]["confidence"]
            is_rejected = False if temp_json["match"]["templates"][key]["is_rejected"] == False else True
            processed = True
            break
        except:
            continue
    if conf == 0.0000:
        processed = False
    return doctype, conf, is_rejected, processed


def process_sample(df, exe_path, bundle_path):
    config = load_config(exe_path, bundle_path)
    img_path = []
    doctype = []
    guessed_doctype = []
    rejected = []
    confidence = []
    is_processed = []
    total_unprocessed = 0
    i = 0
    for image in tqdm.tqdm(df["Image path"]):
        img_path.append(image)
        g_doctype, g_confidence, is_rejected, processed = process_picture(image, config)
        if processed == False:
            total_unprocessed += 1
            is_processed.append(False)
        else:
            is_processed.append(True)
        guessed_doctype.append(g_doctype)
        rejected.append(is_rejected)
        confidence.append(g_confidence)
        doctype.append(df["Document Type"][i])
        i+=1
    res = pd.DataFrame({"Image path": img_path, "Document Type": doctype, \
        "Processed Document Type": guessed_doctype, "Is rejected": rejected, "Confidence" : confidence, "Is processed" : is_processed})
    return res, total_unprocessed

def process_result(res):
    #build roc curve
    return 0

