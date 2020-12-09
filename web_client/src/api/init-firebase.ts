import * as firebaseClient from "firebase/app";
import firebaseConfig from './config/firebase.conn.json';
import  "firebase/auth";
import  "firebase/firestore"
firebaseClient.initializeApp(firebaseConfig);
export default firebaseClient;