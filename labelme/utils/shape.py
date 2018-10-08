import numpy as np
import PIL.Image
import PIL.ImageDraw

from labelme import logger


def polygons_to_mask(img_shape, polygons):
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    xy = list(map(tuple, polygons))
    PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


def mask_to_bbox(mask):
    where = np.argwhere(mask)
    (y1, x1), (y2, x2) = where.min(0), where.max(0) + 1
    return x1, y1, x2, y2


def shapes_to_label(img_shape, shapes, label_name_to_value, type='class', saveGrasplbl2txt=False, saveDetectlbl2csv=True):
    assert type in ['class', 'instance', 'grasping']

    cls = np.zeros(img_shape[:2], dtype=np.int32)
    if type == 'instance':
        ins = np.zeros(img_shape[:2], dtype=np.int32)
        instance_names = ['_background_']
    out_points_good = []
    out_points_bad = []
    out_bbox_points = []
    for shape in shapes:
        polygons = shape['points']
        bbox_class_point=[]
        a_min=np.min(polygons, axis=0)
        a_max=np.max(polygons, axis=0)
        label = shape['label']
        if type == 'class' or type == 'grasping':
            cls_name = label
        elif type == 'instance':
            cls_name = label.split('-')[0]
            if label not in instance_names:
                instance_names.append(label)
            ins_id = len(instance_names) - 1
        
        for points in polygons:
            if str(cls_name) == 'good':
                out_points_good.append(points)
            elif str(cls_name) == 'bad':
                out_points_bad.append(points)
        
        if saveDetectlbl2csv:
            #print("x(min),y(min),x(max),y(max) ",a_min[0],a_min[1],a_max[0],a_max[1])
            # method2: get x1,y1,x2,y2 via mask_to_bbox function (mzhu)
            bbox_class_point.append(cls_name)
            bbox_class_point.append(a_min[0])
            bbox_class_point.append(a_min[1])
            bbox_class_point.append(a_max[0]+1)
            bbox_class_point.append(a_max[1]+1)
            out_bbox_points.append(bbox_class_point)

        cls_id = label_name_to_value[cls_name]
        mask = polygons_to_mask(img_shape[:2], polygons)
        cls[mask] = cls_id
        if type == 'instance':
            ins[mask] = ins_id

    if saveGrasplbl2txt:
        return cls, out_points_good, out_points_bad
    if type == 'instance':
        if saveDetectlbl2csv:
            return cls, ins, out_bbox_points
        else:
            return cls, ins
    if saveDetectlbl2csv:
        return cls, out_bbox_points
    return cls


def labelme_shapes_to_label(img_shape, shapes):
    logger.warn('labelme_shapes_to_label is deprecated, so please use '
                'shapes_to_label.')

    label_name_to_value = {'_background_': 0}
    for shape in shapes:
        label_name = shape['label']
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value

    lbl = shapes_to_label(img_shape, shapes, label_name_to_value)
    return lbl, label_name_to_value
