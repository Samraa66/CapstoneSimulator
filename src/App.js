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
      <nav style={{ padding: "10px", backgroundColor: "#f0f0f0" }}>
        <Link to="/" style={{ marginRight: "10px" }}>Home</Link>
        <Link to="/train" style={{ marginRight: "10px" }}>Train</Link>
        <Link to="/flight" style={{ marginRight: "10px" }}>Flight</Link>
        <Link to="/simulator">Simulator</Link>
      </nav>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/train" element={<TrainPage />} />
        <Route path="/flight" element={<FlightPage />} />
        <Route path="/simulator" element={<Simulator />} />
      </Routes>
    </Router>
  );
}

export default App;

