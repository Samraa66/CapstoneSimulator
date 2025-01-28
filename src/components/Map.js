import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const Map = () => {
  const [route, setRoute] = useState([]);
  // Dummy route connecting cities (latitude, longitude)
  const dummyRoute = [
    [51.1657, 10.4515], // Germany
    [48.8566, 2.3522],  // Paris
    [52.5200, 13.4050], // Berlin
  ];
  useEffect(() => {
    const fetchRoute = async () => {
      const response = await fetch('http://127.0.0.1:8000/api/trains');
      const data = await response.json();
      console.log("Data is : ", data);
      const transformedRoutes = data.map((item) => [
        [item.OriginLat, item.OriginLon],
        [item.DestLat, item.DestLon],
      ]);
      setRoute(transformedRoutes);
    };
    fetchRoute();
  }, []);

  return (
    <div style={{ flex: 1, height: "100%" }}>
      <MapContainer
        center={[51.1657, 10.4515]} // Example: Germany's coordinates
        zoom={6}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {/* Add the Polyline */}
        {route.length > 0 &&
        route.map((line, index) => (
          <Polyline key={index} positions={line} color="blue" weight={3} />
        ))}
      </MapContainer>
    </div>
  );
};

export default Map;
