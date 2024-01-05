import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(2, 0.5)
])


train = datasets.MNIST('dataset/', train=True, download=True, transform=preprocess)
test = datasets.MNIST('dataset/', train=False, download=True, transform=preprocess)

trainloader = torch.utils.data.Dataloader(train, batch_size=32, shuffle=True)
testloader = torch.utils.data.Dataloader(test, batch_size=32, shuffle=True)


# good batch sized models are:
# * batch_size = dataset.size
# * batch_size < dataset.size: batch_size = 2^x (32 is a good starting place)
# * batch_size = 1

nf = 32  # number of neurons
lr = 0.0001
beta1 = 0.5
beta2 = 0.999
device = "cpu"


# a NN is defined as a subclass of torch.nn.Module (super/base class)
class Net(nn.Module):
    # iniatilize layers in __init__ function
    def __init__(self):
        super(Net, self).__init__()

        self.convs = nn.Sequential(
            nn.Conv2d(1, nf, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),

            nn.Conv2d(nf, nf, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(nf, nf, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
            )

        self.linears = nn.Sequential(
                nn.Linear(1568, 100), # width=7, height=7, filters=32; linear layer input = 7*7*32 = 1568
                nn.ReLU(),

                nn.Linear(100, 50),
                nn.ReLU(),

                nn.Linear(50, 10),
                )

        # train/connect them in forward function
    def forward(self, x):
        x = self.convs(x)
        x = x.view(x.size(0), -1) # flattening, result will be (64, 1568)
        x = self.linears(x)
        return x


# activation functions like ReLU where { x > 0, f(x) = x, else f(x) = 0}
# other activation functions exist as well

# each nn produces an output which is then calculated by loss function based off of how far the answer is from the right one
# the output is determined by the inputs being passed around through the activated nodes which use the activation function
# the optiimzer function is supposed to fix some of these issues such as

# gradient - a vector in that directs towards the direction of the greatest change
# exploding gradient is a situation where ReLU is not the best, and maybe leaky ReLU is better
# epxloding gradient: the derrivative of the slope at each layer convering into an infintely small number
# they depend on backpropogation which is a gradient descent based optimizer meaning it is exposed to problems exploding/vanishing gradient
# when exploding gradient, is when the cost function is changing so rapidly meaning that it
# is too volatile the model at the end of the training cycle
# meaning that you should increase batch size
