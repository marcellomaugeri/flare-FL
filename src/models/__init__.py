from .cifar10 import get_model as get_cifar10_model

def get_model(model_name):
    model_mapping = {
        "cifar10": get_cifar10_model,
    }
    
    if model_name in model_mapping:
        return model_mapping[model_name]()
    else:
        raise ValueError(f"Model '{model_name}' is not recognized. Available models: {list(model_mapping.keys())}")