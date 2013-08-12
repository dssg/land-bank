/**
 * jquery.places-search.js - V0.0.1
 * Created by Richard Willis; 2013 Licensed MIT
 */
var cookSW = new google.maps.LatLng(41.463312, -88.250856);
var cookNE = new google.maps.LatLng(42.155259, -87.465334);
var cookBounds = new google.maps.LatLngBounds(cookSW, cookNE);
(function() {

  function PlacesSearch(element, options) {

    this.element = $(element);
    this.options = $.extend({}, options);
    this.onSelectAddress = this.options.onSelectAddress || $.noop;

    this.autocompleteService = new google.maps.places.AutocompleteService();
    this.placesService = new google.maps.places.PlacesService($('<div />')[0]);

    this.element.typeahead({
      source: $.proxy(this.getPredictions, this),
      updater: $.proxy(this.selectAddress, this)
    });
  };

  PlacesSearch.prototype = {
    constructor: PlacesSearch,
    getPredictions: function(query, process) {
      this.autocompleteService.getPlacePredictions({
	input: query,
	componentRestrictions: {country: 'us'},
	bounds: cookBounds,
	types: ['geocode']
	}, $.proxy(this.onGetPrediction, this, process));
    },
    onGetPrediction: function(process, predictions, status) {
      if (status == google.maps.places.PlacesServiceStatus.OK) {
        this.predictions = predictions;
        process($.map(predictions, function(prediction) {
          return prediction.description;
        }));
      };
    },
    onGetPlaceDetails:  function(result, status) {
      if (status !== google.maps.GeocoderStatus.OK) {
        return window.alert('Location was not found. Please try again.');
      }
      this.options.onSelectAddress(result);
    },
    selectAddress: function(address) {

      // Get the prediction reference.
      var reference = $.grep(this.predictions, function(prediction) {
        return prediction.description === address;
      })[0].reference;

      // Now we can reliably geocode the address.
      this.placesService.getDetails({ reference: reference }, $.proxy(this.onGetPlaceDetails, this));

      return address;
    }
  };

  $.fn.placesSearch = function (options) {
    return this.each(function () {
      new PlacesSearch(this, options);
    });
  };
}());
