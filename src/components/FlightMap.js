import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// Returns a color based on flight frequency (you can adjust thresholds as needed)
const getColorFromFrequency = (frequency) => {
  if (frequency > 50) return "red";
  if (frequency > 300) return "orange";
  if (frequency > 1000) return "yellow";
  return "blue";
};

// Returns a line weight based on frequency (adjust the divisor to control thickness)
const getLineWeight = (frequency) => {
  // For example, scale frequency down; adjust the divisor as needed
  return Math.max(0.85, frequency / 400);
};

/**
 * Generates a curved line (quadratic Bézier) between two points.
 * @param {number[]} start - [latitude, longitude] of start point
 * @param {number[]} end - [latitude, longitude] of end point
 * @param {number} curvature - How curved the line should be (0 = straight, default: 0.2)
 * @param {number} numPoints - How many points to generate along the curve (default: 50)
 * @returns {Array} Array of [lat, lng] coordinates for the curved line.
 */
const generateCurvedLine = (start, end, curvature = 0.2, numPoints = 50) => {
  const [lat1, lng1] = start;
  const [lat2, lng2] = end;
  
  // Midpoint
  const midLat = (lat1 + lat2) / 2;
  const midLng = (lng1 + lng2) / 2;
  
  // Direction vector from start to end
  const dx = lat2 - lat1;
  const dy = lng2 - lng1;
  
  // Perpendicular vector (for control point offset)
  let perp = [-dy, dx];
  const norm = Math.sqrt(perp[0] * perp[0] + perp[1] * perp[1]);
  if (norm !== 0) {
    perp = [perp[0] / norm, perp[1] / norm];
  }
  
  // Distance between the two points (approximate, works for small distances)
  const dist = Math.sqrt(dx * dx + dy * dy);
  // The offset is proportional to the distance and the curvature factor
  const offset = curvature * dist;
  const controlLat = midLat + perp[0] * offset;
  const controlLng = midLng + perp[1] * offset;
  
  // Generate points along the quadratic Bézier curve
  const points = [];
  for (let i = 0; i <= numPoints; i++) {
    const t = i / numPoints;
    const oneMinusT = 1 - t;
    const lat = oneMinusT * oneMinusT * lat1 
                + 2 * oneMinusT * t * controlLat 
                + t * t * lat2;
    const lng = oneMinusT * oneMinusT * lng1 
                + 2 * oneMinusT * t * controlLng 
                + t * t * lng2;
    points.push([lat, lng]);
  }
  
  return points;
};

const FlightMap = ({ flightDistance }) => {
  const [routeData, setRouteData] = useState([]);

  useEffect(() => {
    const fetchRoutes = async () => {
      if (!flightDistance) return;
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/flights/above/${flightDistance}`
        );
        if (!response.ok) {
          console.error("API Error:", response.status, await response.text());
          return;
        }
        const data = await response.json();
        //console.log("Fetched Data:", data);

        const transformedRoutes = data
          .map((item, index) => {
            const originLat = parseFloat(item.OriginLat);
            const originLong = parseFloat(item.OriginLong);
            const destLat = parseFloat(item.DestLat);
            const destLong = parseFloat(item.DestLong);

            if (
              isNaN(originLat) ||
              isNaN(originLong) ||
              isNaN(destLat) ||
              isNaN(destLong)
            ) {
              console.error(`Invalid coordinates in entry ${index}:`, item);
              return null;
            }
            return {
              path: [
                [originLat, originLong],
                [destLat, destLong],
              ],
              frequency: Number(item.FlightFrequency) || 0,
            };
          })
          .filter(Boolean);

        //console.log("Final Transformed Routes:", transformedRoutes);
        setRouteData(transformedRoutes);
      } catch (error) {
        console.error("Fetch Error:", error);
      }
    };

    fetchRoutes();
  }, [flightDistance]);

  return (
    <MapContainer
      center={[51.1657, 10.4515]}
      zoom={6}
      style={{ height: "800px", width: "100%" }} // Adjust height to fit your panel
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      {routeData.map((route, index) => {
        // Generate a curved polyline for each route
        const curvedLine = generateCurvedLine(route.path[0], route.path[1]);
        const polyKey = `${index}-${route.frequency}`;
        return (
          <Polyline
            key={polyKey}  // Updated key to force re-render when frequency changes
            positions={curvedLine}
            color={getColorFromFrequency(route.frequency)}
            weight={getLineWeight(route.frequency)}
            opacity={0.8}
          />
        );
      })}
    </MapContainer>
  );
};

export default FlightMap;
