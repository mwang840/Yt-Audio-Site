from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from yt_dlp import YoutubeDL
import requests
import os
from pathToDownload import filePath

#sets the downloaded file to the downloads folder
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True, mode=0o755)

#Sets up the port
SERVER_IP = "0.0.0.0"
PORT = 8000

def downloadYtVideo(ytLink: str):
    """
    Takes in the current youtube link you want to download and returns the path where you downloaded the file
    
    Args:
    current_url (str), the youtube link passed in
    Returns:
        the directory path where the video is downloaded (assuming the download goes successful)
    """
    # Makes a requests with the given url
    req = requests.head(ytLink, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'}).url
    #If the requests has "youtube.com" in it, yt-dlp downloads it, set
    if "youtube.com" in req:
        try:
            ytdl_options = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
    }
            '''
            Create a YoutubeDL object with the given options passed in, extract the information about the link
            and then prepares the output file with the output file name as an .mp3 file
            '''
            with YoutubeDL(ytdl_options) as ydl:
                current_file = ydl.extract_info(ytLink)
                ytFileName = ydl.prepare_filename(current_file).replace(".webm", ".mp3").replace(".m4a", ".mp3")
                return ytFileName
            '''
            Otherwise it fails to download and returns a 500 error
            '''
        except:
                print("Video Failed, please try again!")
                return None
    return None

#Start the Flask Application
app = Flask(__name__)


@app.route("/")
def render_website():
     """
     The Function For Starting up the web page with the default url
     """
     return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_vid():
     """
     When the User clicks the button to download the video, the data from the form gets sent
     and calls the downloadYtVideo function above and then redirects the url for downloading the current youtube link,
     if the status of the form is 200
     """
     ytData = request.form.get("ytlink")
     if not ytData:
        return jsonify({"Downloading the video failed or no link provided"}), 400
     downloadedVideo = downloadYtVideo(ytData)
     print(downloadedVideo)
     if downloadedVideo != None:
          currentFileName = os.path.basename(downloadedVideo)
          print(type(currentFileName))
          print(currentFileName)
          return redirect(url_for("return_downloaded_file", filename=currentFileName))
     else:
        return "Downloading video failed", 500

@app.route("/download/<path:filename>")
def return_downloaded_file(filename: str):
     """
     Takes in a youtube link that was passed in the input form, then call join paths with the downloads folder
     and send the file as an attachment
     """
     file_path = os.path.join(DOWNLOAD_FOLDER, filename)
     return send_file(file_path, as_attachment=True)     

@app.route("/downloadprogram")
def download_program():
     path = filePath
     return send_file(path, as_attachment=True)


def main():
    current_url  = str(input("Enter the url you want to put here\n"))
    downloadYtVideo(current_url)

#Runs the flask application
if __name__ in "__main__":
     app.run(debug=True, host=SERVER_IP, port=PORT)
    