# How to Set Up Facebook Auto-Posting

Since I am an AI, I cannot log in to your Facebook account to create a page for you. You must do this part yourself, but it is easy!

## Step 1: Create a Facebook Page
1.  Go to [facebook.com/pages/create](https://www.facebook.com/pages/create).
2.  Enter your **Page Name** (e.g., "Maison El Wali").
3.  Choose a **Category** (e.g., Jewelry/Watches).
4.  Click **Create Page**.

## Step 2: Get a Page Access Token
Refer to the Meta for Developers documentation or follow these simplified steps:
1.  Go to [developers.facebook.com](https://developers.facebook.com/).
2.  Create a **New App** > Select **Business** type.
3.  In the Dashboard, add **Graph API Explorer** to use for testing, OR:
4.  Go to **Tools > Graph API Explorer**.
5.  Select your new App.
6.  Under "User or Page", select **Get Page Access Token**.
7.  Select your new Page.
8.  **Important**: Ensure you grant the `pages_manage_posts` and `pages_read_engagement` permissions.
9.  Copy the huge string starting with `EAA...`.

## Step 3: Configure Backend
1.  Open the file `backend/.env` in your editor.
2.  Add or update these lines:
    ```bash
    FACEBOOK_PAGE_ID=<your_page_id_number>
    FACEBOOK_ACCESS_TOKEN=<your_long_token_string>
    ```
3.  Save the file.
4.  Restart your backend server.

## Step 4: Test
Run the verification script I prepared:
```bash
cd backend
./venv/bin/python verify_facebook.py
```
