# Bounding Box Detection Example


## Usage

```bash
labelme data_annotated --labels labels.txt --nodata --autosave
```

![](.readme/annotation.png)


## Convert to VOC-like Dataset

```bash
# It generates:
#   - data_annotated_detection/JPEGImages
#   - data_annotated_detection/Annotations
#   - data_annotated_detection/AnnotationsVisualization
Click "export" button to export VOC-like dataset of object detection
```
![](.readme/export_detection_dataset.png)


See below examples:

<img src="data_annotated_detection/JPEGImages/2011_000003.jpg" width="33%" /> <img src="data_annotated_detection/AnnotationsVisualization/2011_000003.png" width="33%" />

<i>Fig1. JPEG image (left), Bounding box annotation visualization (right).</i>
