import httpx
import os
import time

class FacebookCAPIService:
    def __init__(self):
        self.pixel_id = os.getenv("FACEBOOK_PIXEL_ID")
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.api_version = "v19.0"
        self.enabled = bool(self.pixel_id and self.access_token)

    async def send_event(self, event_name: str, event_data: dict, user_data: dict = None):
        """
        Send an event to Meta Conversions API
        """
        if not self.enabled:
            print(f"Meta CAPI disabled (missing credentials). Event '{event_name}' skipped.")
            return

        url = f"https://graph.facebook.com/{self.api_version}/{self.pixel_id}/events"
        
        payload = {
            "data": [
                {
                    "event_name": event_name,
                    "event_time": int(time.time()),
                    "action_source": "website",
                    "user_data": user_data or {"client_user_agent": "Maison-Backend"},
                    "custom_data": event_data
                }
            ],
            "access_token": self.access_token
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    print(f"Meta CAPI: Event '{event_name}' sent successfully.")
                else:
                    print(f"Meta CAPI Error: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Meta CAPI Exception: {str(e)}")

# Singleton instance
fb_capi = FacebookCAPIService()
