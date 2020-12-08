export const firebaseClient = require('firestore/app')
import firebaseConfig from './config/firebase.conn.json';
import * as _ from "firebase/auth";
import * as __ from "firebase/firestore"
firebaseClient.initializeApp(firebaseConfig);