import firebase from 'firebase'

var firebaseConfig = {
    apiKey: "AIzaSyCk2FLrVTdxtTnR46TNRJ2aKu0si0sUqsc",
    authDomain: "unifarm-f9b90.firebaseapp.com",
    databaseURL: "https://unifarm-f9b90.firebaseio.com",
    projectId: "unifarm-f9b90",
    storageBucket: "unifarm-f9b90.appspot.com",
    messagingSenderId: "418423550260",
    appId: "1:418423550260:web:a45d8656b73299e812f561",
    measurementId: "G-HXXDLKW6LD"
};
// Initialize Firebase
const fire = firebase.initializeApp(firebaseConfig);
firebase.analytics();

export default fire