<template>
  <div class="sidebar" :data="backgroundColor">
    <!--
            Tip 1: you can change the color of the sidebar's background using: data-background-color="white | black | darkblue"
            Tip 2: you can change the color of the active button using the data-active-color="primary | info | success | warning | danger"
    -->
    <!-- -->
    <div class="sidebar-wrapper" id="style-3">
      <div class="logo">
        <a href="#" aria-label="sidebar mini logo" class="simple-text logo-mini">
          <div class="logo-img" :class="{'logo-img-rtl': $rtl.isRTL}">
            <img
              src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIoAAACsCAYAAACkcjRPAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBNYWNpbnRvc2giIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NkUxQTg5NjVCRTIwMTFFMkIyMENCRUQzMEQ4RDY4ODQiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6NkUxQTg5NjZCRTIwMTFFMkIyMENCRUQzMEQ4RDY4ODQiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDo2RTFBODk2M0JFMjAxMUUyQjIwQ0JFRDMwRDhENjg4NCIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDo2RTFBODk2NEJFMjAxMUUyQjIwQ0JFRDMwRDhENjg4NCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/Pq4n6C4AAB8eSURBVHja7F0HeFzV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"
              alt
            >
          </div>
        </a>
        <a href="#" class="simple-text logo-normal">DE Forest Watch</a>
      </div>
      <slot></slot>
      <ul class="nav">
        <!--By default vue-router adds an active class to each route link. This way the links are colored when clicked-->
        <slot name="links">
          <sidebar-link
            v-for="(link,index) in sidebarLinks"
            :key="index"
            :to="link.path"
            :name="link.name"
            :icon="link.icon"
          ></sidebar-link>
        </slot>
      </ul>
    </div>
  </div>
</template>
<script>
import SidebarLink from "./SidebarLink";

export default {
  props: {
    title: {
      type: String,
      default: "Creative Tim"
    },
    backgroundColor: {
      type: String,
      default: "vue"
    },
    activeColor: {
      type: String,
      default: "success",
      validator: value => {
        let acceptedValues = [
          "primary",
          "info",
          "success",
          "warning",
          "danger"
        ];
        return acceptedValues.indexOf(value) !== -1;
      }
    },
    sidebarLinks: {
      type: Array,
      default: () => []
    },
    autoClose: {
      type: Boolean,
      default: true
    }
  },
  provide() {
    return {
      autoClose: this.autoClose,
      addLink: this.addLink,
      removeLink: this.removeLink
    };
  },
  components: {
    SidebarLink
  },
  computed: {
    /**
     * Styles to animate the arrow near the current active sidebar link
     * @returns {{transform: string}}
     */
    arrowMovePx() {
      return this.linkHeight * this.activeLinkIndex;
    },
    shortTitle() {
      return this.title
        .split(" ")
        .map(word => word.charAt(0))
        .join("")
        .toUpperCase();
    }
  },
  data() {
    return {
      linkHeight: 65,
      activeLinkIndex: 0,
      windowWidth: 0,
      isWindows: false,
      hasAutoHeight: false,
      links: []
    };
  },
  methods: {
    findActiveLink() {
      this.links.forEach((link, index) => {
        if (link.isActive()) {
          this.activeLinkIndex = index;
        }
      });
    },
    addLink(link) {
      const index = this.$slots.links.indexOf(link.$vnode);
      this.links.splice(index, 0, link);
    },
    removeLink(link) {
      const index = this.links.indexOf(link);
      if (index > -1) {
        this.links.splice(index, 1);
      }
    }
  },
  mounted() {
    this.$watch("$route", this.findActiveLink, {
      immediate: true
    });
  }
};
</script>


<style>
.sidebar-wrapper {
  overflow-x: hidden !important;
}
</style>
