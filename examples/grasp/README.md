# Grasping Labeling Example

## Annotation

```bash
labelme data_annotated --labels labels.txt --nodata
```

![](.readme/annotation.jpg)

## Convert to grasping Dataset

![](.readme/convert.jpg)

```bash
# It generates:
#   - data_annotated_grasp/JPEGImages
#   - data_annotated_grasp/MITPrincetonGraspingClass
#   - data_annotated_grasp/MITPrincetonGraspingClassPNG
#   - data_annotated_grasp/MITPrincetonGraspingClassVisualization
```

<img src="data_dataset_grasp/JPEGImages/2018_000002.jpg" width="33%" /> <img src="data_dataset_grasp/MITPrincetonGraspingClassVisualization/2018_000002.jpg" width="33%" /> <img src="data_dataset_grasp/MITPrincetonGraspingClassPNG/2018_000002.png" width="33%" />  
Fig 1. JPEG image (left), JPEG grasping label visualization (center), PNG grasping label (right)
