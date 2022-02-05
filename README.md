# Graph Neural Networks for Song Recommendation on Spotify Playlists

This project tackles the task of creating meaningful and accurate song recommendations to Spotify Playlists by using Graph Neural Networks. The goal is to better capture the characteristics of songs by analyzing co-occurence of song pairs across thousands of playlists in the form of a graph.

To obtain the spotify playlist data, visit https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge and put the files in `data/playlists`. You will have to create these subfolders. Customize data path in `config/data-params`. To add song features follow steps in `api` folder (Tutorial still WIP). 

To run the GraphSAGE based model on the Spotify Playlist data, use this command from the root folder: `python run.py data model`.

To customize the model parameters, edit `config/model-params`.
