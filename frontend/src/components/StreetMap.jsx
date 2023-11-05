import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import "leaflet-defaulticon-compatibility";

const StreetMap = ({ data }) => {
  const zoom = 12;

  // [{"id":22,"latitude":37.806915284112684,"longitude":-122.43191185424762,"car_match":{"overall_result":"MISMATCH","make_result":{"match_result":"MISMATCH","field_name":"MAKE","plate_value":"Infiniti","car_value":"Hyundai"},"model_result":{"match_result":"MISMATCH","field_name":"MODEL","plate_value":"JX35","car_value":"Santa Fe"},"year_result":{"match_result":"MATCH","field_name":"YEAR","plate_value":"2013","car_value":"2012-2016"}}}]

  const position = [37.773659225681584, -122.44212155915612];

  // return (
  //   <MapContainer center={[51.505, -0.09]} zoom={zoom}>
  //     {/* Map content goes here */}
  //   </MapContainer>
  // );
  return (
    <MapContainer center={position} zoom={zoom} scrollWheelZoom={false}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {data.map((item, index) => {
        console.log(item);
        return (
          <Marker key={index} position={[item.latitude, item.longitude]}>
            <Popup>
              ID: {item.id} <br />
              Latitude: {item.latitude} <br />
              Longitude: {item.longitude} <br />
              <a href={`/incident/${item.id}`}>Go to Incident</a>
            </Popup>
          </Marker>
        );
      })}
      {/* <Marker position={position}>
        <Popup>
          A pretty CSS3 popup. <br /> Easily customizable.
        </Popup>
      </Marker> */}
    </MapContainer>
  );
};

export default StreetMap;
