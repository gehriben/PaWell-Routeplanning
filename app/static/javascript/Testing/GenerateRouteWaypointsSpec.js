
describe("test waypoints generation", function() {
    /*beforeEach(function() {
    player.play(song);
    player.pause();
    });*/


    it("should return a correct route array", function() {
        let expectedOuterRouteArray = []
        let expectedInnerRouteArray = []
        
        expectedInnerRouteArray.push({location: [8.709515425701452, 47.50203989067776], stopover: true})
        expectedInnerRouteArray.push({location: [8.576781346935414, 47.5182112218522], stopover: true})
        expectedInnerRouteArray.push({location: [8.600694201706197, 47.51849791968558], stopover: true})
        expectedInnerRouteArray.push({location: [8.555951252036843, 47.517012917621074], stopover: true})
        expectedInnerRouteArray.push({location: [8.677404497663854, 47.51600630799501], stopover: true})
        expectedInnerRouteArray.push({location: [8.683327179003115, 47.51636457830649], stopover: true})
        expectedInnerRouteArray.push({location: [8.630510210161166, 47.51659227446575], stopover: true})

        expectedOuterRouteArray.push(expectedInnerRouteArray);

        let actualRouteArray = collectWaypointsOfRoutes([[8.709515425701452, 47.50203989067776], 
            [8.576781346935414, 47.5182112218522], [8.600694201706197, 47.51849791968558], [8.555951252036843, 47.517012917621074], 
            [8.677404497663854, 47.51600630799501], [8.683327179003115, 47.51636457830649], [8.630510210161166, 47.51659227446575]]);
        
        expect(actualRouteArray).toEqual(expectedOuterRouteArray);
    });

    it("should return a correct route array with 2 routes", function() {
        let snappedCoordinates = [];
        let expectedOuterRouteArray = []
        let expectedRouteArray1 = []
        let expectedRouteArray2 = []
        
        //Erstelle die Parameter für die Funktion
        for(i=0; i<30; i++) {
            snappedCoordinates.push([8.709515425701452, 47.50203989067776]);
        }

        //Erstelle das erste Route Array
        for(i=0; i<25; i++) {
            expectedRouteArray1.push({location: [8.709515425701452, 47.50203989067776], stopover: true})
        }

        //Erstelle das zweite Route Array
        for(i=0; i<5; i++) {
            expectedRouteArray2.push({location: [8.709515425701452, 47.50203989067776], stopover: true});
        }

        expectedOuterRouteArray.push(expectedRouteArray1);
        expectedOuterRouteArray.push(expectedRouteArray2);

        let actualRouteArray = collectWaypointsOfRoutes(snappedCoordinates);
        
        expect(actualRouteArray).toEqual(expectedOuterRouteArray);
    });

    it("should return the correct waypoint", function() {
        let coordinates = [8.723377, 47.498805]
        let waypoint = { location: coordinates, stopover: true }

        expect(generateWaypoint(coordinates)).toEqual(waypoint);
    });
});
  