import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  // URL paths for fetching dealers
  const dealer_url = "/djangoapp/get_dealers";
  
  // Function to filter dealers by state
  const filterDealers = async (state) => {
    let url = state === "All" ? dealer_url : `${dealer_url}/${state}`;
    
    const res = await fetch(url, {
      method: "GET"
    });
    
    const retobj = await res.json();
    
    if (retobj.status === 200) {
      let state_dealers = Array.from(retobj.dealers);
      setDealersList(state_dealers);
    }
  };

  // Function to fetch all dealers initially
  const get_dealers = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    
    const retobj = await res.json();
    
    if (retobj.status === 200) {
      let all_dealers = Array.from(retobj.dealers);
      let uniqueStates = [];

      all_dealers.forEach((dealer) => {
        uniqueStates.push(dealer.state);
      });

      setStates(Array.from(new Set(uniqueStates)));  // Set unique states
      setDealersList(all_dealers);  // Set all dealers initially
    }
  };

  // Fetch dealers on component mount
  useEffect(() => {
    get_dealers();
  }, []);  

  // Check if the user is logged in
  const isLoggedIn = sessionStorage.getItem("username") != null;

  return (
    <div>
      <Header/>

      <table className='table'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
                <option value="" selected disabled hidden>State</option>
                <option value="All">All States</option>
                {states.map((state, index) => (
                  <option value={state} key={index}>{state}</option>
                ))}
              </select>        
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
        <tbody>
          {dealersList.map(dealer => (
            <tr key={dealer.id}>
              <td>{dealer.id}</td>
              <td><a href={`/dealer/${dealer.id}`}>{dealer.full_name}</a></td>
              <td>{dealer.city}</td>
              <td>{dealer.address}</td>
              <td>{dealer.zip}</td>
              <td>{dealer.state}</td>
              {isLoggedIn && (
                <td>
                  <a href={`/postreview/${dealer.id}`}>
                    <img src={review_icon} className="review_icon" alt="Post Review"/>
                  </a>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dealers;
