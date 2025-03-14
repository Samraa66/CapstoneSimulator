import React, { useEffect, useState } from "react";
import "../styles/EmissionsPanel.css";
import FlightMap from "./FlightMap";
import ReplacedTrainMap from "./ReplacedTrainMap";
import { FaTrain, FaPlane, FaLeaf, FaRedo, FaInfoCircle } from "react-icons/fa";
import Card from "../components/ui/Card"; 
import CardContent from "../components/ui/CardContent";

const EmissionsPanel = () => {
  const [trainDistance, setTrainDistance] = useState(0);
  const [flightDistance, setFlightDistance] = useState(400);
  const [flightEmissions, setFlightEmissions] = useState(0);
  const [trainEmissions, setTrainEmissions] = useState(0);
  const [droppedFlights, setDroppedFlights] = useState([]);

  const calculateEmissions = () => {
    return { trainEmissions, flightEmissions };
  };
  const { trainEmissions: realTrainEmissions, flightEmissions: realFlightEmissions } = calculateEmissions();

  useEffect(() => {
    const fetchFlightEmissions = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/flights/emissions/above/${flightDistance}`);
        if (!response.ok) {
          console.error("API Error:", response.status, await response.text());
          return;
        }
        const data = await response.json();
        setFlightEmissions(data);
      } catch (error) {
        console.error("Error fetching flight emissions:", error);
      }
    };

    fetchFlightEmissions();
  }, [flightDistance]);

  useEffect(() => {
    const fetchTrainEmissions = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/trainEmissions/${flightDistance}`);
        if (!response.ok) {
          console.error("API Error:", response.status, await response.text());
          return;
        }
        const data = await response.json();
        setTrainEmissions(data);
      } catch (error) {
        console.error("Error fetching train emissions:", error);
      }
    };

    fetchTrainEmissions();
  }, [flightDistance]);

  const reset = () => {
    setTrainDistance(0);
    setFlightDistance(400);
    setDroppedFlights([]);
  };

  return (
    <div className="emissions-dashboard">
      <h2 className="dashboard-title">Train vs Flight Emissions Simulator</h2>
      
      {/* Dashboard Statistics Overview */}
      <div className="stats-container">
        <Card className="stats-card">
          <FaTrain className="icon" />
          <CardContent>
            <h3>Train Emissions</h3>
            <p>{realTrainEmissions.toFixed(2)} kg CO₂</p>
          </CardContent>
        </Card>
        <Card className="stats-card">
          <FaPlane className="icon" />
          <CardContent>
            <h3>Flight Emissions</h3>
            <p>{realFlightEmissions.toFixed(2)} kg CO₂</p>
          </CardContent>
        </Card>
        <Card className="stats-card">
          <FaLeaf className="icon" />
          <CardContent>
            <h3>Total Saved CO₂</h3>
            <p>{(realFlightEmissions - realTrainEmissions).toFixed(2)} kg CO₂</p>
          </CardContent>
        </Card>
      </div>
      
      {/* Slider Input */}
      <div className="slider-container">
        <label>Flight Routes Filter (KM)</label>
        <input type="range" min="0" max="1000" step="50" value={flightDistance} onChange={(e) => setFlightDistance(Number(e.target.value))} />
        <span>{flightDistance} KM</span>
      </div>
      <div className="legend-container">
        <h3 className="legend-title"><FaInfoCircle /> Map Legend</h3>
        <div className="legend">
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: "red" }}></span>
            <p>Frequent Flight Routes (Left Map)</p>
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: "blue" }}></span>
            <p>Less Frequent Flight Routes (Left Map)</p>
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: "blue" }}></span>
            <p>Existing Train Routes That Can Handle Passenger Shift (Right Map)</p>
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: "red" }}></span>
            <p>Train Routes Needing Upgrades (Right Map)</p>
          </div>
        </div>
      </div>
      {/* Maps Section */}
      <h2 className="map-title">Flight Routes and Frequencies<tab>----------------------------------------Replaced Train Routes</tab></h2>
      <div className="map-container">
        <div className="map-box">
          <h2 className="map-title">Flight Routes and Frequencies</h2>
          <FlightMap flightDistance={flightDistance} onDroppedFlights={setDroppedFlights} />
        </div>
        <div className="map-box">
          <h3 className="map-title">Replaced Train Routes</h3>
          <ReplacedTrainMap flightDistance={flightDistance} />
        </div>
      </div>

      {/* Legend Section */}
      <div className="legend-container">
        <h3 className="legend-title"><FaInfoCircle /> Map Legend</h3>
        <div className="legend">
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: "red" }}></span>
            <p>Frequent Flight Routes (Left Map)</p>
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: "blue" }}></span>
            <p>Less Frequent Flight Routes (Left Map)</p>
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: "blue" }}></span>
            <p>Existing Train Routes That Can Handle Passenger Shift (Right Map)</p>
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: "red" }}></span>
            <p>Train Routes Needing Upgrades (Right Map)</p>
          </div>
        </div>
      </div>

      {/* Reset Button */}
      <button className="reset-btn" onClick={reset}><FaRedo /> Reset</button>
    </div>
  );
};

export default EmissionsPanel;
