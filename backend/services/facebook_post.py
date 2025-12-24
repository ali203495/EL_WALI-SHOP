
import httpx
import os
import json

class FacebookPostService:
    def __init__(self):
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN") # Using the same token variable as CAPI for simplicity if it works, or user can change it
        self.api_version = "v19.0"
    
    async def post_product(self, product):
        """
        Post a new product to the Facebook Page.
        """
        if not self.page_id or not self.access_token:
            print("Facebook Auto-Post: Missing credentials (PAGE_ID or ACCESS_TOKEN). Skipping.")
            return

        print(f"Facebook Auto-Post: Attempting to post product '{product.name}'...")

        message = (
            f"🌟 New Arrival! 🌟\n\n"
            f"{product.name}\n"
            f"{product.description[:200] + '...' if product.description and len(product.description) > 200 else (product.description or '')}\n\n"
            f"Price: {product.price} AED\n\n"
            f"Shop now! 🛍️"
        )
        
        # If we had a public URL for the product, we would add it here.
        # For now, just the general shop link or no link if not provided.

        async with httpx.AsyncClient() as client:
            try:
                # 1. If there's an image, post as a photo
                if product.image_url:
                    # Check if image_url is a full URL or a relative path
                    image_url = product.image_url
                    if not image_url.startswith("http"):
                        # If it's a local path, we might need to upload the file binary
                        # But for now assuming it's a serve-able URL or we skip image.
                        # Actually, if it's local in 'uploads/', we can try to construct current host url if passed,
                        # OR if we just send the URL to FB, FB needs to be able to reach it.
                        # Since this is likely localhost in dev, FB can't reach localhost.
                        # So we should probably upload the image bytes if it's local.
                        pass

                    # Strategy: Use /photos endpoint
                    # If localhost, we must upload bytes. 
                    # If production, we can use 'url' param.
                    
                    # For robust handling, let's try to pass the 'url' if it looks public, 
                    # otherwise warn we can't post local images easily without public reachability.
                    # However, to be helpful, let's assume we might be in dev and only text works safely,
                    # OR we try to send the image URL if it's public (Cloudinary).
                    
                    # If using Cloudinary (as per env_example hint), it's http/https.
                    url = f"https://graph.facebook.com/{self.api_version}/{self.page_id}/photos"
                    payload = {
                        "message": message,
                        "url": image_url,
                        "access_token": self.access_token
                    }
                    if not image_url.startswith("http"):
                         # Fallback to feed (text only) if we can't serve the image
                         print("Facebook Auto-Post: Image URL is local, cannot send to Facebook unless public. Posting text only.")
                         url = f"https://graph.facebook.com/{self.api_version}/{self.page_id}/feed"
                         payload = {
                            "message": message,
                            "access_token": self.access_token
                        }
                    
                else:
                    # 2. Text only post
                    url = f"https://graph.facebook.com/{self.api_version}/{self.page_id}/feed"
                    payload = {
                        "message": message,
                        "access_token": self.access_token
                    }

                response = await client.post(url, params=payload) # params for url query string, or data/json? 
                # FB Graph API usually takes params or form-data. httpx 'params' goes to query string.
                # For POST, usually 'data' or 'json'.
                # Let's use 'data' for form fields which FB usually accepts.
                
                response = await client.post(url, data=payload)

                if response.status_code == 200:
                    post_id = response.json().get("id")
                    print(f"Facebook Auto-Post: Success! Post ID: {post_id}")
                else:
                     print(f"Facebook Auto-Post: Failed. {response.status_code} - {response.text}")

            except Exception as e:
                print(f"Facebook Auto-Post: Exception occurred: {e}")

facebook_service = FacebookPostService()
