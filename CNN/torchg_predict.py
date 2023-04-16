from PIL import Image
import torchvision.transforms as transforms
import os
import torch
from torch import nn
from torchvision.models.segmentation import deeplabv3_resnet50

X_DIM = 5 #the number of images in x dimension, too many images may cause memory insufficiency errors
Y_DIM = 5
IMAGE_SIZE = 1024 #assuming we have square images
Y_ZERO_BOTTOM = False #turn this true if the image with y_index 0 is on the bottom

model = deeplabv3_resnet50(weights=None, num_classes=2)

backbone = model.get_submodule('backbone')

conv = nn.modules.conv.Conv2d(
    in_channels=3, 
    out_channels=64, 
    kernel_size=(7, 7),
    stride=(2, 2),
    padding=(3, 3),
    bias=False
)
backbone.register_module('conv1', conv)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

os.chdir('') #the path to the folder containing images to classify

#transform image to tensor
transform = transforms.Compose([
    transforms.PILToTensor()
])

files = os.listdir()
file_iterator = iter(files)
img_stack = torch.empty((X_DIM, Y_DIM, 3, IMAGE_SIZE, IMAGE_SIZE))
for i in range(len(files)):
    image = Image.open(next(file_iterator))
    x_index = int(image.filename.split('_')[-2]) #the indexing of the file is assumed to be 'imagesetname_xindex_yindex.tif'
    y_index = int(image.filename.split('_')[-1].split('.')[0])
    if Y_ZERO_BOTTOM:
        y_index = abs(y_index - (Y_DIM - 1))
    if x_index >= X_DIM or y_index >= Y_DIM:
        continue
    img_tensor = transform(image)
    img_stack[x_index, y_index] = img_tensor

os.chdir('') #the path to the model
model.load_state_dict(torch.load('geo_model', map_location=torch.device(device))) #change the name of the saved model if necessary
model.eval()

pred = model(img_stack[0,:,:,:,:]) # the first 'column of masks'
pred = torch.argmax(pred['out'], dim=1)
image = torch.flatten(pred, start_dim=0, end_dim=1)
for i in range(1, X_DIM):
    pred = model(img_stack[i,:,:,:,:])
    pred = torch.argmax(pred['out'], dim=1)
    new_image_column = torch.flatten(pred, start_dim=0, end_dim=1)
    image = torch.cat((image, new_image_column), dim=1)


img = Image.fromarray(image.mul(255).byte().cpu().numpy())
img.save('classified.tif')



