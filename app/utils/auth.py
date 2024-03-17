from jwt import encode


def encode_jwt(payload):
    return encode(
        payload,
    )
