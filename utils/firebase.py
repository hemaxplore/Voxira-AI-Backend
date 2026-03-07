import pyrebase

firebase_config = {
  "apiKey": "AIzaSyCAcpxmCy4feBhnT5OhrpKx7dUAOq_c25E",
  "authDomain": "hema-transcription-app.firebaseapp.com",
  "projectId": "hema-transcription-app",
  "storageBucket": "hema-transcription-app.firebasestorage.app",
  "messagingSenderId": "612273721760",
  "appId": "1:612273721760:web:3b977681c2f4e79dcb14c5",
  "databaseURL" :"https://hema-transcription-app-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
