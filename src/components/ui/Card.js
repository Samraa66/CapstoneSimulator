import React from "react";

const Card = ({ children }) => {
  return (
    <div style={{
      background: "white",
      padding: "15px",
      borderRadius: "8px",
      boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)",
      textAlign: "center"
    }}>
      {children}
    </div>
  );
};

export default Card;
