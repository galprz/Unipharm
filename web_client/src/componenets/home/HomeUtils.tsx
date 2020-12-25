export default class Utils {

    static getLocations()
    {
        const locations : Array<[number, number, number]> = []
        var xDistance = 10;
        var yDistance = 7;
        var zDistance = 30;
        var xOffset = -135;
        var yOffset = 5;

        for(var i = 0; i < 15; i++){
            for(var j = 0; j < 20; j++){
                for(var k = 0; k < 3; k++){
                    locations.push([xDistance * i + xOffset, yDistance * j + yOffset, zDistance * k]);
                }
            }
        }

        return locations;
    }

    static getColor(index: number)
    {
        return index % 90; //This means nothing
    }

}