# Suction Labeling Example

## Annotation

```bash
labelme data_annotated --labels labels.txt --nodata
```

![](.readme/annotation.png)

## Convert to suction Dataset

![](.readme/convert.png)

```bash
# It generates:
#   - data_annotated_suction/JPEGImages
#   - data_annotated_suction/SuctionClass
#   - data_annotated_suction/SuctionClassPNG
#   - data_annotated_suction/SuctionClassVisualization
```

<img src="data_annotated_suction/JPEGImages/2018_000002.jpg" width="33%" /> <img src="data_annotated_suction/SuctionClassVisualization/2018_000002.jpg" width="33%" /> <img src="data_annotated_suction/SuctionClassPNG/2018_000002.png" width="33%" />  
Fig 1. JPEG image (left), JPEG suction label visualization (center), PNG suction label (right)
