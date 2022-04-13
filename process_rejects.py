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
    if result["Document Type"][i] == doctypes_vocab[result["Processed Document Type"][i]]:
        return True
    else:
        return False

def get_tpr(result, thresh):
    total_p = 0
    total_tp = 0
    for i in range(len(result["Image path"])):
        if not match_doctypes(result, i):
            total_p += 1
            if result["Confidence"][i] < thresh:
                total_tp += 1
    return total_tp / total_p


def get_fpr(result, thresh):
    total_n = 0
    total_fp = 0
    for i in range(len(result["Image path"])):
        if match_doctypes(result, i):
            total_n += 1
            if result["Confidence"][i] < thresh:
                total_fp += 1
    return total_fp / total_n

def get_roc_curve(data, margin):
    points = []
    for i in range(0, 100, margin*100):
        points.append([get_tpr(data, i/100), get_fpr(data, i/100)])
    return points