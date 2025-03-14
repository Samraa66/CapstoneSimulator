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
        <Link to="/train" className="nav-link">Train</Link>
        <Link to="/flight" className="nav-link">Flight</Link>
        <Link to="/simulator"className="nav-link">Simulator</Link>
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

