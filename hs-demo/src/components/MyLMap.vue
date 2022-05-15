<template>
  <div id = "map"></div>
</template>

<script>
// 引入 Leaflet
import * as L from 'leaflet'
// 引入 leaflet.markercluster
import 'leaflet.markercluster'
import 'leaflet.chinatmsproviders'
import bjHSPoiJson from '../static//bj_hs_pois.json'

export default {
    data() {
    return {
      map: null,
    }
  },
  mounted() {
      // 创建OMS图层
    //   var omsLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    //   });
      // 创建天地图图层
      var tiandituLayer1 = L.tileLayer.chinaProvider('TianDiTu.Normal.Map');
      var tiandituLayer2 = L.tileLayer.chinaProvider('TianDiTu.Normal.Annotion');

      // 初始化地图基本信息
      this.map = L.map('map', {
          center: [39.90, 116.37],
          zoom: 10,
        //   layers: [omsLayer],
          layers: [tiandituLayer1, tiandituLayer2],
          attributionControl:false,
      });
      

      var geojsonMarkerOptions = {
            radius: 8,
            fillColor: "#ff7800",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8};
      
      // 创建核酸POI点图层
      var hsPOILayer = L.geoJSON(bjHSPoiJson, {
          pointToLayer: (feature, latlng) => {
              return L.circleMarker(latlng, geojsonMarkerOptions);
          },
          onEachFeature: (feature, layer) => {
              let popupText = '<p> 采样点机构： ' + layer.feature.properties.poi_name + '</p>' + '<p> 采样点位置： ' + layer.feature.properties.poi_address; +'</p>';
              layer.bindPopup(popupText);
          }
      });

      // 创建聚散点图层 
      var markersLayer = L.markerClusterGroup();
      markersLayer.addLayer(hsPOILayer);
      this.map.addLayer(markersLayer);

  }
}
</script>

<style>
#map {
    width: 100%;
    height: 95vh;
    /* background: red; */
}
</style>