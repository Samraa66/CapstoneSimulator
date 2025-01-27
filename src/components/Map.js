import React from "react";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const Map = () => {
  // Dummy route connecting cities (latitude, longitude)
  const dummyRoute = [
    [51.1657, 10.4515], // Germany
    [48.8566, 2.3522],  // Paris
    [52.5200, 13.4050], // Berlin
  ];

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
        <Polyline positions={dummyRoute} color="blue" weight={3} />
      </MapContainer>
    </div>
  );
};

export default Map;
