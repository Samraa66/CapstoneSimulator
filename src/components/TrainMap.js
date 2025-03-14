import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const getColorFromFrequency = (frequency) => {
  const baseColor = [0, 0, 255]; // RGB for Blue

  // Scale frequency into brightness range (50% to 100% intensity)
  const intensity = Math.min(255, Math.max(100, 255 - frequency / 5));

  return `rgb(${baseColor[0]}, ${baseColor[1]}, ${intensity})`; // Darker/Lighter Blue
};



const getLineWeight = (frequency) => {
  if (frequency > 450) return 30;
  if (frequency > 300) return 20; // Super high-frequency routes (thickest)
  if (frequency > 200) return 10;  // Very busy routes
  if (frequency > 100) return 4;  // Busy routes
  if (frequency > 70) return 3;  // Medium traffic
  if (frequency > 50) return 2.5; // Low traffic
  return 1.5; // Default for lowest frequency
};


const TrainMap = () => {
  const [trainRoutes, setTrainRoutes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrainAlternatives = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/trains");
    
        if (!response.ok) {
          console.error("API Error:", response.status, await response.text());
          return;
        }
    
        const data = await response.json();
        console.log("🚆 Raw API Response:", data);  // 👈 Debug the API response
    
        if (!Array.isArray(data)) {
          console.error("❌ Invalid train data received:", data);
          return;
        }
    
        setTrainRoutes(data);
        setLoading(false);
      } catch (error) {
        console.error("❌ Error fetching train alternatives:", error);
        setLoading(false);
      }
    };
  
    fetchTrainAlternatives();
  }, []);
  
  

  return (
    <div>
      {loading ? (
        <p>Loading train data...</p> // ✅ Show loading indicator
      ) : (
        <MapContainer center={[51.1657, 10.4515]} zoom={6} style={{ height: "800px", width: "100%" }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
          {trainRoutes.length > 0 ? (
  trainRoutes.map((route, index) => {
    console.log(`Rendering Train Route ${index}:`, route.path);
    return (
      <Polyline
        key={index}
        positions={route.path}
        color={getColorFromFrequency(route.frequency)}
        weight={getLineWeight(route.frequency)}
        opacity={0.8}
      />
    );
  })
) : (
  console.log("No train routes to render.")
)}

        </MapContainer>
      )}
    </div>
  );
};

export default TrainMap;
