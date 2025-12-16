import torch
import torch.nn as nn
import torch.nn.functional as F

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        return F.relu(x + residual)

class PolicyValueNet(nn.Module):
    def __init__(self):
        super().__init__()
        # Input: 12 channels (6 piece types × 2 colors)
        self.input_conv = nn.Conv2d(12, 64, 3, padding=1)
        self.res_blocks = nn.Sequential(
            *[ResidualBlock(64) for _ in range(3)]
        )

        # Policy head - outputs move probabilities for each square
        # For simplicity, we output a value per square (64 values)
        self.policy_head = nn.Sequential(
            nn.Conv2d(64, 2, 1),
            nn.BatchNorm2d(2),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(2 * 8 * 8, 128),
            nn.ReLU(),
            nn.Linear(128, 64),  # 64 squares
            nn.Softmax(dim=1)
        )

        # Value head - outputs position evaluation
        self.value_head = nn.Sequential(
            nn.Conv2d(64, 1, 1),
            nn.BatchNorm2d(1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(8 * 8, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1),
            nn.Tanh()  # Output between -1 and 1
        )

    def forward(self, x):
        """
        Forward pass
        Args:
            x: Input tensor of shape (batch, 12, 8, 8)
        Returns:
            policy: Policy distribution over moves (batch, 64)
            value: Position evaluation (batch, 1)
        """
        x = F.relu(self.input_conv(x))
        x = self.res_blocks(x)
        
        policy = self.policy_head(x)
        value = self.value_head(x)
        
        return policy, value