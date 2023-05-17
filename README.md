# Forest Patches

![Final result](https://github.com/Linzh7/ForestPatches/blob/linzh/assets/GIS-screenshot.png?raw=true)

Welcome to our research project, where we aim to investigate the impact of past forest fragmentation on the evolution of insect population traits. To achieve this, we are exploring ways to digitize, detect, and extract past forest patches from historical aerial photographs. Our primary objective is to develop a tool that can accurately classify forest and non-forest areas with a specific threshold based on ground truth data. The tool will help us detect past forest patches, starting from present aerial images and going back to older images. Students working on this project will supervise open access aerial images with two possible ground truth datasets: biomass and canopy cover raster GIS data sets provided by the Natural Resources Institute Finland, and the Corine Land Cover (CLC) GIS data set about land use types provided by the Finnish Environmental Institute. As we move towards older aerial images, ground truth data become scarce or non-existent, and we will rely on the tool's training on newer or present data to recognize forest patches. Key elements for image recognition and classification are image texture and relative differences in color attributes. Aerial photographs are from different phenological stages and light conditions. Newer images are colored, whereas older ones are grayscale. Open access aerial images are available through the WMS interface provided by the HRI (Helsinki Region Infoshare) from 1932 to 2021.


## Stucture of project

This project is organized into several directories each serving a specific purpose:

- GAN: Contains the source code for the Generative Adversarial Network used for image colorization. This includes the colorize.py script which is used to colorize grayscale images, as well as a modified version of the fastai library and the deoldify library which provides models and utilities for training and running the GAN.
- model_zoo: Contains fine-tuned semantic segmentation models and training scripts.
- preprocess: Contains utilities for downloading and preprocessing data used in training our model.
- UNet: Contains the source code for the semantic segmentation neural network used for image segmentation. This includes the train.py and predict.py scripts for training and testing the model, as well as various utility functions for data loading and processing.
```
.
├── GAN
│   ├── colorize.py
│   ├── deoldify
│   │   ├── ...
│   ├── environment.yml
│   ├── fastai
│   │   ├── ...
│   ├── fid
│   │   ├── ...
│   ├── ImageColorizerArtistic.ipynb
│   ├── ImageColorizerStable.ipynb
│   ├── linzhutils.py
│   ├── models
│   │   ├── ...
│   ├── requirements.txt
│   └── setup.py
├── model_zoo
│   ├── linzhutils.py
│   ├── models
│   │   ├── ...
│   └── train.ipynb
├── preprocess
│   ├── color_picker.py
│   ├── data_downloader_parallel.py
│   ├── data_downloader.py
│   ├── data_downloader.py.bak
│   ├── linzhutils.py
│   ├── mask_process_kuusi.py
│   ├── mask_process.py
├── README.md
└── UNet
    ├── checkpoints
    │   ├── ...
    ├── data
    │   └── ...
    ├── Dockerfile
    ├── evaluate.py
    ├── hubconf.py
    ├── LICENSE
    ├── linzhutils.py
    ├── predict.py
    ├── README.md
    ├── requirements.txt
    ├── scripts
    │   └── download_data.sh
    ├── test.py
    ├── train.py
    ├── unet
    │   ├── __init__.py
    │   ├── unet_model.py
    │   └── unet_parts.py
    └── utils
        ├── data_loading.py
        ├── dice_score.py
        ├── __init__.py
        └── utils.py
```

## How to get started

Please read the following instructions carefully before you start.

### Install requirements

Make sure that you installed all libraries, or you could use the modules on [Puhti](https://www.puhti.csc.fi/).

To use the Puhti modules, you need to load the modules first.

1. For downloading the data, you need to load the `geoconda` module. You can use `module load geoconda` to load this module. If you prefer the Puhti JupyterLab, you can select the `geoconda` module in the `Settings/Python` tab on dashboard.
2. For training the model or using the model to predict, you need to load the `pytorch` module.

### Download dataset
- In our project, there are two versions of the downloader script available to download data: `data_downloader.py` and `data_downloader_parallel.py`. The former is a single-thread downloader, while the latter is a multi-thread downloader that offers faster downloading speeds. However, the multi-thread downloader may cause issues such as `ConnectionResetError` due to server limitations, so it's essential to ensure a stable network connection when using it and do not start too many threads at same time. For simplicity, we will be using the single-thread downloader in the following instructions.
- To download the data, navigate to the root folder of the project and run `preprocess/data_downloader.py`, for example, `python preprocess/data_downloader.py`. There are various arguments you can use with this script; for more information, run python `preprocess/data_downloader.py --help`.
- When using the `data_downloader.py` script, each tile downloaded will have a default configuration of 5120x5120 pixels, covering an area of 1km x 1km for reducing the . you can further split these tiles to suit your needs. To do this, you can use any image processing library or tool of your choice.

### Process the masks and images

- There are two version of processer, `mask_process_kuusi.py` is for kuusi dataset, which means you only want to detect the existence of kuusi. `mask_process.py` is for the whole dataset, which means you want to detect the forest dominated by kuusi.

`mask_process_kuusi.py` is a script that converts color masks to binary masks. The script takes as input a set of color masks in the form of .jpg, .png or .jpeg files located in a folder called "color_masks", specified by the variable INPUT_PATH. It then processes each mask to create a binary mask and saves it to a folder called "bin_masks", specified by the variable OUTPUT_PATH. The binary mask is created by setting all pixels in the color mask that match any of the colors in COLOR_LIST to 1 and all other pixels to 0. The purpose of this script is to prepare data for further processing in the research project, specifically to simplify the forest/non-forest classification task by converting color-coded labels into binary labels.


### Train your model

- There are two ways to train the model. The U-Net model is in `UNet` folder, you can run `train.py` to train the model.

- The other way is to much flexible in `model_zoo` folder. You could know more of methods and backbones in [here](https://github.com/qubvel/segmentation_models.pytorch). You could follow the instructions in `model_zoo/train.ipynb` to train your model.
- You can also use `model_zoo/explore.ipynb` to visualize the dataset and some samples.

### Use model to predict

#### UNet
- run `UNet/test_single.py` to predict a single image or few images as a list.
- run `UNet/test.py` to predict a whole folder.

#### Model Zoo
- run `model_zoo/run_prediction.ipynb` to run inference on a dataset.


## Credits

In this project, the following repositories are used:

- [UNet](https://github.com/milesial/Pytorch-UNet)
- [Seamentation Models](https://github.com/qubvel/segmentation_models.pytorch)
- [DeOldify](https://github.com/jantic/DeOldify)