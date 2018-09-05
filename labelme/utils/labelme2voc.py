from __future__ import print_function

import argparse
import glob
import json
import os
import os.path as osp
import csv

import numpy as np
import PIL.Image

import labelme


def exportVOC_instance(labels_file, in_dir, out_dir):
    if osp.exists(out_dir):
        print('Output directory already exists:', out_dir)
        return 1
    os.makedirs(out_dir)
    os.makedirs(osp.join(out_dir, 'JPEGImages'))
    os.makedirs(osp.join(out_dir, 'SegmentationClass'))
    os.makedirs(osp.join(out_dir, 'SegmentationClassPNG'))
    os.makedirs(osp.join(out_dir, 'SegmentationClassVisualization'))
    os.makedirs(osp.join(out_dir, 'SegmentationObject'))
    os.makedirs(osp.join(out_dir, 'SegmentationObjectPNG'))
    os.makedirs(osp.join(out_dir, 'SegmentationObjectVisualization'))
    print('Creating dataset:', out_dir)

    class_names = []
    class_name_to_id = {}
    for i, line in enumerate(open(labels_file).readlines()):
        class_id = i - 1  # starts with -1
        class_name = line.strip()
        class_name_to_id[class_name] = class_id
        if class_id == -1:
            assert class_name == '__ignore__'
            continue
        elif class_id == 0:
            assert class_name == '_background_'
        class_names.append(class_name)
    class_names = tuple(class_names)
    print('class_names:', class_names)
    out_class_names_file = osp.join(out_dir, 'class_names.txt')
    out_class_csv_file = osp.join(out_dir, 'class_dict.csv')
    with open(out_class_names_file, 'w') as f:
        f.writelines('\n'.join(class_names))
    print('Saved class_names:', out_class_names_file)

    colormap = labelme.utils.label_colormap(255)

    rgb_dict = []
    for label_file in glob.glob(osp.join(in_dir, '*.json')):
        print('Generating dataset from:', label_file)
        with open(label_file) as f:
            base = osp.splitext(osp.basename(label_file))[0]
            out_img_file = osp.join(
                out_dir, 'JPEGImages', base + '.jpg')
            out_cls_file = osp.join(
                out_dir, 'SegmentationClass', base + '.npy')
            out_clsp_file = osp.join(
                out_dir, 'SegmentationClassPNG', base + '.png')
            out_clsv_file = osp.join(
                out_dir, 'SegmentationClassVisualization', base + '.jpg')
            out_ins_file = osp.join(
                out_dir, 'SegmentationObject', base + '.npy')
            out_insp_file = osp.join(
                out_dir, 'SegmentationObjectPNG', base + '.png')
            out_insv_file = osp.join(
                out_dir, 'SegmentationObjectVisualization', base + '.jpg')

            data = json.load(f)

            img_file = osp.join(osp.dirname(label_file), data['imagePath'])
            img = np.asarray(PIL.Image.open(img_file))
            PIL.Image.fromarray(img).save(out_img_file)

            cls, ins = labelme.utils.shapes_to_label(
                img_shape=img.shape,
                shapes=data['shapes'],
                label_name_to_value=class_name_to_id,
                type='instance',
            )
            ins[cls == -1] = 0  # ignore it.

            # class label
            labelme.utils.lblsave(out_clsp_file, cls)
            np.save(out_cls_file, cls)
            clsv, rgb_info = labelme.utils.draw_label(
                cls, img, class_names, colormap=colormap, csvFilePath=out_class_csv_file)
            l = len(rgb_info)
            for i in range(l):
                if rgb_info[i] not in rgb_dict:
                    rgb_dict.append(rgb_info[i])
            PIL.Image.fromarray(clsv).save(out_clsv_file)

            # instance label
            labelme.utils.lblsave(out_insp_file, ins)
            np.save(out_ins_file, ins)
            instance_ids = np.unique(ins)
            instance_names = [str(i) for i in range(max(instance_ids) + 1)]
            insv = labelme.utils.draw_label(ins, img, instance_names)
            PIL.Image.fromarray(insv).save(out_insv_file)
    fo = open(out_class_csv_file, 'w')
    writer=csv.writer(fo)
    m = len(rgb_dict)
    for i in range(m):
        writer.writerow(rgb_dict[i])
    fo.close()
    print('...... Finish exporting tasks for:', out_dir)

def exportVOC_semantic(labels_file, in_dir, out_dir):
    if osp.exists(out_dir):
        print('Output directory already exists:', out_dir)
        return 1
    os.makedirs(out_dir)
    os.makedirs(osp.join(out_dir, 'JPEGImages'))
    os.makedirs(osp.join(out_dir, 'SegmentationClass'))
    os.makedirs(osp.join(out_dir, 'SegmentationClassPNG'))
    os.makedirs(osp.join(out_dir, 'SegmentationClassVisualization'))
    print('Creating dataset:', out_dir)

    class_names = []
    class_name_to_id = {}
    for i, line in enumerate(open(labels_file).readlines()):
        class_id = i - 1  # starts with -1
        class_name = line.strip()
        class_name_to_id[class_name] = class_id
        if class_id == -1:
            assert class_name == '__ignore__'
            continue
        elif class_id == 0:
            assert class_name == '_background_'
        class_names.append(class_name)
    class_names = tuple(class_names)
    print('class_names:', class_names)
    out_class_names_file = osp.join(out_dir, 'class_names.txt')
    out_class_csv_file = osp.join(out_dir, 'class_dict.csv')
    with open(out_class_names_file, 'w') as f:
        f.writelines('\n'.join(class_names))
    print('Saved class_names:', out_class_names_file)

    colormap = labelme.utils.label_colormap(255)
    rgb_dict = []
    for label_file in glob.glob(osp.join(in_dir, '*.json')):
        print('Generating dataset from:', label_file)
        with open(label_file) as f:
            base = osp.splitext(osp.basename(label_file))[0]
            out_img_file = osp.join(
                out_dir, 'JPEGImages', base + '.jpg')
            out_lbl_file = osp.join(
                out_dir, 'SegmentationClass', base + '.npy')
            out_png_file = osp.join(
                out_dir, 'SegmentationClassPNG', base + '.png')
            out_viz_file = osp.join(
                out_dir, 'SegmentationClassVisualization', base + '.jpg')

            data = json.load(f)

            img_file = osp.join(osp.dirname(label_file), data['imagePath'])
            img = np.asarray(PIL.Image.open(img_file))
            PIL.Image.fromarray(img).save(out_img_file)

            lbl = labelme.utils.shapes_to_label(
                img_shape=img.shape,
                shapes=data['shapes'],
                label_name_to_value=class_name_to_id,
            )
            labelme.utils.lblsave(out_png_file, lbl)

            np.save(out_lbl_file, lbl)

            viz, rgb_info = labelme.utils.draw_label(
                lbl, img, class_names, colormap=colormap, csvFilePath=out_class_csv_file)
            l = len(rgb_info)
            for i in range(l):
                if rgb_info[i] not in rgb_dict:
                    rgb_dict.append(rgb_info[i])
            PIL.Image.fromarray(viz).save(out_viz_file)
    fo = open(out_class_csv_file, 'w')
    writer=csv.writer(fo)
    m = len(rgb_dict)
    for i in range(m):
        writer.writerow(rgb_dict[i])
    fo.close()
    print('...... Finish exporting tasks for:', out_dir)
