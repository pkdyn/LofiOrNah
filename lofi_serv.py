
import pickle
from flask import Flask, render_template, request
app = Flask('lofi')


def predict_single(samp, dv, rf): 
    X = dv.transform([samp]) 
    y_pred = rf.predict_proba(X)[0, 1] 
    return y_pred

with open('lofi.bin', 'rb') as f_in:
   dv, rf = pickle.load(f_in)


@app.route('/')
def home():   
    title_text = "This is a lofi predictor"
    title = {'titlename':title_text}
    return render_template('home.html',title=title)

@app.route('/show-prediction/')
def predict():
    
    
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    import re

    def validate_spotify_link(link):
        pattern = r"^https:\/\/open\.spotify\.com\/track\/[A-Za-z0-9]+(\?si=[A-Za-z0-9]+)?$"
        if re.match(pattern, link):
            return True
        else:
            return False

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials( client_id=  "9f133c4fea4142498c182dc76383ce4d",
                                                            client_secret= "84511eaa3a0c4ef6aaf6350ec8ff4d1b"))

    sid = request.args.get('inp')
    is_valid = validate_spotify_link(sid)
    
    tracks=[sid]


    def track_info(tracks) :
            audio_features = sp.audio_features(tracks)[0]

            samp={
            'bpm':  round(audio_features['tempo']),
            'energy': round(audio_features['energy']*100),
            'dance': round(audio_features['danceability']*100),
            'loud': round(audio_features['loudness']),
            'valence':  round(audio_features['valence']*100),
            'lens': round(audio_features['duration_ms']/1000), 
            'acoustic':round(audio_features['acousticness']*100)
            }
            return samp

    
    

    samp={}
    samp=track_info(tracks)
    samp
    predict_single(samp, dv, rf)

    predict=predict_single(samp, dv, rf)
    if predict >= 0.5:
        predict_string = "yes it's lofi: " + str(round(predict*100)) + "%"
    else:
        predict_string = "nyet it's not lofi"
    
    prediction = {'prediction_key': predict_string, 'valid_link': is_valid}
    return(render_template('show-prediction.html',prediction=prediction))
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)