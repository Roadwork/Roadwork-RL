import pytest
import numpy as np

from gym.spaces import Tuple, Box, Discrete, MultiDiscrete, MultiBinary, Tuple, Dict
import proto_compiled.roadwork_pb2 as rw # Contains Message Classes

# Run with pytest -s --disable-pytest-warnings
import Serializer
import Unserializer

@pytest.mark.parametrize("tests", [
    # Test simple discrete space
    (Discrete(3), rw.MetaSpaceWrapper(discrete=rw.MetaSpaceDiscrete(n=3))),

    # Test box containing 1 rgb values
    (Box(low=0, high=255, shape=(3, )), rw.MetaSpaceWrapper(box=rw.MetaSpaceBox(shape=[3], dimensions=[
        rw.MetaSpaceBoxDimension(low=0, high=255),
        rw.MetaSpaceBoxDimension(low=0, high=255),
        rw.MetaSpaceBoxDimension(low=0, high=255),
    ]))),

    # Test box containing 2 rgb values
    (Box(low=0, high=255, shape=(3, 2)), rw.MetaSpaceWrapper(box=rw.MetaSpaceBox(shape=[3, 2], dimensions=[
        rw.MetaSpaceBoxDimension(low=0, high=255),
        rw.MetaSpaceBoxDimension(low=0, high=255),
        rw.MetaSpaceBoxDimension(low=0, high=255),
        rw.MetaSpaceBoxDimension(low=0, high=255),
        rw.MetaSpaceBoxDimension(low=0, high=255),
        rw.MetaSpaceBoxDimension(low=0, high=255),
    ]))),

    # Test Box with Infinite characters
    (Box(low=-np.inf, high=np.inf, shape=(2,2)), rw.MetaSpaceWrapper(box=rw.MetaSpaceBox(shape=[2, 2], dimensions=[
        rw.MetaSpaceBoxDimension(low=-1e100, high=1e100),
        rw.MetaSpaceBoxDimension(low=-1e100, high=1e100),
        rw.MetaSpaceBoxDimension(low=-1e100, high=1e100),
        rw.MetaSpaceBoxDimension(low=-1e100, high=1e100),
    ]))),

    (Box(low=np.array([ -1.0, -2.0 ]), high=np.array([ 2.0, 4.0 ]), shape=(2, )), rw.MetaSpaceWrapper(box=rw.MetaSpaceBox(shape=[2], dimensions=[
        rw.MetaSpaceBoxDimension(low=-1.0, high=2.0),
        rw.MetaSpaceBoxDimension(low=-2.0, high=4.0)
    ]))),

    # Test Tuple
    (
        Tuple([
            Box(0, 100, shape=(2, )), # (x, y)
            Discrete(4) # Wind direction (N, E, S, W)
        ]),
        rw.MetaSpaceWrapper(tuple=rw.MetaSpaceTuple(spaces=[
            rw.MetaSpaceWrapper(
                box=rw.MetaSpaceBox(shape=[2], dimensions=[
                    rw.MetaSpaceBoxDimension(low=0, high=100),
                    rw.MetaSpaceBoxDimension(low=0, high=100)
                ])
            ),
            rw.MetaSpaceWrapper(discrete=rw.MetaSpaceDiscrete(n=4))
        ]))
    ),

    # Test Nested Tuple
    (
        Tuple([
            Tuple([ Discrete(3) ]),
            Box(0, 100, shape=(2, )), # (x, y)
            Discrete(4) # Wind direction (N, E, S, W)
        ]),
        rw.MetaSpaceWrapper(tuple=rw.MetaSpaceTuple(spaces=[
            rw.MetaSpaceWrapper(
                tuple=rw.MetaSpaceTuple(spaces=[
                    rw.MetaSpaceWrapper(discrete=rw.MetaSpaceDiscrete(n=3))
                ])
            ),
            rw.MetaSpaceWrapper(
                box=rw.MetaSpaceBox(shape=[2], dimensions=[
                    rw.MetaSpaceBoxDimension(low=0, high=100),
                    rw.MetaSpaceBoxDimension(low=0, high=100)
                ])
            ),
            rw.MetaSpaceWrapper(discrete=rw.MetaSpaceDiscrete(n=4))
        ]))
    )
])
def test_meta_space_serialization(tests):
    u, s = tests

    # Test Serialization
    assert Serializer.serializeMeta(u) == s

    # Test Unserialization
    assert Unserializer.unserializeMeta(s) == u