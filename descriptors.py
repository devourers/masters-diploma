import tqdm
import os
import sys
from multiprocessing import Pool

BYTES_COUNTER = 16

def keypoint_distance_wrapper(kps):
    return keypoint_distance(kps[0], kps[1])

def keypoint_distance(keypoint1, keypoint2):
    res = 0
    for i in range(len(keypoint1)):
        c1 = bin(int.from_bytes(keypoint1[i], byteorder=sys.byteorder))[2:].zfill(8)
        c2 = bin(int.from_bytes(keypoint2[i], byteorder=sys.byteorder))[2:].zfill(8)
        cur_dist = 0
        for j in range(len(c1)):
            if c1[j] != c2[j]:
                cur_dist += 1
        res += cur_dist
    return res

def distance_matrix(keypoints1, keypoints2):
    res = [[0 for i in keypoints2] for j in keypoints1]
    #pool = Pool()
    for id_1, keypoint1 in enumerate(keypoints1):
        #res[id_1] = pool.map(keypoint_distance_wrapper, [(keypoint1, keypoint2) for keypoint2 in keypoints2])
        for id_2, keypoint2 in enumerate(keypoints2):
            res[id_1][id_2] = keypoint_distance(keypoint1, keypoint2)
    return res
    
def distance(keypoints1, keypoints2):
    DM = distance_matrix(keypoints1, keypoints2)
    n = len(DM)
    if n == 0:
        return -10
    m = len(DM[0])
    minimum = DM[0][0]
    min_i = 0
    min_j = 0
    for i in range(n):
        for j in range(m):
            if DM[i][j] < minimum:
                minimum = DM[i][j]
                min_i = i
                min_j = j
    sup_x_xy = max(DM[min_i])
    DM_col = [DM[k][min_j] for k in range(n)]
    sup_y_xy = max(DM_col)
    return max(sup_x_xy, sup_y_xy)

def load_keypoints(path):
    res = []
    curr_res = []
    with open(path, 'rb') as f:
        byte = f.read(1)
        curr_res.append(byte)
        while byte != b"":
            byte = f.read(1)
            curr_res.append(byte)
            if len(curr_res) == BYTES_COUNTER:
                res.append(curr_res)
                curr_res = []
    return res

def load_templates(prefix):
    res = []
    templates_path = prefix+"data\\descriptors\\templates"
    dirs = os.listdir(templates_path)
    for tmp in dirs:
        file = os.listdir( templates_path + "\\" + tmp)
        descrs = load_keypoints(templates_path + "\\" + tmp + "\\" + file[0])
        res.append([tmp, descrs])
    return res

def load_files(prefix):
    res = []
    files_path = prefix+"data\\descriptors\\images"
    dirs = os.listdir(files_path)
    for dr in dirs:
        files = os.listdir(files_path + "\\" + dr)
        for file in files:
            descrs = load_keypoints(files_path + "\\" + dr + "\\" + file)
            res.append([dr, file, descrs])
    return res

def distance_wrapper(item):
    decrs_file = item[0]
    template_name = item[1]
    decrs_template = item[2]
    dist = distance(decrs_file, decrs_template)
    return template_name, dist

def process_file(doc, name, decrs_file, templates):
    res = []
    for template in templates:
        template_name = template[0]
        decrs_template = template[1]
        dist = distance(decrs_file, decrs_template)
        res.append([template_name, dist])
    return [doc, name, res]

def process_file_wrapper(item):
    doc = item[0]
    name = item[1]
    decrs_file = item[2]
    templates = item[3]
    return process_file(doc, name, decrs_file, templates)

def process_files(prefix):
    res = dict()
    templates = load_templates(prefix)
    files = load_files(prefix)
    print("loaded files, processing...")
    pool = Pool()
    results = tqdm.tqdm(pool.imap_unordered(process_file_wrapper, [(file[0], file[1], file[2], templates) for file in files]), total=len(files))
    results = list(results)
    for r in results:
        res.setdefault(r[0], dict())
        res[r[0]].setdefault(r[1], dict())
        for t in r[2]:
            print(t[0], t[1])
            res[r[0]][r[1]].setdefault(t[0], t[1])
    #for file in (pbar:= tqdm.tqdm(files)):
    #    doc = file[0]
    #    name = file[1]
    ##    pbar.set_postfix_str(doc + "/" + name)
    #    decrs_file = file[2]
    #    res.setdefault(doc, dict())
    #    res[doc].setdefault(name, dict())#

    #    cur_res = pool.map(distance_wrapper, [(decrs_file, template[0], template[1]) for template in templates])
    #    for r in cur_res:
    #        res[doc][name].setdefault(r[0], r[1])
        #for template in templates:
        #    template_name = template[0]
        #    decrs_template = template[1]
        #    dist = distance(decrs_file, decrs_template)
        #    res[doc][name].setdefault(template_name, dist)
    return res