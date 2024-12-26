    let map;
    const image ="https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

    function addLanding(latLng) {
      // Create a takeoff
      const landing = new google.maps.Marker({
        position: latLng,
        map: map,
        draggable: false, // Allow landing to be draggable
        icon: image,
        title: "Посадка"
      });

      // Add a click listener for the landing
      landing.addListener("click", () => {
        const infoWindow = new google.maps.InfoWindow({
          content: `${landing.getTitle()}<br>
            Широта: ${latLng.lat()}, Довгота: ${latLng.lng()}`,
        });
        infoWindow.close();
        infoWindow.open(map, landing);
      });
    }

    function addTakeoff(latLng) {
      // Create a takeoff
      const takeoff = new google.maps.Marker({
        position: latLng,
        map: map,
        draggable: false, // Allow takeoff to be draggable
        icon: image,
        title: "Зліт"
      });

      // Add a click listener for the takeoff
      takeoff.addListener("click", () => {
        const infoWindow = new google.maps.InfoWindow({
          content: `${takeoff.getTitle()}<br>Широта: ${latLng.lat()}, Довгота: ${latLng.lng()}`,
        });
        infoWindow.close();
        infoWindow.open(map, takeoff);
      });
    }

    function addMarker(id, latLng) {
      // Create a marker
      const marker = new google.maps.Marker({
        position: latLng,
        map: map,
        draggable: false, // Allow marker to be draggable
        label: `${id}`,
      });

      // Add a click listener for the marker
      marker.addListener("click", () => {
        const infoWindow = new google.maps.InfoWindow({
          content: `Широта: ${latLng.lat()}, Довгота: ${latLng.lng()}`,
        });
        infoWindow.close();
        infoWindow.open(map, marker);
      });
    }

    function initMap() {
      map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: { lat: 34.84555, lng: -111.8035 },
      });

      // Define a symbol using a predefined path (an arrow)
      // supplied by the Google Maps JavaScript API.
      const lineSymbol = {
        path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
      };

      // Draw polyline using points_array
      polyline = new google.maps.Polyline({
          path: {{ points_array | tojson }},
          geodesic: true,
          strokeColor: "#FF0000",
          strokeOpacity: 1.0,
          strokeWeight: 2,
          icons: [{
            icon: lineSymbol,
            offset: "100%",
            },],
      });

      polyline.setMap(map);
    }

    function fetchAndDisplayMarkers() {
      // Create an empty bounds object
      const bounds = new google.maps.LatLngBounds();

      fetch('/map_get_targets')
        .then(response => response.json())
        .then(targets => {
          targets.forEach(target => {
            const latLng = new google.maps.LatLng(target.lat, target.lng);
            addMarker(target.id,latLng); // Add marker using the addMarker function
            bounds.extend(latLng); // Extend bounds to include the marker
          });
          // Fit the map to the bounds
          map.fitBounds(bounds);
        })
        .catch(error => {
          console.error('Error fetching targets:', error);
        });

      fetch('/map_get_takeoffs')
        .then(response => response.json())
        .then(takeoffs => {
          takeoffs.forEach(takeoff => {
            const latLng = new google.maps.LatLng(takeoff.lat, takeoff.lng);
            addTakeoff(latLng); // Add marker using the addMarker function
            bounds.extend(latLng); // Extend bounds to include the marker
          });
          // Fit the map to the bounds
          map.fitBounds(bounds);
        })
        .catch(error => {
          console.error('Error fetching takeoffs:', error);
        });

      fetch('/map_get_landings')
        .then(response => response.json())
        .then(landings => {
          landings.forEach(landing => {
            const latLng = new google.maps.LatLng(landing.lat, landing.lng);
            addLanding(latLng); // Add marker using the addMarker function
            bounds.extend(latLng); // Extend bounds to include the marker
          });
          // Fit the map to the bounds
          map.fitBounds(bounds);
        })
        .catch(error => {
          console.error('Error fetching landings:', error);
        });
    }
    window.initMap = initMap;
    // Call this function to fetch targets and display markers when the page loads
    window.onload = fetchAndDisplayMarkers;