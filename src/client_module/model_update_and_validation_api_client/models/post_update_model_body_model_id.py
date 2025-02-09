from enum import Enum


class PostUpdateModelBodyModelId(str, Enum):
    CIFAR10 = "cifar10"

    def __str__(self) -> str:
        return str(self.value)
