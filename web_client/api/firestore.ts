import {firebaseClient} from './init-firebase'

interface IFirePath{
    readonly path : string
    asArray(p : string) : Array<[string, string]>
}

export class FirestoreClient{
 
    private  getDocRef(path: IFirePath) {
        let docRef = firebaseClient.firestore()
        path.asArray(path.path).forEach(function([collectionName, DocumentName]){
            docRef = docRef.collection(collectionName).doc(DocumentName)
        })
        return docRef;
    }

    private async pathExists(path: IFirePath){
        const saidDocument = await this.getDocRef(path).get()
        return saidDocument.exists;
    }

    private writeJsonToDocument(path: IFirePath, data: Array<[string,string]>){
        var docRef = this.getDocRef(path);
        data.forEach(function([key,value]){
            docRef.set({key: value})
        })
    }

    async read(path: IFirePath){
        var doc = await this.getDocRef(path).get();
        return doc.data();
        
    }

    update(path: IFirePath, data : Array<[string,string]>){
        if(this.pathExists(path)) this.writeJsonToDocument(path,data);
    }

    create(path: IFirePath, data : Array<[string,string]>){
        if(!this.pathExists(path)) this.writeJsonToDocument(path,data);
    }

    delete(path: IFirePath, field : string){
        if(this.pathExists(path)){
            const ref = this.getDocRef(path)
            ref.update({field: firebaseClient.firestore.FieldValue.delete()})
        }
    }
}
