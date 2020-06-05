import gym.spaces
import proto_compiled.roadwork_pb2 as roadwork_messages
import numpy as np

def serialize(obj):
    className = obj.__class__.__name__

    res = roadwork_messages.MetaSpaceWrapper()

    if className == 'Box':
        res.box.CopyFrom(serializeBox(obj))
    elif className == 'Discrete':
        res.discrete.CopyFrom(serializeDiscrete(obj))
    elif className == 'Tuple':
        res.tuple.CopyFrom(serializeTuple(obj))

    return res

# https://github.com/openai/gym/blob/master/gym/spaces/box.py
# Serialize shape to array
# Serialize Low and High to respective object with low and high
def serializeBox(b):
    result = roadwork_messages.MetaSpaceBox()

    # Set shape array
    result.shape.extend(np.asarray(b.shape)) 

    # Add dimensions
    for x in range(len(np.array(b.low).flatten())):
        result.dimensions.extend([roadwork_messages.MetaSpaceBoxDimension(
            low=(np.array(b.low).flatten()[x] if np.array(b.low).flatten()[x] != -np.inf else -1e100), 
            high=(np.array(b.high).flatten()[x] if np.array(b.high).flatten()[x] != +np.inf else +1e100)
        )])
    
    return result

def serializeDiscrete(d):
    result = roadwork_messages.MetaSpaceDiscrete()
    result.n = d.n

    return result

# https://github.com/openai/gym/blob/master/gym/spaces/tuple.py
def serializeTuple(t):
    result = roadwork_messages.MetaSpaceTuple()

    for t in t.spaces:
        tCN = t.__class__.__name__
        serializedTupleValue = serialize(t)
        result.spaces.extend([ serializedTupleValue ])

    return result