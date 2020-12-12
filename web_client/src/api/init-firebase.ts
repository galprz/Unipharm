import firebaseClient from "firebase/app";
import firebaseConfig from "./config/firebase.conn.json";
import "firebase/auth";
import "firebase/firestore";
firebaseClient.initializeApp(firebaseConfig);
export const authClient = firebaseClient.auth();
export const firestoreClient = firebaseClient.firestore();
export const deleteFlag = firebaseClient.firestore.FieldValue.delete();
