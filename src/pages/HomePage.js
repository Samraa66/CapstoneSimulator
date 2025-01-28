import React from "react";
import FlightMapAnimation from "../components/FlightMapAnimation";

const HomePage = () => {
  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Welcome to the Emissions Simulator</h1>
      <p>Explore and compare train and flight emissions to reduce your carbon footprint.</p>
      <FlightMapAnimation />
      <div>
        <button
          style={{
            margin: "10px",
            padding: "10px 20px",
            backgroundColor: "#007BFF",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
          onClick={() => window.location.href = "/train"}
        >
          Explore Train Emissions
        </button>
        <button
          style={{
            margin: "10px",
            padding: "10px 20px",
            backgroundColor: "#28A745",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
          onClick={() => window.location.href = "/flight"}
        >
          Explore Flight Emissions
        </button>
      </div>
    </div>
  );
};

export default HomePage;
