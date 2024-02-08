def remove_dead_end(route):
    #Rekursive Funktion für das Entfernen von Sackgassen
    #Prüft identische Wegpunkte von Zwischenrouten, wenn mehr als 2 existieren, handelt es sich um eine Sackgasse

    #Parameters:
    #    route (json) : Route, die initial von der Directions API zurückgegeben wird.

    #Returns:
    #    actual_waypoints (json) : Eine Route, bei der ein Wegpunkt entfernt wurde

    actual_waypoints = []
    actual_waypoints.append([route[0]['start_location']['lat'],route[0]['start_location']['lng']])
    removed = 0
    for previous, current in zip(route, route[1:]):
        last_idx = len(previous['steps']) - 1
        temp_current = current['steps'][0]['path']
        temp_last = previous['steps'][last_idx]['path']

        next_array = []
        last_array = []

        for i in temp_current:
            next_array.append([i['lat'], i['lng']])

        for j in temp_last:
            last_array.append([j['lat'], j['lng']])

        counter = 0
        # check path points of current and last path
        for k in last_array:
            for l in next_array:
                if k == l:
                    counter += 1
        
        if counter == 1 and (len(current['steps']) < 2):
            removed += 1
        elif counter < 2:
            actual_waypoints.append([current['start_location']['lat'], current['start_location']['lng']])
        else:
            removed += 1

    if removed != 0 and len(actual_waypoints) + 1 != len(route):
        return actual_waypoints
    else:
        return "finished"



