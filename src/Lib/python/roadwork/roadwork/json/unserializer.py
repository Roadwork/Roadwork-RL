import gym.spaces
from gym.spaces import Tuple, Box, Discrete, MultiDiscrete, MultiBinary, Tuple, Dict
from google.protobuf.json_format import MessageToDict, MessageToJson
import numpy as np
import json

# https://github.com/openai/gym/tree/master/gym/spaces
def unserializeMeta(obj):
    if obj['name'] == 'Discrete':
        return unserializeMetaDiscrete(obj)
    elif obj['name'] == 'MultiDiscrete':
        return unserializeMetaMultiDiscrete(obj)
    elif obj['name'] == 'Box':
        return unserializeMetaBox(obj)
    elif obj['name'] == 'Tuple':
        return unserializeMetaTuple(obj)
    else:
        print("Unsupported Space Type:")
        print(obj)

# https://github.com/openai/gym/blob/master/gym/spaces/box.py
def unserializeMetaBox(obj):
    shape = tuple(obj['shape'])

    return Box(
        low=np.reshape(np.array(obj['low']), shape), 
        high=np.reshape(np.array(obj['high']), shape), 
        shape=shape
    )

def unserializeMetaDiscrete(obj):
    return Discrete(obj['n'])

def unserializeMetaMultiDiscrete(obj):
    return MultiDiscrete(obj['nvec'])

# https://github.com/openai/gym/blob/master/gym/spaces/tuple.py
def unserializeMetaTuple(obj):
    res = []

    for t_space in obj['spaces']:
        t_space_unserialized = unserializeMeta(t_space)
        res.append(t_space_unserialized)

    return Tuple(res)