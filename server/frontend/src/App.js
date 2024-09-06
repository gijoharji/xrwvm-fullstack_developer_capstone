import React from "react";
import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";  // Assuming you have a LoginPanel component
import Register from "./components/Register/Register";  // Import the Register component

function App() {
  return (
    <Routes>
      {/* Route for Login */}
      <Route path="/login" element={<LoginPanel />} />

      {/* Route for Register */}
      <Route path="/register" element={<Register />} />

      {/* You can add more routes here, like Home or Dashboard */}
      {/* <Route path="/" element={<Home />} /> */}
    </Routes>
  );
}

export default App;
