import {ManagementClient} from "../../api/stock_management/ManagementClient";
import axios from 'axios';

export default class Utils {

    static async getLocations()
    {
        const locations : Array<[number, number, number]> = await ManagementClient.getAllLocations();
        return locations;
    }

    static async getMaterials()
    {
        var materials : Array<String> = await ManagementClient.getAllMaterials();
        return materials;
    }

    static async getColor(x: number, y: number, z: number, material: String)
    {
        var returnVal = false;
        await axios.get("http://localhost:8080/box_status",
            { params: 
                {location_id: x+","+y+","+z,
                material: material}}
        ).then(response => {
            // success
           console.log({result: response.data});
           console.log(response.data.success);
           if(x === -5)
           {
            returnVal = false;
           }
           else
           {
            returnVal = response.data.success;
           }
        })
        .catch((error) => {
            // handle this error
            console.log(error);
            returnVal = false;
        });
        return returnVal;
    }
}