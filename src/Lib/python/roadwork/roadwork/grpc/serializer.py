import gym.spaces
import roadwork.proto.roadwork_pb2 as api_v1
import numpy as np

def serialize(observation_space_info, observation):
    space_wrapper = api_v1.SpaceWrapper()

    if observation_space_info.HasField('discrete'):
        space_discrete = api_v1.SpaceDiscrete()
        space_discrete.observation = observation
        space_wrapper.discrete.CopyFrom(space_discrete)
    elif observation_space_info.HasField('box'):
        space_box = api_v1.SpaceBox()
        space_box.observation.extend(observation)
        space_wrapper.box.CopyFrom(space_box)
    else:
        print("Unsupported Space Type")
        print(observation_space_info)

    return space_wrapper

def serializeMeta(obj):
    className = obj.__class__.__name__

    res = api_v1.MetaSpaceWrapper()

    if className == 'Box':
        res.box.CopyFrom(serializeMetaBox(obj))
    elif className == 'Discrete':
        res.discrete.CopyFrom(serializeMetaDiscrete(obj))
    elif className == 'Tuple':
        res.tuple.CopyFrom(serializeMetaTuple(obj))
    else:
        print("Unsupported Space Type")
        print(obj)

    return res

# https://github.com/openai/gym/blob/master/gym/spaces/box.py
# Serialize shape to array
# Serialize Low and High to respective object with low and high
def serializeMetaBox(b):
    result = api_v1.MetaSpaceBox()

    # Set shape array
    result.shape.extend(np.asarray(b.shape)) 

    # Add dimensions
    for x in range(len(np.array(b.low).flatten())):
        result.dimensions.extend([api_v1.MetaSpaceBoxDimension(
            low=(np.array(b.low).flatten()[x] if np.array(b.low).flatten()[x] != -np.inf else -1e100), 
            high=(np.array(b.high).flatten()[x] if np.array(b.high).flatten()[x] != +np.inf else +1e100)
        )])
    
    return result

def serializeMetaDiscrete(d):
    result = api_v1.MetaSpaceDiscrete()
    result.n = d.n

    return result

# https://github.com/openai/gym/blob/master/gym/spaces/tuple.py
def serializeMetaTuple(t):
    result = api_v1.MetaSpaceTuple()

    for t in t.spaces:
        tCN = t.__class__.__name__
        serializedTupleValue = serializeMeta(t)
        result.spaces.extend([ serializedTupleValue ])

    return result