from .shuffle_vertex import ShuffleVertex
from .mnetv2cls import SimpleMNetV2Cls
from .resnet_vertex import ResNetVertex
import torch.nn as nn

__all__ = ['build_model']

_models_list_ = dict(ShuffleVertex=ShuffleVertex, MobileVertex=SimpleMNetV2Cls, ResNetVertex=ResNetVertex)


def build_model(name: str, **option) -> nn.Module:
    assert name in _models_list_.keys()
    return _models_list_[name](**option)


