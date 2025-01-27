import React, { useState } from "react";
import "../styles/EmissionsPanel.css";

const EmissionsPanel = () => {
  const [trainDistance, setTrainDistance] = useState(0);
  const [flightDistance, setFlightDistance] = useState(0);

  const calculateEmissions = () => {
    const trainEmissions = trainDistance * 0.029; // Example calculation
    const flightEmissions = flightDistance * 0.214; // Example calculation
    return { trainEmissions, flightEmissions };
  };

  const { trainEmissions, flightEmissions } = calculateEmissions();
  
  const reset = () => {
    setTrainDistance(0);
    setFlightDistance(0);
  }

  return (
    <div className="emissions-panel">
      <h2>Train vs Flight Emissions Simulator</h2>
      <div className="slider-container">
        <label>Train Routes Filter (KM)</label>
        <input
          type="range"
          min="0"
          max="500"
          value={trainDistance}
          onChange={(e) => setTrainDistance(Number(e.target.value))}
        />
        <span>{trainDistance} KM</span>
      </div>
      <div className="slider-container">
        <label>Flight Routes Filter (KM)</label>
        <input
          type="range"
          min="0"
          max="500"
          value={flightDistance}
          onChange={(e) => setFlightDistance(Number(e.target.value))}
        />
        <span>{flightDistance} KM</span>
      </div>
      <button onClick={calculateEmissions}>Calculate Emissions</button>
      <div className="emissions-output">
        <p>Train Emissions: {trainEmissions.toFixed(2)} kg CO₂</p>
        <p>Flight Emissions: {flightEmissions.toFixed(2)} kg CO₂</p>
        <p>Total Saved CO₂: {(flightEmissions - trainEmissions).toFixed(2)} kg CO₂</p>
      </div>
      <button onClick={reset}> Reset</button>
    </div>
  );
};

export default EmissionsPanel;
