import torch
import torch.nn.functional as F

y = torch.randn(5, 3)
y = F.softmax(y, 1)
print(y)