<template>
  <div class="wrapper">
    <side-bar>
      <template slot="links">
        <file-pond
          name="test"
          ref="pond"
          label-idle="Drop Images here..."
          allow-multiple="true"
          accepted-file-types="image/jpeg, image/png"
          server="/api"
          v-bind:files="myFiles"
          v-on:init="handleFilePondInit"
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
export default {
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
    MobileMenu,
    FilePond
  },
  data: function() {
    return { myFiles: [], output: null };
  },
  methods: {
    updateMap() {
      axios({
        method: "post",
        url: "http://127.0.0.1:8000/test/",
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
    },

    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
    handleFilePondInit: function() {
      console.log("FilePond has initialized");

      // FilePond instance methods are available on `this.$refs.pond`
    }
  }
};
</script>
