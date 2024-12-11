import redis.asyncio as redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


async def store_otp(email: str, otp: str, ttl: int = 300):
    await redis_client.set(email, otp, ex=ttl)


async def get_otp(email: str):
    return await redis_client.get(email)


async def delete_otp(email: str):
    await redis_client.delete(email)


async def get_otp_ttl(email: str):
    ttl = await redis_client.ttl(email)
    if ttl == -1:
        return "Key exists but has no expiration"
    elif ttl == -2:
        return "Key does not exist"
    return ttl