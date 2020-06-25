from google.protobuf.any_pb2 import Any

def to_any_pb(pb):
    """Converts a typed protobuf to the ``Any`` message type.
    Args:
        pb: the object to be converted.
    Returns:
        any_type: An instance of the pb_type message.
    Raises:
        TypeError: if the message could not be converted.
    """
    a = Any()
    a.Pack(pb)
    return a

def from_any_pb(pb_type, any_pb, type_url_prefix = "roadwork"):
    """Converts an ``Any`` protobuf to the specified message type.
    Args:
        pb_type (type): the type of the message that any_pb stores an instance of.
        any_pb (google.protobuf.any_pb2.Any): the object to be converted.
        type_uri_prefix: The prefix added to the type_uri property. Since not all serializers pass this
    Returns:
        pb_type: An instance of the pb_type message.
    Raises:
        TypeError: if the message could not be converted.
    """
    msg = pb_type()

    if not type_url_prefix == "":
        any_pb.type_url = f'type.googleapis.com/{type_url_prefix}.{pb_type.DESCRIPTOR.name}'

    # Unwrap proto-plus wrapped messages.
    if callable(getattr(pb_type, "pb", None)):
        msg_pb = pb_type.pb(msg)
    else:
        msg_pb = msg

    # Unpack the Any object and populate the protobuf message instance.
    if not any_pb.Unpack(msg_pb):
        raise TypeError(
            "Could not convert {} to {}".format(
                any_pb.__class__.__name__, pb_type.__name__
            )
        )

    # Done; return the message.
    return msg