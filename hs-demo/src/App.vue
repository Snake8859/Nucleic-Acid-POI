<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App" /> -->
    <MapHeader/>
    <MyLMapVue/>
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
import 'leaflet/dist/leaflet.css' // Leaflet样式引入
import 'leaflet.markercluster/dist/MarkerCluster.css' // markercluster样式引入
import 'leaflet.markercluster/dist/MarkerCluster.Default.css' // markercluster样式引入
import MyLMapVue from './components/MyLMap.vue';
import MapHeader from './components/MapHeader.vue';

export default {
  name: "App",
  components: {
    // HelloWorld,
    MyLMapVue,
    MapHeader,
  },
};
</script>

<style lang="less">
// #app {
//   font-family: Avenir, Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   text-align: center;
//   color: #2c3e50;
//   margin-top: 60px;
// }
body{
  margin: 2px;
}
</style>
