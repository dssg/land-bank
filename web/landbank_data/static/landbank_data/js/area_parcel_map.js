var map
  ,pageContext = 'area'
  ,currentPin
  ,newPin
  ,currentParcel=null
  ,currentParcelLatLng
  ,currentAreaBounds
  ,currentMarker;

function returnToParcel() {
  if (currentParcel != null) {
    onGotParcelData(currentParcel);
    // Disable street view if necessary
    closeStreetView();
  }
}

// Callback for map-click listener
function onGotParcelData(parcel) {
  if (updateParcelView(parcel) == false) {
    return;
  }
  if (pageContext=='area') {
    pageContext = 'parcel';
    updateDetailPane();
    updateNav();
  }
  currentParcelLatLng = new google.maps.LatLng(parcel['assessor']['lat_y'],parcel['assessor']['long_x']);
  map.setCenter(currentParcelLatLng);
  if (map.getZoom() <17) { map.setZoom(17); }
  if (currentMarker) { currentMarker.setMap(null); }
  currentMarker = new google.maps.Marker({
    position: currentParcelLatLng
  });
  google.maps.event.addListener(currentMarker, 'click', function() {
    returnToParcel();
  });
  currentMarker.setMap(map);
}

// Switch the left hand navigation between parcel/area views
// as necessary
function updateDetailPane() {
  if (pageContext == 'parcel') {
    $('#area-details').hide();
    $('#parcel-details').show();
  } else {
    $('#parcel-details').hide();
    $('#area-details').show();
  }
}

// Change the navbar links depending on current context
function updateNav() {
  if (pageContext == 'parcel') {
    $('#parcel-title').show();
    $('#area-title').removeClass('active');
    $('#parcel-title').addClass('active');
  } else {
    if (currentParcel == null) {
      $('#parcel-title').hide();
    }
    $('#parcel-title').removeClass('active');
    $('#area-title').addClass('active');
  }
}

// Load new parcel data into the detail pane
function updateParcelView(parcel) {
  if (parcel['status']=='error') { return false; }
  newPin = parcel['parcel_info']['pin']
  currentPin = newPin;
  currentParcel = parcel;

  // Update navbar text and parcel detail pane heading
  var pInfo = parcel['parcel_info'];
  var title = pInfo['address'];
  if (title == null || title == '') {
    title = 'PIN:' + pInfo['pin'];
  }
  //$('#parcel-h3').text(title);
  $('#parcel-title a').text(title);

  // Update table of data in parcel detail pane
  for (var i=0; i<parcelDataFields.length; i++) {
    var thisSection = parcelDataFields[i];
    for (var j=0; j<thisSection.fields.length; j++) {
      // Hide this section until we've seen a defined value for it
      $('table#'+thisSection.id).parent().hide();
      var thisField = thisSection.fields[j];
      var thisFieldVal = pInfo[thisField.id];
      $('td#'+thisField.id+'-td').empty();
      if (thisFieldVal == null || thisFieldVal ==='') {
        // No value? hide this row
        $('tr#'+thisField.id).hide();
      } else {
        if (thisField['link']==true) {
          $('td#'+thisField.id+'-td').append('<a href="' + thisFieldVal + '" target="_blank">' + thisFieldVal + '</a>');
        } else {
          $('td#'+thisField.id+'-td').text(thisFieldVal);
        }
        $('tr#'+thisField.id).show();
        // We have at least one thing shown, so show the parent well
        $('table#'+thisSection.id).parent().show();
      }
    }
  }
  return true;
} 

function refreshArea() {
  pageContext = 'area';
  updateNav();
  updateDetailPane();
  map.setCenter(currentAreaBounds.getCenter());
  map.fitBounds(currentAreaBounds);
  // Disable street view if necessary
  closeStreetView();
}

function refreshParcel() {
  pageContext = 'parcel';
  updateDetailPane();
  updateNav();
  returnToParcel();
}

function closeStreetView() {
  if (map != null) {
    var streetView = map.getStreetView();
    if (streetView.getVisible()) {
      streetView.setVisible(false);
    } else {
      return;
    }
  }
}

function initialize() {
  var mapOptions = {
    zoom: 14,
    center: new google.maps.LatLng(mapCenterLat, mapCenterLng),
    mapTypeControl: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    zoomControlOptions: {
      position: google.maps.ControlPosition.TOP_RIGHT
    },
    panControlOptions: {
      position: google.maps.ControlPosition.TOP_RIGHT
    }
  };
  var bounds = new google.maps.LatLngBounds();
  map = new google.maps.Map(document.getElementById("map-pane"),
      mapOptions);
  // todo: get ALL polygons for areas and add them to map...
  var the_polygon = new google.maps.Polygon({
    clickable: false,
    paths: polygonCoords,
    strokeColor: "#222",
    strokeOpacity: 0.8,
    strokeWeight: 5,
    fillColor: null,
    fillOpacity: 0
  });

    for (i=0; i<polygonCoords.length; i++) {
      bounds.extend(polygonCoords[i]);
    }

    currentAreaBounds = bounds;
    the_polygon.setMap(map);

  var transitLayer = new google.maps.TransitLayer();
  transitLayer.setMap(map); 

  // Composited raster layer of parcel outline and shaded foreclosure
  var base_foreclosure_url = 'http://api.tiles.mapbox.com/v3/salice412.parcel,salice412.parcel_foreclosure.jsonp';
  wax.tilejson(base_foreclosure_url,
    function(tilejson) {
      map.overlayMapTypes.insertAt(0, new wax.g.connector(tilejson));
    });
  map.fitBounds(bounds);

  // Create a listener for map clicks; sends an AJAX call to Django
  // server to request information about a parcel given the clicked
  // latitude/longitude
  // Triggers callback function "onGotParcelData"
  google.maps.event.addDomListener(map, 'click', function(e) {
    Dajaxice.landbank_data.get_property_from_latlng(Dajax.process,
      {'lat':e.latLng.lat()
      ,'lng':e.latLng.lng()
    });
  });

  // ************* Inject base HTML table for parcel details *********** //
  for (var i=0; i<parcelDataFields.length; i++) {
    var thisSection = parcelDataFields[i];
    var $parcelDiv = $('#parcel-details');
    var $well = $('<div class="well well-sm">');
    $parcelDiv.append($well);
    var $heading = $('<h3 id="parcel-h3">' + thisSection.heading + '</h3>');
    $well.append($heading);
    var $table = $('<table class="table" id="' + thisSection.id + '">');
    $well.append($table);
    var $tbody = $('<tbody>');
    $table.append($tbody);
    for (var j=0; j<thisSection.fields.length; j++) {
      var thisField = thisSection.fields[j];
      var $row = $('<tr id="' + thisField.id + '">');
      $tbody.append($row);
      var $header = $('<th id="' + thisField.id + '-th">' + thisField.display + '</th>');
      $row.append($header);
      var $value = $('<td id="' + thisField.id + '-td">');
      $row.append($value);
    }
  } 
}
google.maps.event.addDomListener(window, 'load', initialize);
