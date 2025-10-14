import redis
import httpx
from ..core.config import settings


def get_redis_client():
    """Get Redis client - uses Upstash REST API if available, otherwise local Redis"""
    if hasattr(settings, 'UPSTASH_REDIS_REST_URL') and settings.UPSTASH_REDIS_REST_URL:
        return UpstashRedisClient()
    else:
        return redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )


class UpstashRedisClient:
    """Upstash Redis client using REST API"""
    
    def __init__(self):
        self.url = settings.UPSTASH_REDIS_REST_URL
        self.token = settings.UPSTASH_REDIS_REST_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def get(self, key):
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.url}/get/{key}", headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("result")
                return None
        except Exception:
            return None
    
    def set(self, key, value):
        try:
            with httpx.Client() as client:
                response = client.post(f"{self.url}/set/{key}", 
                                     json={"value": value}, 
                                     headers=self.headers)
                return response.status_code == 200
        except Exception:
            return False
    
    def setex(self, key, seconds, value):
        try:
            with httpx.Client() as client:
                response = client.post(f"{self.url}/setex/{key}", 
                                     json={"value": value, "ex": seconds}, 
                                     headers=self.headers)
                return response.status_code == 200
        except Exception:
            return False
    
    def delete(self, key):
        try:
            with httpx.Client() as client:
                response = client.post(f"{self.url}/del/{key}", headers=self.headers)
                return response.status_code == 200
        except Exception:
            return False
    
    def incr(self, key):
        try:
            with httpx.Client() as client:
                response = client.post(f"{self.url}/incr/{key}", headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("result", 0)
                return 0
        except Exception:
            return 0
    
    def expire(self, key, seconds):
        try:
            with httpx.Client() as client:
                response = client.post(f"{self.url}/expire/{key}", 
                                     json={"ex": seconds}, 
                                     headers=self.headers)
                return response.status_code == 200
        except Exception:
            return False


