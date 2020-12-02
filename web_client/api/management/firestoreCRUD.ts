interface IFirePath{
    readonly path : string
    asArray(p : string) : Array<[string, string]>
}

import {firebase} from './init-firebase'

function getDocRef(path: IFirePath) {
    var databaseReference = firebase.firestore()
    var docRef = databaseReference
    path.asArray(path.path).forEach(function([collectionName, DocumentName]){
        docRef = docRef.collection(collectionName).doc(DocumentName)
    })
    return docRef;
}


function readDocument(path: IFirePath){
    var docRef = getDocRef(path);
    docRef.get().then(function(doc: { data: () => any }) {
            return doc.data()
    });
}

function updateDocument(path: IFirePath, data : Array<[string,string]>){
    var docRef = getDocRef(path);
    data.forEach(function([key,value]){
        docRef.set({key: value})
    })

}


/*

function readSettings(){
    var db = firebase.firestore()
    var settingsRef = db.collection("dev").doc("setting");
    settingsRef.get().then(function(doc: { exists: any; data: () => any; }) {
        if (doc.exists) {
            console.log("Document data:", doc.data());
        } else {
            // doc.data() will be undefined in this case
            console.log("No such document!");
        }
    }).catch(function(error: any) {
        console.log("Error getting document:", error);
    });
}

function writeSettings(val: string){
    var db = firebase.firestore()
    var settingsRef = db.collection("dev").doc("setting");
    settingsRef.set({test : val})
}
*/
