import firebaseClient from './init-firebase'


export class FirestoreClient{

 
    private  getDocRef(path : string) {
        const db = firebaseClient.firestore()
        let parity = 0
        let mold : Array<string>
        let applyPathOn = (databaseRef: any)=>{
            var intermediateDocRef = databaseRef.collection(path.split('/')[0]).doc(path.split('/')[1])

            path.split('/').slice(2).forEach((name)=>{
                mold[parity] = name
                parity = 1 - parity
                if(parity===0){
                    intermediateDocRef = intermediateDocRef.collection(mold[0]).doc(mold[1])
                }
            })
            return intermediateDocRef;
        }

        return applyPathOn(db);
    }

    private async fieldsExist(path: string, fields : Array<string>) : Promise<boolean>{
        return this.pathExists(path).then(async(res)=>{
            if(res){
                const document = await this.read(path)
                const docKeys = Object.keys(document)
                let flag = false;
                fields.forEach((field)=>{if(!docKeys.includes(field)){ flag = true;}})
                return flag
            }else{
                return false
            }
        })
    }

    private async  pathExists(path: string) : Promise<boolean>{
        const promise = await this.getDocRef(path).get()
        return promise.exists;
    }


    async read(path: string): Promise<JSON>{
        return this.pathExists(path).then(async (res) => {
            if (res) {
                const promise = await this.getDocRef(path).get()
                return promise.data()
            }
            else {
                console.log("error - trying to read a non-existing document")
                return new Promise<JSON>((resolve, undef) => JSON.parse("{}"))
            }
        }).catch((err) => {
            console.log("The following error occured while trying to read: " + err)
            return new Promise<JSON>((resolve, undef) => JSON.parse("{}"))
        })
             
    }

    async update(path: string, data : JSON) : Promise<void>{
        this.pathExists(path).then(async (res)=>{
            if(!res){
                console.log("error - trying to update a non-existing document");
            }
            else{
                const promise = await this.getDocRef(path).update(data);
                return promise
            }
        }).catch(async (err)=>{alert("The following error occured while trying to update: "+err)})
    }

    async create(path: string, data : JSON) : Promise<void>{
        this.pathExists(path).then(async (res)=>{
            if(res){
                console.log("error - trying to create an existing document ");
            }
            else{
                const promise = await this.getDocRef(path).set(data);
                return promise
            }
        }).catch(async (err)=>{console.log("The following error occured while trying to create: "+err)})

    }

    async deleteFields(path: string, fields : Array<string>) : Promise<void>{
        this.fieldsExist(path,fields).then(async (res)=>{
            if(!res){
                console.log("error - trying to delete a non-existing document");
            }
            else{
                let x = JSON.parse("{}")
                fields.forEach((field)=>{x[field]=firebaseClient.firestore.FieldValue.delete()})
                const promise = await this.getDocRef(path).update(x)
                return promise
            }
        }).catch(async (err)=>{console.log("The following error occured while trying to delete fields: "+err)})
        
    }

    async deleteDocument(path : string){
        this.pathExists(path).then(async (res)=>{
            if(!res){
                console.log("error - trying to delete a non-existing document");
            }
            else{
                
                const promise = await this.getDocRef(path).delete()
                return promise
            }
        }).catch(async (err)=>{console.log("The following error occured while trying to delete a document: "+err)})
    }
}
