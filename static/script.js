
let map;
let target_id = 1;
let addTakeoffMode = false;
let addLandingMode = false;
let targets = [];
let landing = [];
let takeoff = [];
const image ="https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

function toggleAddTakeoffMode() {
    const button = document.getElementById("add-takeoff");
    if (!addTakeoffMode) {
        // If not in "Add Takeoff" mode, enter the mode
        addTakeoffMode = true;
        button.value = "Choose Takeoff on map";
    } else {
        // If already in "Add Takeoff" mode, exit the mode
        addTakeoffMode = false;
        button.value = "Add Takeoff";
    }
}

function toggleAddLandingMode() {
    const button = document.getElementById("add-landing");
    if (!addLandingMode) {
        // If not in "Add Landing" mode, enter the mode
        addLandingMode = true;
        button.value = "Choose Landing on map";
    } else {
        // If already in "Add Landing" mode, exit the mode
        addLandingMode = false;
        button.value = "Add Landing";
    }
}

function addLanding(latLng) {
  // Create a takeoff
  const landing = new google.maps.Marker({
    position: latLng,
    map: map,
    draggable: false, // Allow landing to be draggable
    icon: image,
    title: "Посадка"
  });

  // Add the landing's position to the targets array
//  Take.push({ lat: latLng.lat(), lng: latLng.lng() });

  // Add a click listener for the landing
  landing.addListener("click", () => {
    const infoWindow = new google.maps.InfoWindow({
      content: `${landing.getTitle()}<br>
        Широта: ${latLng.lat()}, Довгота: ${latLng.lng()}`,
    });
    infoWindow.close();
    infoWindow.open(map, landing);
  });

  // Add a right-click listener to remove the landing
  landing.addListener("rightclick", () => {
    landing.setMap(null); // Remove the landing from the map

    // Remove the corresponding target from the targets array
    const index = targets.findIndex(target => target.lat === latLng.lat() && target.lng === latLng.lng());
    if (index !== -1) {
      targets.splice(index, 1);
    }

    fetch('/map_delete_landing', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        latitude: landing.getPosition().lat(),
        longitude: landing.getPosition().lng(),
      }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to delete landing from the database');
      }
      return response.json();
    })
    .then(data => {
      console.log('Landing deleted from database:', data);
    })
    .catch(error => {
      console.error('Error deleting landing from database:', error);
    });

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

  // Add the takeoff's position to the targets array
//  Take.push({ lat: latLng.lat(), lng: latLng.lng() });

  // Add a click listener for the takeoff
  takeoff.addListener("click", () => {
    const infoWindow = new google.maps.InfoWindow({
      content: `${takeoff.getTitle()}<br>Широта: ${latLng.lat()}, Довгота: ${latLng.lng()}`,
    });
    infoWindow.close();
    infoWindow.open(map, takeoff);
  });

  // Add a right-click listener to remove the takeoff
  takeoff.addListener("rightclick", () => {
    takeoff.setMap(null); // Remove the takeoff from the map

    // Remove the corresponding target from the targets array
    const index = targets.findIndex(target => target.lat === latLng.lat() && target.lng === latLng.lng());
    if (index !== -1) {
      targets.splice(index, 1);
    }

    fetch('/map_delete_takeoff', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        latitude: takeoff.getPosition().lat(),
        longitude: takeoff.getPosition().lng(),
      }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to delete takeoff from the database');
      }
      return response.json();
    })
    .then(data => {
      console.log('Takeoff deleted from database:', data);
    })
    .catch(error => {
      console.error('Error deleting takeoff from database:', error);
    });

    });
}

function addMarker(id,latLng) {
  // Create a marker
  const marker = new google.maps.Marker({
    position: latLng,
    map: map,
    draggable: false, // Allow marker to be draggable
    label: `${id}`,
  });

  // Add the marker's position to the targets array
  targets.push({ lat: latLng.lat(), lng: latLng.lng() });

  // Add a click listener for the marker
  marker.addListener("click", () => {
    const infoWindow = new google.maps.InfoWindow({
      content: `Широта: ${latLng.lat()}, Довгота: ${latLng.lng()}`,
    });
    infoWindow.close();
    infoWindow.open(map, marker);
  });

  // Add a right-click listener to remove the marker
  marker.addListener("rightclick", () => {
    marker.setMap(null); // Remove the marker from the map

    // Remove the corresponding target from the targets array
    const index = targets.findIndex(target => target.lat === latLng.lat() && target.lng === latLng.lng());
    if (index !== -1) {
      targets.splice(index, 1);
    }

    fetch('/map_delete_target', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        latitude: marker.getPosition().lat(),
        longitude: marker.getPosition().lng(),
      }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to delete target from the database');
      }
      return response.json();
    })
    .then(data => {
      console.log('Target deleted from database:', data);
    })
    .catch(error => {
      console.error('Error deleting target from database:', error);
    });

    });
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 34.84555, lng: -111.8035 },
  });
  map.addListener("click", (event) => {
    if (addTakeoffMode){
      addTakeoff(event.latLng);

      toggleAddTakeoffMode();

      fetch('/map_add_takeoff', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: event.latLng.lat(),
          longitude: event.latLng.lng(),
        }),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to add takeoff point to the database');
        }
        return response.json();
      })
      .then(data => {
        console.log('Takeoff point added to database:', data);
      })
      .catch(error => {
        console.error('Error adding takeoff point to database:', error);
      });
    } else if (addLandingMode){
      addLanding(event.latLng);

      toggleAddLandingMode();

      fetch('/map_add_landing', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: event.latLng.lat(),
          longitude: event.latLng.lng(),
        }),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to add landing point to the database');
        }
        return response.json();
      })
      .then(data => {
        console.log('Landing point added to database:', data);
      })
      .catch(error => {
        console.error('Error adding landing point to database:', error);
      });
    } else {
      target_id=target_id+1;
      addMarker(target_id,event.latLng);

      fetch('/map_add_target', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: event.latLng.lat(),
          longitude: event.latLng.lng(),
        }),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to add target to the database');
        }
        return response.json();
      })
      .then(data => {
        console.log('Target added to database:', data);
      })
      .catch(error => {
        console.error('Error adding target to database:', error);
      });
    }
  });
}

function fetchAndDisplayMarkers() {
  // Create an empty bounds object
  const bounds = new google.maps.LatLngBounds();



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

  fetch('/map_get_targets')
    .then(response => response.json())
    .then(targets => {
      targets.forEach(target => {
        const latLng = new google.maps.LatLng(target.lat, target.lng);
        addMarker(target.id,latLng); // Add marker using the addMarker function
        target_id=target.id
        bounds.extend(latLng); // Extend bounds to include the marker
      });
      // Fit the map to the bounds
      map.fitBounds(bounds);

    })
    .catch(error => {
      console.error('Error fetching targets:', error);
    });
}

// Call this function to fetch targets and display markers when the page loads
window.onload = fetchAndDisplayMarkers;

window.initMap = initMap;





