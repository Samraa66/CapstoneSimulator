import React, { useState } from "react";
import TrainMap from "../components/TrainMap";

const TrainPage = () => {
  const [showMap, setShowMap] = useState(true);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Train Emissions</h1>
      <p>Explore train routes and their emissions impact.</p>
      <button onClick={() => setShowMap(!showMap)}>
        {showMap ? "Hide Map" : "Show Map"}
      </button>
      {showMap && <TrainMap />}  {/* ✅ Ensures map renders only once */}
    </div>
  );
};

export default TrainPage;
