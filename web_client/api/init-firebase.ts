// Firebase App (the core Firebase SDK) is always required and
// must be listed before other Firebase SDKs
var firebase = require("firebase/app");

// Add the Firebase products that you want to use
require("firebase/auth");
require("firebase/firestore");
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCk2FLrVTdxtTnR46TNRJ2aKu0si0sUqsc",
  authDomain: "unifarm-f9b90.firebaseapp.com",
  databaseURL: "https://unifarm-f9b90.firebaseio.com",
  projectId: "unifarm-f9b90",
  storageBucket: "unifarm-f9b90.appspot.com",
  messagingSenderId: "418423550260",
  appId: "1:418423550260:web:a45d8656b73299e812f561",
  measurementId: "G-HXXDLKW6LD"
};

firebase.initializeApp(firebaseConfig);
firebase.analytics();

export {firebase}