import React, { useState } from "react";
import "../styles/EmissionsPanel.css";

const EmissionsPanel = ({ mode }) => {
  const [distance, setDistance] = useState(100);
  const CO2_PER_KM_TRAIN = 29; // CO2 g per passenger-km for trains
  const CO2_PER_KM_FLIGHT = 214; // CO2 g per passenger-km for flights

  const trainEmissions = (distance * CO2_PER_KM_TRAIN) / 1000; // Convert to kg
  const flightEmissions = (distance * CO2_PER_KM_FLIGHT) / 1000;
  const savedCO2 = flightEmissions - trainEmissions;

  return (
    <div className="emissions-panel">
      {mode === "train" && (
        <div>
          <h3>Eco-Friendly Train Travel</h3>
          <p>Trains are one of the most sustainable modes of transport!</p>
          <label>Distance (KM): {distance} KM</label>
          <input
            type="range"
            min="50"
            max="1000"
            value={distance}
            onChange={(e) => setDistance(e.target.value)}
          />
          <p>CO₂ Emissions by Train: {trainEmissions.toFixed(2)} kg</p>
          <p>Equivalent Car Emissions: {(trainEmissions * 2.4).toFixed(2)} kg</p>
          <p className="fun-fact">🚆 Did you know? High-speed trains run on 60% renewable energy!</p>
        </div>
      )}

      {mode === "flight" && (
        <div>
          <h3>Flight Environmental Impact</h3>
          <p>Air travel is fast, but has a higher CO₂ footprint.</p>
          <label>Distance (KM): {distance} KM</label>
          <input
            type="range"
            min="50"
            max="1000"
            value={distance}
            onChange={(e) => setDistance(e.target.value)}
          />
          <p>CO₂ Emissions by Flight: {flightEmissions.toFixed(2)} kg</p>
          <p>Trees Needed to Offset: {(flightEmissions / 20).toFixed(0)} 🌳</p>
          <p className="fun-fact">✈️ Did you know? Contrails contribute to global warming more than CO₂ itself!</p>
        </div>
      )}

      {mode === "compare" && (
        <div>
          <h3>Train vs. Flight Emissions Comparison</h3>
          <p>Compare the environmental impact of train vs. air travel.</p>
          <label>Distance (KM): {distance} KM</label>
          <input
            type="range"
            min="50"
            max="1000"
            value={distance}
            onChange={(e) => setDistance(e.target.value)}
          />
          <p>Train Emissions: {trainEmissions.toFixed(2)} kg CO₂</p>
          <p>Flight Emissions: {flightEmissions.toFixed(2)} kg CO₂</p>
          <p>Total CO₂ Saved by Train: {savedCO2.toFixed(2)} kg</p>
          <p className="fun-fact">🌍 If 10% of flights switched to trains, we’d cut CO₂ by millions of tons yearly!</p>
        </div>
      )}
    </div>
  );
};

export default EmissionsPanel;

import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import TrainPage from "./pages/TrainPage";
import FlightPage from "./pages/FlightPage";
import Simulator from "./pages/Simulator";

// router and routes are a library to help with navigation btw pages 
// <nav is an html tag for navigation . it is used to oprganize the links
function App() {
  return (
    <Router>
      <nav style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        gap: "20px",
        padding: "15px",
        backgroundColor: "#f8f9fa",
        boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        position: "fixed",
        top: 0,
        width: "100%",
        zIndex: 1000,
      }}>
        <Link to="/" className="nav-link">Home</Link>
        {/*<Link to="/train" className="nav-link">Train</Link> */}
        {/<Link to="/flight" className="nav-link">Flight</Link>/}
        <Link to="/simulator" className="nav-link">Simulator</Link>
      </nav>

      

      <div style={{ marginTop: "60px" }}> {/* Adds space so content doesn't go under nav */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/train" element={<TrainPage />} />
          <Route path="/flight" element={<FlightPage />} />
          <Route path="/simulator" element={<Simulator />} />
        </Routes>
      </div>
    </Router>
  );
}


export default App;