# Instance Segmentation Example

## Annotation

```bash
labelme data_annotated --labels labels.txt --nodata
```

![](.readme/annotation.jpg)

## Convert to VOC-like Dataset

![](.readme/convert.jpg)

```bash
# It generates:
#   - data_annotated_voc_instance/JPEGImages
#   - data_annotated_voc_instance/SegmentationClass
#   - data_annotated_voc_instance/SegmentationClassVisualization
#   - data_annotated_voc_instance/SegmentationObject
#   - data_annotated_voc_instance/SegmentationObjectVisualization
```

<img src="data_annotated_voc_instance/JPEGImages/2011_000003.jpg" width="33%" /> <img src="data_annotated_voc_instance/SegmentationClassVisualization/2011_000003.jpg" width="33%" /> <img src="data_annotated_voc_instance/SegmentationObjectVisualization/2011_000003.jpg" width="33%" />  
Fig 1. JPEG image (left), JPEG class label visualization (center), JPEG instance label visualization (right)


Note that the label file contains only very low label values (ex. `0, 4, 14`), and
`255` indicates the `__ignore__` label value (`-1` in the npy file).  
You can see the label PNG file by following.

```bash
labelme_draw_label_png data_annotated_voc_instance/SegmentationClassPNG/2011_000003.png   # left
labelme_draw_label_png data_annotated_voc_instance/SegmentationObjectPNG/2011_000003.png  # right
```

<img src=".readme/draw_label_png_class.jpg" width="33%" /> <img src=".readme/draw_label_png_object.jpg" width="33%" />
