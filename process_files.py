from ntpath import join
import os
import tqdm
import pandas as pd
import json
import random
import process_pictures


def process_markup(image_folder, markup_path):
    img_path = []
    doctype = []
    template_quad = []
    with open(markup_path) as f:
        markup_data = json.load(f)
        pic_markup = markup_data["_via_img_metadata"]
        for key in markup_data["_via_image_id_list"]:
            img_path.append(image_folder + '\\' +pic_markup[key]["filename"])
            doctype.append(markup_data["_via_settings"]["project"]["name"])
            #process template_quad
            curr_quad = []
            for i in range(4):
                curr_quad.append([pic_markup[key]["regions"][1]["shape_attributes"]["all_points_x"][i],\
                     pic_markup[key]["regions"][1]["shape_attributes"]["all_points_y"][i]])
            template_quad.append(curr_quad)
    res = pd.DataFrame({"Image path": img_path, "Document Type": doctype, "Template Quad": template_quad})
    return res


def mix_markups(dataframes, img_count):
    img_path = []
    doctype = []
    template_quad = []
    while len(img_path) < img_count:
        df = dataframes[random.choice([i for i in range(len(dataframes))])]
        chce = random.choice([i for i in range(len(df))])
        img_path.append(df["Image path"][chce])
        doctype.append(df["Document Type"][chce])
        template_quad.append(df["Template Quad"][chce])
    res = pd.DataFrame({"Image path": img_path, "Document Type": doctype, "Template Quad": template_quad})
    return res

def join_dfs(markups):
    res = pd.concat(markups, ignore_index=True)
    return res


def load_all_markups(lst_file):
    markups = []
    with open(lst_file) as f:
        lines = f.readlines()
    for line in lines:
        folders_images = os.listdir(line+"\\images")
        folders_markup = os.listdir(line+"\\annotations")
        for i, j in zip(folders_images, folders_markup):
            markups.append(process_markup(line+"\\images\\" + i, line + "\\annotations\\" + j))
    return markups


def get_data(lst_file):
    markups = load_all_markups(lst_file)
    res = join_dfs(markups)
    return res


def copy_file(file):
    temp_file_path = ""
    with open("prefix.path") as prefix:
        temp_file_path = prefix.readline().strip()
    temp_file_path += "\\data\\temp\\temp.desc"
    file_list = file.split('\\')
    if "rus" in file_list[-2]:
        return
    file_desc_path = file_list[0] + '\\' + file_list[1] + '\\' + file_list[2] + '\\' + file_list[3] + "\\descriptors\\images\\" + file_list[-2] + "\\" + (file_list[-1].split('.')[0] + ".desc")
    temp_f = open(file_desc_path, 'w')
    temp_f.close()
    with open(temp_file_path, 'rb') as r_f:
        with open(file_desc_path, 'wb') as w_f:
            byte = r_f.read(1)
            while byte != b"":
                w_f.write(byte)
                byte = r_f.read(1)
        w_f.close()
    r_f.close()

            

def save_descs(config):
    loaded_markups = get_data("folders.lst")
    images = loaded_markups["Image path"]
    for image in tqdm.tqdm(images):
        process_pictures.process_picture(image, config)
        copy_file(image)

