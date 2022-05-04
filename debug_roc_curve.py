import random
import pandas as pd
from torch import rand

def form_random_sample(df):
    image_path = []
    is_rejected = []
    is_processed = []
    right_doc_type = []
    processed_doc_type = []
    conf = []
    for i in range(len(df["Image path"])):
        image_path.append(df["Image path"][i])
        right_doc_type.append(df["Document Type"][i])
        processed_doc_type.append(df["Processed Document Type"][i])
        is_rejected.append(df["Is rejected"][i])
        is_processed.append(df["Is processed"][i])
        conf.append(random.randint(0, 100) / 100)
    res_df = pd.DataFrame({"Image path" : image_path, "Document Type" : right_doc_type,\
         "Processed Document Type" : processed_doc_type, "Is rejected" : is_rejected, \
         "Confidence" : conf, "Is processed" : is_processed})
    return res_df
