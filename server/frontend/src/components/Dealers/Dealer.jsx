import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [loadingDealer, setLoadingDealer] = useState(true);  // Add loading state for dealer
  const [loadingReviews, setLoadingReviews] = useState(true); // Add loading state for reviews
  const [postReview, setPostReview] = useState(<></>);
  const [error, setError] = useState(""); // To handle errors
  
  let { id } = useParams();  // Extract dealer id from params
  let curr_url = window.location.href;
  let root_url = curr_url.substring(0, curr_url.indexOf("dealer"));
  let dealer_url = root_url + `djangoapp/dealer/${id}`;
  let reviews_url = root_url + `djangoapp/get_reviews/${id}`;
  let post_review_url = root_url + `postreview/${id}`;

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200 && retobj.dealer) {
        setDealer(retobj.dealer);
      } else {
        setError("Dealer not found");
      }
    } catch (error) {
      setError("Error fetching dealer data");
      console.error("Error fetching dealer data: ", error);
    } finally {
      setLoadingDealer(false); // Set loading state to false once data is fetched
    }
  };

  const get_reviews = async () => {
    try {
      const res = await fetch(reviews_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200 && Array.isArray(retobj.reviews)) {
        setReviews(retobj.reviews);
      } else {
        setError("No reviews found");
      }
    } catch (error) {
      setError("Error fetching reviews");
      console.error("Error fetching reviews: ", error);
    } finally {
      setLoadingReviews(false); // Set loading state to false once data is fetched
    }
  };

  const senti_icon = (sentiment) => {
    return sentiment === "positive" ? positive_icon : sentiment === "negative" ? negative_icon : neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review_url}>
          <img src={review_icon} style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }} alt='Post Review' />
        </a>
      );
    }
  }, [id]);  // Include 'id' in the dependency array

  if (error) return <div style={{ color: "red" }}>{error}</div>;

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        {loadingDealer ? (
          <h1 style={{ color: "grey" }}>Loading Dealer Information...</h1>
        ) : (
          <>
            <h1 style={{ color: "grey" }}>{dealer.full_name}{postReview}</h1>
            <h4 style={{ color: "grey" }}>
              {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
            </h4>
          </>
        )}
      </div>
      <div className="reviews_panel">
        {loadingReviews ? (
          <text>Loading Reviews....</text>
        ) : reviews.length === 0 ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map((review) => (
            <div className='review_panel' key={review.id}>
              <img src={senti_icon(review.sentiment)} className="emotion_icon" alt='Sentiment' />
              <div className='review'>{review.review}</div>
              <div className="reviewer">{review.name} {review.car_make} {review.car_model} {review.car_year}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;
