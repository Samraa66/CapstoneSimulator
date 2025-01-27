import React from "react";
import Map from "../components/Map";
import EmissionsPanel from "../components/EmissionsPanel";

const Simulator = () => {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ flex: 2 }}> {/* Map gets more space */}
        <Map />
      </div>
      <div style={{ flex: 1, overflow: "auto" }}> {/* EmissionsPanel */}
        <EmissionsPanel />
      </div>
    </div>
  );
};

export default Simulator;
