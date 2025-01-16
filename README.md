# tiktok-dl
Download your important content off of TikTok

# First
Submit a request to download your data.  Instructions are here:  https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/requesting-your-data
Pick 'JSON' as your file format.

# Next
Move that zip file to a computer, unzip it somewhere (it'll have one big JSON file in it).

# Then
Clone this repo.  Pull the dependencies using the requirments.txt. Run the app, providing the command options you want.

## Examples:

- python main.py .\user_data_tiktok.json M:\tiktok_data\ --type my-videos
- - Downloads YOUR videos to a subfolder named "my-videos"
  - The videow will be named according to the date/time they were created, so will be in chronological order.
- python main.py .\user_data_tiktok.json M:\tiktok_data\ --type favorites
- - Downloads your Favorite-d videos to a folder named "favorites"
  - The videos will be named according to when you favorited them, so won't be in order by creation date/time, but in the order you saw and Favorited them.

# DANGER
Videos are large.  You may have thousands of favorited videos and - depending on how prolific a content-creator you are - as many personal videos.  BE SURE YOU HAVE A LOT OF DISK SPACE!


