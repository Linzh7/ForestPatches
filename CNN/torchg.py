#this code is based on this blog series: https://towardsdatascience.com/artificial-intelligence-for-geospatial-analysis-with-pytorchs-torchgeo-part-1-52d17e409f09
from pathlib import Path
from typing import List, Callable, Optional

from torchgeo.datasets import RasterDataset, unbind_samples, stack_samples
from torchgeo.samplers import RandomGeoSampler, Units
from torch.utils.data import DataLoader
from torch import nn
import torch
from torchvision.models.segmentation import deeplabv3_resnet50
from sklearn.metrics import jaccard_score

root = Path('') #the path where both aerial images and masks are in their own folders
assert root.exists()

train_imgs = RasterDataset(root=(root/'helsinki2015').as_posix()) #the image folder
train_msks = RasterDataset(root=(root/'mask2015').as_posix()) #the mask folder

valid_imgs = RasterDataset(root=(root/'helsinki2015/val').as_posix()) #the validation data is placed in a subfolder
valid_msks = RasterDataset(root=(root/'mask2015/val').as_posix())

# IMPORTANT
train_msks.is_image = False
valid_msks.is_image = False

train_dset = train_imgs & train_msks
valid_dset = valid_imgs & valid_msks

train_sampler = RandomGeoSampler(train_imgs, size=512, length=50, units=Units.PIXELS)
valid_sampler = RandomGeoSampler(valid_imgs, size=512, length=10, units=Units.PIXELS)

train_dataloader = DataLoader(train_dset, sampler=train_sampler, batch_size=5, collate_fn=stack_samples)
valid_dataloader = DataLoader(valid_dset, sampler=valid_sampler, batch_size=5, collate_fn=stack_samples)

train_batch = next(iter(train_dataloader))
valid_batch = next(iter(valid_dataloader))

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

def train_loop(
    epochs: int, 
    train_dl: DataLoader, 
    val_dl: Optional[DataLoader], 
    model: nn.Module, 
    loss_fn: Callable, 
    optimizer: torch.optim.Optimizer, 
    acc_fns: Optional[List]=None, 
    batch_tfms: Optional[Callable]=None
):
    used_model = model.to(device)

    for epoch in range(epochs):
        accum_loss = 0
        for i, batch in enumerate(train_dl):
            if batch_tfms is not None:
                batch = batch_tfms(batch)

            X = batch['image'].to(device)
            y = batch['mask'].type(torch.long).to(device)
            pred = used_model(X)['out']
            loss = loss_fn(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            accum_loss += float(loss) / len(train_dl)

        # Testing against the validation dataset
        if acc_fns is not None and val_dl is not None:
            # reset the accuracies metrics
            acc = [0.] * len(acc_fns)

            with torch.no_grad():
                for batch in val_dl:

                    if batch_tfms is not None:
                        batch = batch_tfms(batch)                    

                    X = batch['image'].type(torch.float32).to(device)
                    y = batch['mask'].type(torch.long).to(device)

                    pred = used_model(X)['out']

                    for i, acc_fn in enumerate(acc_fns):
                        acc[i] = float(acc[i] + acc_fn(pred, y)/len(val_dl))

            # at the end of the epoch, print the errors, etc.
            print(f'Epoch {epoch}: Train Loss={accum_loss:.5f} - Accs={[round(a, 3) for a in acc]}')
        else:

            print(f'Epoch {epoch}: Train Loss={accum_loss:.5f}')

#overall accuracy
def oa(pred, y):
    flat_y = y.squeeze()
    flat_pred = pred.argmax(dim=1)
    acc = torch.count_nonzero(flat_y == flat_pred) / torch.numel(flat_y)
    return acc

#intersection over union
def iou(pred, y):
    flat_y = y.cpu().numpy().squeeze()
    flat_pred = pred.argmax(dim=1).detach().cpu().numpy()
    return jaccard_score(flat_y.reshape(-1), flat_pred.reshape(-1), zero_division=1.)

def loss(p, t):    
    return torch.nn.functional.cross_entropy(p, t.squeeze())

optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
train_loop(10, train_dataloader, valid_dataloader, model, loss, optimizer, acc_fns=[oa, iou])

#save the model for using the pretrained model for prediction
torch.save(model.state_dict(), 'geo_model')