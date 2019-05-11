<template>
  <card type="plain" title="Google Maps">
    <div id="map" class="map"></div>
  </card>
</template>
<script>
import { serverBus } from "../main";
import Papa from "papaparse";
import axios from "axios";
export default {
  data() {
    return {
      myconfig: {
        delimiter: "", // auto-detect
        newline: "", // auto-detect
        quoteChar: '"',
        escapeChar: '"',
        header: true,
        transformHeader: true,
        dynamicTyping: false,
        preview: 0,
        encoding: "",
        worker: false,
        comments: false,
        step: undefined,
        complete: undefined,
        error: undefined,
        downloadRequestHeaders: undefined,
        skipEmptyLines: false,
        chunk: undefined,
        fastMode: undefined,
        beforeFirstChunk: undefined,
        withCredentials: undefined,
        transform: undefined,
        delimitersToGuess: [",", "\t", "|", ";", Papa.RECORD_SEP, Papa.UNIT_SEP]
      },
      long: null,
      lat: null,
      myLatlng: null
    };
  },
  created() {},
  mounted() {
    this.myLatlng = new window.google.maps.LatLng(9.0765, 7.3986);

    let mapOptions = {
      zoom: 13,
      center: this.myLatlng,
      scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
      mapTypeId: "satellite"
    };
    let map = new window.google.maps.Map(
      document.getElementById("map"),
      mapOptions
    );

    let marker = new window.google.maps.Marker({
      position: this.myLatlng,
      title: "Hello World!"
    });

    // To add the marker to the map, call setMap();
    // marker.setMap(map);

    // Using the server bus
    serverBus.$on("long", function(payLoad) {
      this.long = payLoad[0];
      this.lat = payLoad[1];

      let myLatlng = new google.maps.LatLng(this.lat, this.long);
      map.setCenter(myLatlng);
      let marker = new window.google.maps.Marker({
        position: myLatlng,
        title: "Location"
      });

      let geocoder = new google.maps.Geocoder();
      geocoder.geocode({ location: myLatlng }, (results, status) => {
        if (status === google.maps.GeocoderStatus.OK) {
          let addres = {};
          let longName = {};
          const address_components = results[0].address_components;
          address_components.forEach(element => {
            addres[element.types[0]] = element.short_name;
            longName[element.types[0]] = element.long_name;
          });

          const address = {
            formatted_address: results[0].formatted_address,
            address_parts: addres
          };

          serverBus.$emit("country_code", [
            address.address_parts.country,
            longName.country
          ]);
        }
      });
    });
  }
};
</script>
<style>
</style>
