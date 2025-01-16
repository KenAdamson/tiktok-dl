# Download Your Important Content Off TikTok

This guide will help you download your TikTok videos or favorites to your computer. Even if you’re not tech-savvy, just follow these simple steps!

---

## Step 1: Request Your TikTok Data
1. Open the TikTok app or website.
2. Submit a request to download your data by following [these instructions](https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/requesting-your-data).
3. When prompted, choose **JSON** as the file format.
4. TikTok will notify you when your data is ready to download. Save the ZIP file to your computer.

---

## Step 2: Download the Tool
1. Go to the [GitHub Repository](#) for this TikTok Video Downloader.
2. On the repository page, look for a green **Code** button.
3. Click **Code** and then select **Download ZIP**.
4. Save the ZIP file to your computer and unzip it to a folder of your choice.

---

## Step 3: Install Python (If Needed)
1. Download Python from the [official website](https://www.python.org/downloads/).
2. Run the installer and make sure to check the box that says **"Add Python to PATH"** during installation.

---

## Step 4: Install Required Libraries
1. Open a terminal or command prompt.
2. Navigate to the folder where you unzipped the tool.
3. Run the following command to install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Step 5: Prepare Your TikTok Data
1. Move the ZIP file you downloaded from TikTok to your computer.
2. Unzip the file. Inside, you’ll find a large JSON file that contains all your TikTok data.

---

## Step 6: Run the Tool
1. Open a terminal or command prompt.
2. Navigate to the folder where you unzipped the tool.
3. Run one of the following commands, depending on what you want to download:

### To Download Your TikTok Videos
```bash
python main.py path_to_json_file output_folder --type my-videos
```
- Replace `path_to_json_file` with the path to your JSON file (e.g., `./user_data_tiktok.json`).
- Replace `output_folder` with the folder where you want the videos saved.
- Videos will be named based on the date they were created, in chronological order.

### To Download Your Favorite Videos
```bash
python main.py path_to_json_file output_folder --type favorites
```
- Replace `path_to_json_file` with the path to your JSON file (e.g., `./user_data_tiktok.json`).
- Replace `output_folder` with the folder where you want the videos saved.
- Videos will be named based on when you favorited them.

---

## Important Notes
1. **Storage Space**: Videos are large. Ensure you have enough storage space on your computer before downloading.
2. **Backup Your Data**: Once TikTok is gone, this may be your only way to preserve your videos.

Feel free to ask for help if you get stuck or encounter any issues!
