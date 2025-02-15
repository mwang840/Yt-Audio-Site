from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL
import requests


def downloadYtVideo(ytLink: str):
    """
    Takes in the current youtube link you want to download and returns the path where you downloaded the file
    
    Args:
    current_url (str), the youtube link passed in
    Returns:
        the directory path where the video is downloaded (assuming the download goes successful)
    """
    req = requests.head(ytLink, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'}).url


    if "youtube.com" in req:
        try:
            ytdl_options = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s'
    }
            with YoutubeDL(ytdl_options) as ydl:
                ydl.download(ytLink)
                return "Downloading Video Completed"
        except:
                print("Video Failed, please try again!")
                return None 
    return

#Start the Flask Application
app = Flask(__name__)

@app.route("/")
def render_website():
     return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_vid():
     ytData = request.form.get("ytlink")
     if ytData:
          downloadedVideo = downloadYtVideo(ytData)
          return render_template("index.html")
          
     else:
          return jsonify({"Downloading the video failed or no link provided"}), 400
     

def main():
    current_url  = str(input("Enter the url you want to put here\n"))
    downloadedClip = downloadYtVideo(current_url)
    print(downloadedClip)

if __name__ in "__main__":
     app.run(host="localhost", debug=True)
    