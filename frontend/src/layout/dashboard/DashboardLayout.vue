<template>
  <div class="wrapper">
    <div class="vld-parent">
      <loading :active.sync="isLoading" :can-cancel="false" :is-full-page="fullPage"></loading>
    </div>
    <side-bar>
      <template slot="links">
        <file-pond
          name="file"
          ref="pond"
          label-idle="Drop Images here..."
          allow-multiple="true"
          accepted-file-types="image/jpeg, image/png"
          v-bind:server="myServer"
          v-bind:files="myFiles"
          v-on:init="handleFilePondInit"
          v-bind:onload="handleFilePondOnload"
          style="margin-right:5%;margin-left:5%;"
        />
        <div class="row">
          <div class="col-md-5">
            <hr
              class="pull-right"
              style="background:#ffffff80;   
   
    height: 1px;
    width: calc(100% - 20px);"
            >
          </div>
          <div class="col-md-2">OR</div>
          <div class="col-md-5">
            <hr
              class="pull-left"
              style="background:#ffffff80;   
    
    height: 1px;
    width: calc(100% - 20px);"
            >
          </div>
        </div>
        <form>
          <br>
          <div class="form-row" style="color:white">
            <div class="form-group col-md-1"></div>
            <div class="form-group col-md-5">
              <label for="Longitude">Longitude</label>
              <input
                type="text"
                style="color:white"
                class="form-control"
                id="Longitude"
                ref="long"
                placeholder="Long"
              >
            </div>
            <div class="form-group col-md-5">
              <label for="Lat">Latitude</label>
              <input
                type="text"
                style="color:white"
                class="form-control"
                id="Latitude"
                ref="lat"
                placeholder="Latitude"
              >
            </div>
            <div class="form-group col-md-1"></div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-1"></div>
            <div class="form-group col-md-5">
              <button type="submit" @click.prevent="updateMap()" class="btn btn-primary">Submit</button>
            </div>
          </div>
        </form>
      </template>
    </side-bar>

    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar"></dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss">
</style>
<script>
import { serverBus } from "../../main";
// Import Vue FilePond
import vueFilePond from "vue-filepond";

// Import FilePond styles
import "filepond/dist/filepond.min.css";

// Import FilePond plugins
// Please note that you need to install these plugins separately

// Import image preview plugin styles
import "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css";

// Import image preview and file type validation plugins
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type";
import FilePondPluginImagePreview from "filepond-plugin-image-preview";

// Create component
const FilePond = vueFilePond(
  FilePondPluginFileValidateType,
  FilePondPluginImagePreview
);
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";
import axios from "axios";
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";
export default {
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
    MobileMenu,
    FilePond,
    Loading
  },
  data: function() {
    return {
      myServer: {
        process: (fieldName, file, metadata, load, error, progress, abort) => {
          // fieldName is the name of the input field
          // file is the actual file object to send
          const formData = new FormData();
          formData.append(fieldName, file, file.name);

          const request = new XMLHttpRequest();
          request.open("POST", "http://127.0.0.1:8000/upload/");

          // Should call the progress method to update the progress to 100% before calling load
          // Setting computable to false switches the loading indicator to infinite mode
          request.upload.onprogress = e => {
            progress(e.lengthComputable, e.loaded, e.total);
          };

          // Should call the load method when done and pass the returned server file id
          // this server file id is then used later on when reverting or restoring a file
          // so your server knows which file to return without exposing that info to the client
          request.onload = function() {
            if (request.status >= 200 && request.status < 300) {
              console.log(request.responseText);
              // the load method accepts either a string (id) or an object
              load(request.responseText);
            } else {
              // Can call the error method if something is wrong, should exit after
              error("oh no");
            }
          };

          request.send(formData);

          // Should expose an abort method so the request can be cancelled
          return {
            abort: () => {
              // This function is entered if the user has tapped the cancel button
              request.abort();

              // Let FilePond know the request has been cancelled
              abort();
            }
          };
        }
      },
      isLoading: false,
      fullPage: true,
      myFiles: [],
      output: null
    };
  },
  methods: {
    getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    updateMap() {
      this.isLoading = true;
      axios({
        method: "get",
        url:
          "http://127.0.0.1:8000/getimage/?latitude=" +
          this.$refs.long.value +
          "&longitude=" +
          this.$refs.lat.value,

        auth: {
          username: "admin",
          password: "password123"
        }
      })
        .then(response => console.log(response.data))
        .catch(error => {})
        .finally(() => ({}));

      this.output = [this.$refs.long.value, this.$refs.lat.value];
      serverBus.$emit("long", this.output);
      this.isLoading = false;
    },

    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
    handleFilePondInit: function() {
      console.log("FilePond has initialized");
    },
    handleFilePondOnload: function(response) {
      console.log(response);

      // FilePond instance methods are available on `this.$refs.pond`
    }
  }
};
</script>
