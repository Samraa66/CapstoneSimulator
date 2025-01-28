import React from "react";
import Lottie from "lottie-react";
import flightMapData from "../assets/flight-map-animation.json"; // Renamed JSON import

const FlightMapAnimation = () => {
  return (
    <div style={{ width: "100%", height: "400px", display: "flex", justifyContent: "center" }}>
      <Lottie animationData={flightMapData} style={{ width: "100%", height: "100%" }} />
    </div>
  );
};

export default FlightMapAnimation;
