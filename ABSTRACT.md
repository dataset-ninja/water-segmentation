For this work, authors have thus built a waterrelated image database, which they referred to as the **WaterDataset**. This training dataset contains 2388 water-related images that come with annotations. It also contains 20 manually labeled water videos for testing. Our model and the comparative methods are all trained and evaluated using this dataset.

The training set has 2388 waterrelated still images with annotations; 1888 images are from [ADE20K](https://openaccess.thecvf.com/content_cvpr_2017/html/Zhou_Scene_Parsing_Through_CVPR_2017_paper.html) and 300 images are from [RiverDataset](https://www.researchgate.net/publication/322515648_River_segmentation_for_flood_monitoring). These images contain various types of water, including lakes, canals, rivers, oceans, and floods. The evaluation set contains 20 water related videos:
1. 7 videos recorded on days with heavy rain, when local creeks and ponds were flooded. Frames in these 7 videos were all manually labeled.
2. 10 surveillance videos from [Farson Digital Watercams](https://www.farsondigitalwatercams.com/) that recorded open waters from 8 a.m. to 6 p.m. Frames in these 10 videos were uniformly labeled every 50 frames.
3. 3 surveillance videos taken at the beach that recorded changes in sea waves.

<i>Please Note, that some images contain blanked masks (For example: ADE_train_00002842.png, ADE_train_00003321.png etc. (total 8)</i>
