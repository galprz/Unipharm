import {ManagementClient} from "../../api/stock_management/ManagementClient";

export default class Utils {

    static async getLocations()
    {
        const locations : Array<[number, number, number]> = await ManagementClient.getAllLocations();
        return locations;
    }

    static getColor(x: number, y: number, z: number)
    {
        return x % 15; //This means nothing
    }

}