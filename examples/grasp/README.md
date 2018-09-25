# Grasping Labeling Example

## Annotation

```bash
labelme data_annotated --labels labels.txt --nodata
```

![](.readme/annotation.png)

## Convert to grasping Dataset

![](.readme/convert.png)

```bash
# It generates:
#   - data_annotated_grasp/JPEGImages
#   - data_annotated_grasp/GraspingClass
#   - data_annotated_grasp/GraspingClassPNG
#   - data_annotated_grasp/GraspingClassCoordinate
#   - data_annotated_grasp/GraspingClassVisualization
```

<img src="data_annotated_grasp/JPEGImages/2018_000002.jpg" width="33%" /> <img src="data_annotated_grasp/GraspingClassVisualization/2018_000002.jpg" width="33%" /> <img src="data_annotated_grasp/GraspingClassPNG/2018_000002.png" width="33%" />  
Fig 1. JPEG image (left), JPEG grasping label visualization (center), PNG grasping label (right)
