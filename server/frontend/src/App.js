import React from 'react';
import Dealers from './components/Dealers/Dealers';
import PostReview from './components/Dealers/PostReview'; // Correct path to PostReview
import Dealer from './components/Dealers/Dealer';
import LoginPanel from './components/Login/Login';
import Register from './components/Register/Register'; // Correct path to Register.jsx
import { Routes, Route } from 'react-router-dom';

function App() {
    return (
      <Routes>
        {/* Route for Login */}
        <Route path="/login" element={<LoginPanel />} />
  
        {/* Route for Register */}
        <Route path="/register" element={<Register />} />
  
        {/* Route for Dealers */}
        <Route path="/dealers" element={<Dealers />} />
  
        {/* Route for a specific dealer with id */}
        <Route path="/dealer/:id" element={<Dealer />} />
        
        {/* Route for posting a review for a specific dealer */}
        <Route path="/postreview/:id" element={<PostReview />} /> {/* New route for posting reviews */}
  
        {/* You can add more routes here */}
      </Routes>
    );
}


export default App;
