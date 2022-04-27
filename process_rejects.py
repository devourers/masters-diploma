import tqdm
import pandas as pd

doctypes_vocab = {"alb.id.type1" : "alb_id",
                    "aze.passport.type2" : "aze_passport",
                    "esp.id.type1" : "esp_id",
                    "est.id.type1" : "est_id",
                    "fin.id.type1" : "fin_id",
                    "grc.passport.type1" : "grc_passport",
                    "lva.passport.type1" : "lva_passport",
                    "rus.passport.national" : "rus_internalpassport",
                    "srb.passport.type1" : "srb_passport",
                    "svk.id.type1" : "svk_id",
                    "" : "" } #debug

def match_doctypes(result, i):
    try:
        if result["Document Type"][i] == doctypes_vocab[result["Processed Document Type"][i].split(":")[0]] and result["Document Type"][i] != "":
            return True
        else:
            return False
    except:
        return False

def conf_score(num_inliers):
    if num_inliers != 0:
        return (max(0, num_inliers - 4))/num_inliers #TODO
    else:
        return 0.0

def process_rejected_file(df, file):
    with open(file, encoding="utf8") as f:
        lines = [line.strip() for line in f.readlines()]
    index = 0
    max_inliers = 0
    max_tpl = ""
    for line in lines:
        if line != "------":
            if int(line.strip().split(' | ')[0]) > max_inliers:
                max_inliers = int(line.strip().split(' | ')[0])
                max_tpl = line.strip().split(' | ')[1]
        else:
            df["Processed Document Type"][index] = max_tpl.split(":")[0]
            df["Confidence"][index] = conf_score(max_inliers)
            max_inliers = 0
            max_tpl = ""
            index += 1
    return df


def fix_df(unproc_df, df):
    counter = 0
    for line in unproc_df["Unnamed: 0"]:
        df["Processed Document Type"][line] = unproc_df["Processed Document Type"][counter]
        df["Confidence"][line] = unproc_df["Confidence"][counter]
        counter += 1
    return df

def get_tpr(result, thresh):
    total_p = 0
    total_tp = 0
    for i in range(len(result["Image path"])):
        if not match_doctypes(result, i):
            total_p += 1
            if result["Confidence"][i] < thresh:
                total_tp += 1
    if total_p != 0:
        return total_tp / total_p
    else:
        return 0.0


def get_fpr(result, thresh):
    total_n = 0
    total_fp = 0
    for i in range(len(result["Image path"])):
        if match_doctypes(result, i):
            total_n += 1
            if result["Confidence"][i] < thresh:
                total_fp += 1
    if total_n != 0:
        return total_fp / total_n
    else:
        return 0.0

def get_roc_curve(data, margin):
    points = []
    for i in range(0, 100, int(margin*100)):
        points.append([get_fpr(data, i/100), get_tpr(data, i/100)])
    return points