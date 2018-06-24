import os
import glob
from flask import Flask, request, render_template, Response, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_script import Manager


song_dir = "songs"

application = Flask(__name__)
app = application
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    albums=os.walk(song_dir).next()[1]  #grab directories under song_dir
    #sort them by reverse modification date
    albums.sort(key=lambda x: -os.path.getmtime(song_dir+"/"+x)) 
    return render_template("index.html", title="Carlos Allende",albums=albums)

@app.route('/who')
def who():
    return render_template("who.html",title="Who")


@app.route('/invited')
def invited():
    return render_template("invited.html",title="Invited Artists")


@app.route('/<album>')
def list_songs(album):
    songs=[f for f in os.listdir(os.path.join(song_dir,album)) if f.endswith('mp3')]
    songs.sort(key=lambda x: -os.path.getmtime(os.path.join(song_dir,album,x)),reverse=True)

    #remove .mp3 from the filenames
    for i in range(len(songs)): songs[i]=songs[i].replace('.mp3','')

    stores=[]
    links=[]
    try:
      info=open(song_dir+"/"+album+"/"+album+".info",'r')
      while 1:
        line=info.readline().rstrip()
        if not line: break
        (store,link)=line.rsplit()
        stores.append(store)
        links.append(link)
      info.close()
    except:
      pass

    return render_template("songs.html", album=album, songs=songs,stores=stores,links=links)
    #return image

@app.route('/<album>/<filename>')
def play_song(album,filename):
    def generate():
      with open(song_dir+"/"+album+"/"+filename,"rb") as file:
        data=file.read(1024)
        while data:
          yield data
          data=file.read(1024)
        #file.close()

    return Response(generate(),mimetype="audio/mp3")

@app.route('/<album>/Playall')
def playall(album):
    def generate():
      songs=[f for f in os.listdir(os.path.join(song_dir,album)) if f.endswith('mp3')]
      songs.sort(key=lambda x: -os.path.getmtime(os.path.join(song_dir,album,x)),reverse=True)
      for i in range(len(songs)): 
        with open(song_dir+"/"+album+"/"+songs[i],"rb") as file:
          data=file.read(1024)
          while data:
            yield data
            data=file.read(1024)
          file.close()

    return Response(generate(),mimetype="audio/mp3")


if __name__ == '__main__':
    #app.run(host='192.168.1.107',port=5000)
    #app.run()
    manager.run()
