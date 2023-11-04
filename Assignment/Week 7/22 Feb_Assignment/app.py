import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask, render_template

app = Flask(__name__)

def scrape_youtube():
    open_br = webdriver.Chrome()
    url = "https://www.youtube.com/@PW-Foundation/videos"
    open_br.get(url)

    video_elements = open_br.find_elements(By.TAG_NAME, "a")
    videos = []
    for element in video_elements:
        url = element.get_attribute("href")
        if url is not None and "/watch?v=" in url and url not in videos and len(videos) < 5:
            videos.append(url)

    thumbnail_elements = open_br.find_elements(By.XPATH, "//*[@id='thumbnail']/yt-image/img")
    thumbnails = []
    for thumb in thumbnail_elements:
        src = thumb.get_attribute("src")
        if src is not None:
            thumbnails.append(src)

    while len(thumbnails) < 5:
        thumbnails.append("no more url")

    title_elements = open_br.find_elements(By.XPATH, "//*[@id='video-title']")
    titles = [title.text for title in title_elements[:5]]
 
    view_elements = open_br.find_elements(By.XPATH, "//*[@id='metadata-line']/span[1]")
    views = [view.text for view in view_elements[:5]]

    duration_elements = open_br.find_elements(By.XPATH, "//*[@id='metadata-line']/span[2]")
    durations = [dur.text for dur in duration_elements[:5]]

    open_br.quit()

    return videos, thumbnails, titles, views, durations

def save_to_csv_file(video, thumbnail, title, views, durations):
    reviews = []
    for i in range(5):
        mydict = {
            "VideoLink": str(video[i]),
            "ThumbnailUrl": str(thumbnail[i]),
            "VideoTitle": str(title[i]),
            "Views": str(views[i]),
            "Time of Upload": str(durations[i])
        }
        reviews.append(mydict)

    with open("data_csv/data.csv", "w", newline='', encoding='utf-8') as w:
        headers = ["VideoLink", "ThumbnailUrl", "VideoTitle", "Views", "Time of Upload"]
        writer = csv.DictWriter(w, fieldnames=headers)
        writer.writeheader()
        writer.writerows(reviews)

@app.route('/')
def index():
    video, thumbnail, title, views, durations = scrape_youtube()
    return render_template('index.html', video=video, thumbnail=thumbnail, title=title, views=views, durations=durations)

if __name__ == '__main__':
    app.run(debug=True)
