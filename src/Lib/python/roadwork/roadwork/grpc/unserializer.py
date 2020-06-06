import gym.spaces
from gym.spaces import Tuple, Box, Discrete, MultiDiscrete, MultiBinary, Tuple, Dict
import numpy as np

def unserialize(obj):
    if obj.HasField('discrete'):
        return obj.discrete
    elif obj.HasField('box'):
        return np.array(obj.box.observation)
    else:
        print("Unsupported Space Type:")
        print(obj)

# https://github.com/openai/gym/tree/master/gym/spaces
def unserializeMeta(obj):
    if obj.HasField('discrete'):
        return unserializeMetaDiscrete(obj.discrete)
    elif obj.HasField('box'):
        return unserializeMetaBox(obj.box)
    elif obj.HasField('tuple'):
        return unserializeMetaTuple(obj.tuple)
    else:
        print("Unsupported Space Type:")
        print(obj)


# https://github.com/openai/gym/blob/master/gym/spaces/box.py
def unserializeMetaBox(b):
    low = []
    high = []
    shape = tuple(b.shape)

    for x in b.dimensions:
        low.append(x.low)
        high.append(x.high)

    return Box(
        low=np.reshape(np.array(low), shape), 
        high=np.reshape(np.array(high), shape), 
        shape=shape
    )

def unserializeMetaDiscrete(d):
    return Discrete(d.n)

# https://github.com/openai/gym/blob/master/gym/spaces/tuple.py
def unserializeMetaTuple(t):
    res = []

    for t_space in t.spaces:
        t_space_unserialized = unserializeMeta(t_space)
        res.append(t_space_unserialized)

    return Tuple(res)