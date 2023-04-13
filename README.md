# Forest Patches

This project is aimed to ...


## Stucture of project

```
.
├── README.md
├── UNet
├── data
└── preprocess
    ├── archived  # archived files
    ├── color_picker.py  # Utils for pick the color in a image
    ├── data_downloader.py  # download dataset from WMS
    ├── linzhutils.py  # my tools collection
    └── mask_process.py  # process masks to a binary mask
```

## How to get started

Please read the following instructions carefully before you start.

### Install requirements

Make sure that u install all libraries.

TODO:
- [ ] add requirements.txt

<!-- 
We also provide a `requirements.txt` for pip. Use the following command to install.

``pip install -r requirements.txt``

NB: If you are using Macbook with Apple silicon, you can install `mediapipe-silicon` instead of `mediapipe`, but they said that mediapipe will support Apple silicon soon. And use `requirements_maxOS.txt` instead of `requirements.txt`. -->

### Download dataset
<<<<<<< HEAD

TODO: 
- [x] add argument parser
1. run `preprocess/data_downloader.py`, such as `python preprocess/data_downloader.py`.
=======
- There are two version of downloader, one is `data_downloader.py`, the other is `data_downloader_parallel.py`. The first one is a single thread downloader, the second one is a multi-thread downloader. The second one is faster, but it may cause some problems, such as `ConnectionResetError` beucase the server might limit our requests. If you want to use the second one, please make sure that you have a stable network. However, to simplify our statement, we will use the first one in the following instructions.
- Run `preprocess/data_downloader.py` at **root** folder, such as `python preprocess/data_downloader.py`.
- There are some arguments you can use, type `python preprocess/data_downloader.py --help` or to see more.
- The size of each tile is 5120x5120, which shows the 1km*1km area. You could split them later.
>>>>>>> 06ce86bf243d6246e80521bd53770ec57ca8597a

### Process the masks and images

TODO:
- [ ] add argument parser
- [ ] add split function


- There are two version of processer, `mask_process_kuusi.py` is for kuusi dataset, which means you only want to detect the existence of kuusi. `mask_process.py` is for the whole dataset, which means you want to detect the forest dominated by kuusi. However, to simplify our statement, we will use the first one in the following instructions.
- run `preprocess/mask_process.py`.

### Train your model

TODO:
- [ ] find a best model
- [ ] add argument parser
- [ ] make the train and test more flexible

- There are two ways to train the model. The U-Net model is in `UNet` folder, you can run `train.py` to train the model.

- The other way is to much flexible in `model_zoo` folder. You could know more of methods and backbones in [here](https://github.com/qubvel/segmentation_models.pytorch). You could follow the instructions in `model_zoo/train.ipynb` to train your model.
- You can also use `model_zoo/explore.ipynb` to visualize the dataset and some samples.

### Use model to predict

#### UNet
- run `UNet/test_single.py` to predict a single image or few images as a list.
- run `UNet/test.py` to predict a whole folder.

#### Model Zoo
- run `model_zoo/predict.ipynb` to predict a single image or few images as a list.
- run `model_zoo/test.ipynb` to test the model on some dataset.


<!-- 1. run `main.py`
1. act some sign to the camera
2. after the program comfirm your sign, it will play the corresponding English word
3. enjoy

*If you do not like the Preview window, you can set`SHOW = False`* -->
