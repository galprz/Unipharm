import * as firestoreClient  from './../firestore'
interface SettingsJSON{
    test: boolean
}

class SettingsClient{
    private firestoreClientRef;
    private settingsPath = {
        path: "dev/setting",
        asArray: function(p: string) {return  ["dev","setting"] }
    }
    constructor(){
        this.firestoreClientRef = firestoreClient.FirestoreClient
    }

    getSettings(){
        return this.firestoreClientRef.read(this.settingsPath)
    }

    saveSettings(newSettings: SettingsJSON){
        this.firestoreClientRef.update(this.settingsPath,{"test":newSettings.test})
    }
}