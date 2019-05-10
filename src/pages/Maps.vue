<template>
  <card type="plain" title="Google Maps">
    <div id="map" class="map"></div>
  </card>
</template>
<script>
import { serverBus } from "../main";
export default {
  data() {
    return {
      long: null,
      lat: null,
      myLatlng: null
    };
  },
  created() {},
  mounted() {
    this.myLatlng = new window.google.maps.LatLng(40.748817, -73.985428);

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
    marker.setMap(map);

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
    });
  }
};
</script>
<style>
</style>
