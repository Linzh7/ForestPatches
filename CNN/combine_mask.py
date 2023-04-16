#this code is a helper function that combines the mask pieces to one file so that inspecting quality is easier
from PIL import Image
import torchvision.transforms as transforms
import os
import torch
from torch import nn
from torchvision.models.segmentation import deeplabv3_resnet50

X_DIM = 5
Y_DIM = 5
IMAGE_SIZE = 1024 #assuming we have square images
Y_ZERO_BOTTOM = False #turn this true if the image with y_index 0 is on the bottom

#transform image to tensor
transform = transforms.Compose([
    transforms.PILToTensor()
])

files = os.listdir()
file_iterator = iter(files)
img_stack = torch.empty((X_DIM, Y_DIM, 1, IMAGE_SIZE, IMAGE_SIZE))
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

mask_stack = img_stack[0,:,0,:,:]
mask_stack = torch.flatten(mask_stack, start_dim=0, end_dim=1)

for i in range(1, X_DIM):
    new_stack = img_stack[i,:,0,:,:]
    new_stack = torch.flatten(new_stack, start_dim=0, end_dim=1)
    mask_stack = torch.cat((mask_stack, new_stack), dim=1)

img = Image.fromarray(mask_stack.mul(255).byte().cpu().numpy())
img.save('combined_mask2011.tif')