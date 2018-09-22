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


def exportMITP_grasp(labels_file, in_dir, out_dir):
    if osp.exists(out_dir):
        print('Output directory already exists:', out_dir)
        return 1
    os.makedirs(out_dir)
    os.makedirs(osp.join(out_dir, 'JPEGImages'))
    os.makedirs(osp.join(out_dir, 'MITPrincetonGraspingClass'))
    os.makedirs(osp.join(out_dir, 'MITPrincetonGraspingClassPNG'))
    os.makedirs(osp.join(out_dir, 'MITPrincetonGraspingClassVisualization'))
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
    with open(out_class_names_file, 'w') as f:
        f.writelines('\n'.join(class_names))
    print('Saved class_names:', out_class_names_file)

    label_name_to_value = {'_background_': 0, 'bad': 1, 'good': 2}

    colormap = labelme.utils.label_colormap(255)

    for label_file in glob.glob(osp.join(in_dir, '*.json')):
        print('Generating dataset from:', label_file)
        with open(label_file) as f:
            base = osp.splitext(osp.basename(label_file))[0]
            out_img_file = osp.join(
                out_dir, 'JPEGImages', base + '.jpg')
            out_cls_file = osp.join(
                out_dir, 'MITPrincetonGraspingClass', base + '.npy')
            out_clsp_file = osp.join(
                out_dir, 'MITPrincetonGraspingClassPNG', base + '.png')
            out_clsv_file = osp.join(
                out_dir, 'MITPrincetonGraspingClassVisualization', base + '.jpg')

            data = json.load(f)

            img_file = osp.join(osp.dirname(label_file), data['imagePath'])
            img = np.asarray(PIL.Image.open(img_file))
            PIL.Image.fromarray(img).save(out_img_file)

            cls, ins = labelme.utils.shapes_to_label(
                img_shape=img.shape,
                shapes=data['shapes'],
                label_name_to_value=label_name_to_value,
                type='instance',
            )
            ins[cls == -1] = 0  # ignore it.

            label_names  =[None] * (max(label_name_to_value.values()) + 1 )
            for name, value in label_name_to_value.items():
                label_names[value] = name

            # class label
            labelme.utils.lblsave(out_clsp_file, cls)
            np.save(out_cls_file, cls)
            clsv = labelme.utils.draw_label(
                cls, img, label_names, colormap=colormap)
            PIL.Image.fromarray(clsv).save(out_clsv_file)
    print('...... Finish exporting tasks for:', out_dir)

def exportMITP_suction(labels_file, in_dir, out_dir):
    if osp.exists(out_dir):
        print('Output directory already exists:', out_dir)
        return 1
    os.makedirs(out_dir)
    os.makedirs(osp.join(out_dir, 'JPEGImages'))
    os.makedirs(osp.join(out_dir, 'MITPrincetonSuctionClass'))
    os.makedirs(osp.join(out_dir, 'MITPrincetonSuctionClassPNG'))
    os.makedirs(osp.join(out_dir, 'MITPrincetonSuctionClassVisualization'))
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
    with open(out_class_names_file, 'w') as f:
        f.writelines('\n'.join(class_names))
    print('Saved class_names:', out_class_names_file)

    label_name_to_value = {'_background_': 0, 'bad': 1, 'good': 2}

    colormap = np.array([(1,1,1),(0,0,0),(0.50196078,0.50196078,0.50196078)])

    for label_file in glob.glob(osp.join(in_dir, '*.json')):
        print('Generating dataset from:', label_file)
        with open(label_file) as f:
            base = osp.splitext(osp.basename(label_file))[0]
            out_img_file = osp.join(
                out_dir, 'JPEGImages', base + '.jpg')
            out_cls_file = osp.join(
                out_dir, 'MITPrincetonSuctionClass', base + '.npy')
            out_clsp_file = osp.join(
                out_dir, 'MITPrincetonSuctionClassPNG', base + '.png')
            out_clsv_file = osp.join(
                out_dir, 'MITPrincetonSuctionClassVisualization', base + '.jpg')

            data = json.load(f)

            img_file = osp.join(osp.dirname(label_file), data['imagePath'])
            img = np.asarray(PIL.Image.open(img_file))
            PIL.Image.fromarray(img).save(out_img_file)

            cls = labelme.utils.shapes_to_label(
                img_shape=img.shape,
                shapes=data['shapes'],
                label_name_to_value=label_name_to_value,
            )

            label_names  =[None] * (max(label_name_to_value.values()) + 1 )
            for name, value in label_name_to_value.items():
                label_names[value] = name

            # class label
            labelme.utils.lblsave_robotic(out_clsp_file, cls)
            np.save(out_cls_file, cls)
            clsv = labelme.utils.draw_label_robotic(
                cls, img, label_names, colormap=colormap)
            PIL.Image.fromarray(clsv).save(out_clsv_file)
    print('...... Finish exporting tasks for:', out_dir)
