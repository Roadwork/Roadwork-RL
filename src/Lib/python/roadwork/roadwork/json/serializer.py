import gym.spaces
import roadwork.proto.roadwork_pb2 as api_v1
import numpy as np

import gym.spaces
import roadwork.proto.roadwork_pb2 as api_v1
import numpy as np

def serializeMeta(space):
    res = {}
    res['name'] = space.__class__.__name__

    if res['name'] == 'Box':
        res = serializeMetaBox(res, space)
    elif res['name'] == 'Discrete':
        res = serializeMetaDiscrete(res, space)
    elif res['name'] == 'MultiDiscrete':
        res = serializeMetaMultiDiscrete(res, space)
    elif res['name'] == 'Tuple':
        res = serializeMetaTuple(res, space)
    else:
        print("Unsupported Space Type")
        print(space)

    return res

# https://github.com/openai/gym/blob/master/gym/spaces/box.py
# Serialize shape to array
# Serialize Low and High to respective object with low and high
def serializeMetaBox(res, space):
    res['shape'] = np.asarray(space.shape).tolist()

    # It's not JSON compliant to have Infinity, -Infinity, NaN.
    # Many newer JSON parsers allow it, but many don't. Notably python json
    # module can read and write such floats. So we only here fix "export version",
    # also make it flat.
    res['low']  = [float(x if x != -np.inf else -1e100) for x in np.array(space.low ).flatten()]
    res['high'] = [float(x if x != +np.inf else +1e100) for x in np.array(space.high).flatten()]

    return res

def serializeMetaDiscrete(res, space):
    res['n'] = space.n
    return res

def serializeMetaMultiDiscrete(res, space):
    res['nvec'] = space.nvec.tolist()
    return res

# https://github.com/openai/gym/blob/master/gym/spaces/tuple.py
def serializeMetaTuple(res, space):
    res['spaces'] = []

    for spaceTuple in space.spaces:
        res['spaces'].append(serializeMeta(spaceTuple))

    return res