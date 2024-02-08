describe("test route rating", function() {
    let directionsService;

    beforeEach(function() {
        directionsService = new google.maps.DirectionsService();
    });

    it("should calculate the correct duration of a route", function(done) {
        let actualDuration = 0;

        var request = {
            origin: 'Bülach',
            destination: 'Winterthur',
            travelMode: 'WALKING'
        };

        directionsService.route(request, function(result, status) {
            if (status == 'OK') {
                actualDuration = calculateRouteDuration(result["routes"][0]["legs"]);

                expect(actualDuration).toEqual(207);
                done();
            } 
        });
    });

    it("should calculate correct distance of a route", function(done) {
        let actualDistance = 0;

        var request = {
            origin: 'Bülach',
            destination: 'Winterthur',
            travelMode: 'WALKING'
        };

        directionsService.route(request, function(result, status) {
            if (status == 'OK') {
                actualDistance = calculateRouteDistance(result["routes"][0]["legs"]);

                expect(actualDistance).toEqual(16.5);
                done();
            } 
        });
    });
});