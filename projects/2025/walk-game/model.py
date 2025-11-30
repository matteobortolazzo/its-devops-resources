import torch.nn as nn

class PolicyNet(nn.Module):
    def __init__(self, input_dim=6, hidden=32, n_actions=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, n_actions),
        )

    def forward(self, x):
        return self.net(x)

class BigPolicyNet(nn.Module):
    def __init__(self, input_dim=6, hidden=64, n_actions=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),  # Additional hidden layer
            nn.ReLU(),
            nn.Linear(hidden, n_actions),
        )

    def forward(self, x):
        return self.net(x)