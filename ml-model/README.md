# Running Conda Environment to Access Camera

1. Install conda on your local machine
2. Create your conda environment to run ultralytics and OpenCV using `CONDA_SUBDIR=osx-arm64 conda create -n ultralytics-env python=3.12 -y`
    - For Windows you can ignore the CONDA_SUBDIR=osx-arm64 environment variable
3. Enter the conda environment by entering `conda activate ultralytics-env`
4. Install ultralytics on the conda environment using `pip install ultralytics`
5. Run yoloV11.py script using `python3 yoloV11.py` or yolo11nLabelKeypoints.py using `python3 yolo11nLabelKeypoints.py`

## Resources

-   ![Ultralytics Coco Pose Estimation](https://docs.ultralytics.com/datasets/pose/coco/)
-   ![Ultralytics Pose Estimation Tasks](https://docs.ultralytics.com/tasks/pose/)
