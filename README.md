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

## How to get start

### Requirements

Make sure that u install all libraries.

TODO:
- [ ] add requirements.txt

<!-- 
We also provide a `requirements.txt` for pip. Use the following command to install.

``pip install -r requirements.txt``

NB: If you are using Macbook with Apple silicon, you can install `mediapipe-silicon` instead of `mediapipe`, but they said that mediapipe will support Apple silicon soon. And use `requirements_maxOS.txt` instead of `requirements.txt`. -->

### Download dataset

TODO: 
- [x] add argument parser
1. run `preprocess/data_downloader.py`, such as `python preprocess/data_downloader.py`.

### Process the masks and images

TODO:
- [ ] add argument parser
1. run `preprocess/mask_process.py`.
2. wait, until it exit.

### Train your model

TODO:
- [ ] find a best model
- [ ] create a `train.py` to train the model
- [ ] add argument parser
<!-- 1. run `train.py`.
2. wait, until it exit. -->

### Use model to predict

- [ ] create a `predict.py` to use the model to predict some images.
- [ ] add argument parser

<!-- 1. run `main.py`
2. act some sign to the camera
3. after the program comfirm your sign, it will play the corresponding English word
4. enjoy

*If you do not like the Preview window, you can set`SHOW = False`* -->
