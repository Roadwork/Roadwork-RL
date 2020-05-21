# SDKs

The SDKs utilize the well known [OpenAI Specification](https://github.com/openai/gym/blob/master/gym/core.py) but will implement these differently due to the server / client split. For the end-user however nothing is being changed.

## Implemented

* [Python](./sdks-python.md)
* [Node.JS](./sdks-node.md)

## Writing your own

Writing your own SDK client is as easy as hooking onto the gRPC API that is being created on the server. For a general overview of this specification, refer to this [document](../simulator/api.md).

An example of this can be found in the `./src/Clients/python/Client.py` file, implementing the gRPC server API.