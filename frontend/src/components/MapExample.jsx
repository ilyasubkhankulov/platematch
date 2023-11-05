import React from "react";
import rewind from "@turf/rewind";
import buffer from "@turf/buffer";
import difference from "@turf/difference";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import "leaflet-defaulticon-compatibility";

const goodParcel = {
  type: "Feature",
  properties: {},
  geometry: {
    type: "Polygon",
    coordinates: [
      [
        [3.8860702514648438, 51.0070667378415],
        [3.8869044184684753, 51.00721525623504],
        [3.886807858943939, 51.007384026559585],
        [3.8866925239562984, 51.00736546185394],
        [3.8867354393005376, 51.007277701326686],
        [3.886571824550629, 51.00725238575913],
        [3.88653963804245, 51.00732833242038],
        [3.886400163173675, 51.00730976769242],
        [3.88640284538269, 51.007284452142365],
        [3.8863277435302734, 51.007267575101324],
        [3.886300921440124, 51.00730301688043],
        [3.8862499594688416, 51.00729964147408],
        [3.886233866214752, 51.007336770930614],
        [3.886193633079529, 51.007336770930614],
        [3.8861614465713505, 51.00740765435601],
        [3.886072933673858, 51.00739415275953],
        [3.886099755764008, 51.007321581611066],
        [3.885973691940307, 51.00729964147408],
        [3.8860702514648438, 51.0070667378415],
      ],
    ],
  },
};
const rewindParcel = rewind(goodParcel);
console.log(rewindParcel);

const surroundingBufferZone = buffer(goodParcel, 0.5, { units: "meters" });
const firstBufferZone = buffer(goodParcel, 100, { units: "meters" });
const secondBufferZone = buffer(goodParcel, 300, { units: "meters" });
const firstBuffer = difference(firstBufferZone, surroundingBufferZone);
const secondBuffer = difference(secondBufferZone, firstBufferZone);

class MapExample extends React.PureComponent {
  state = {
    lat: 51.0070667378415,
    lng: 3.8860702514648438,
    zoom: 17,
  };

  render() {
    const position = [this.state.lat, this.state.lng];
    return (
      <MapContainer
        center={position}
        zoom={this.state.zoom}
        style={{ height: "70em" }}
      >
        <TileLayer
          attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <GeoJSON
          style={{ color: "gold", opacity: 0, fillOpacity: 1 }}
          key="parcel"
          data={goodParcel}
        />
        <GeoJSON
          style={{ color: "aqua", opacity: 1 }}
          key="firstBuffer"
          data={firstBuffer}
        />

        <GeoJSON
          style={{ color: "blue", opacity: 0 }}
          key="secondBuffer"
          data={secondBuffer}
        />
      </MapContainer>
    );
  }
}

export default MapExample;
