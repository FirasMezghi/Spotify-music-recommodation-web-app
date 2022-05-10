from flask import Flask,render_template,url_for,request,jsonify
from flask_cors import cross_origin
import pandas as pd
from recomend import process_song
from extract_feature_song import ari_to_features

app = Flask(__name__, template_folder="templates")

complete_feature_set_new=pd.read_csv('C:\\Users\\user\\spot_recom\\complete_feature.csv')
music=pd.read_csv('C:\\Users\\user\\spot_recom\\music_featured_data.csv')

@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("recomand.html")
@app.route("/about",methods=['GET'])
@cross_origin()
def about():
	return render_template("about.html")

@app.route("/",methods=['GET', 'POST'])
@cross_origin()
def recomand():
    if request.method == "POST":
        URL = request.form['URL']
        track_uri=track_uri =str(URL).split("/")[-1].split("?")[0]
        features=ari_to_features(track_uri)
        recom=process_song(features,complete_feature_set_new)
        number_of_recs = int(request.form['number-of-recs'])
        my_songs = []
        for i in range(number_of_recs):
            print(list(recom['id'])[i])
            my_songs.append("https://open.spotify.com/track/"+str(list(recom['id'])[i])+"?si=289110ef0f664dd0")
        return render_template('result.html',songs= my_songs)
    return render_template("recomand.html")

if __name__=='__main__':
	app.run(debug=True)