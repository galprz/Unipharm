import { FirestoreClient } from "../firestore";
interface SettingsJSON extends JSON {
  test: boolean;
}

class SettingsClient {
  private static readonly settingsPath = "dev/setting";

  static getSettings(): Promise<SettingsJSON> {
    return FirestoreClient.read(
      SettingsClient.settingsPath
    ) as Promise<SettingsJSON>;
  }

  static saveSettings(newSettings: SettingsJSON): Promise<void> {
    return FirestoreClient.update(SettingsClient.settingsPath, newSettings);
  }
}
export default SettingsClient;
