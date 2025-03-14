import React from "react";
import FlightMap from "../components/FlightMap";
import EmissionsPanel from "../components/EmissionsPanel";

const Simulator = () => {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ flex: 1, overflow: "auto" }}> {/* EmissionsPanel */}
        <EmissionsPanel />
      </div>
    </div>
  );
};

export default Simulator;
