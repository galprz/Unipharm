import * as firestoreClient  from '../firestore'
interface SettingsJSON{
    test: boolean
}

class SettingsClient{
    private firestoreClientRef;
    private settingsPath = 'dev/setting'
      
    constructor(){
        this.firestoreClientRef = new firestoreClient.FirestoreClient()
    }

    getSettings(){
        return this.firestoreClientRef.read(this.settingsPath)
    }

    saveSettings(newSettings: SettingsJSON){
        return this.firestoreClientRef.update(this.settingsPath,JSON.parse("{\"test\" : "+newSettings.test+"}"))
    }
}

const settingsSingleton = new SettingsClient();
export default settingsSingleton