import React, { useState } from "react";
import "./styles.css";
import axios from 'axios';

const App = () => {
  const [loading, setLoading] = useState(false);
  const [instagramId, setInstagramId] = useState("");
  const [mbtiType, setMbtiType] = useState("");
  const [mbtiDescription, setMbtiDescription] = useState([]);

  const handleInputChange = (event) => {
    setInstagramId(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchMbtiData();
    console.log(loading);
  };

  const fetchMbtiData = async () => {
    fetch(`https://k-army-project-irpqk.run.goorm.site/insta/${instagramId}`);
    
    axios.get(`https://k-army-project-irpqk.run.goorm.site/user/classification_by_media/${instagramId}`)
    .then(function (response) {
      setLoading(true);
      const data = response.data;
      const mbti = data.response;

      axios.get(`https://k-army-project-irpqk.run.goorm.site/user/generate_characteristic_description/${mbti}`)
        .then(function (response) {
          setMbtiType(mbti);
          setMbtiDescription(response.data.response);
          console.log(response.data.response);
          console.log(loading);
          setLoading(false);
        })
        .catch(function (error) {
          setLoading(false);
          console.error(error);
        });
    })
    .catch(function (error) {
      setLoading(false);
      console.error(error);
    });
  };

  return (
    <div className="container">
      {mbtiType ? (
        <div className="mbti-container">
          <h1 style={{"fontWeight":700, "fontSize": 30}}>{mbtiType}</h1>
            {mbtiDescription.map((description, index) => (
              <div key={index} className="hashtag-box">#{description}</div>
            ))}
          <button type="button" onClick={() => {setMbtiType("");}}>Retry</button>
        </div>
      ) : (
        <div className="form-container">
        <form onSubmit={handleSubmit}>
          <label htmlFor="instagramId">Instagram ID:</label>
          <input
            type="text"
            id="instagramId"
            value={instagramId}
            onChange={handleInputChange}
          />
          <button type="submit">{loading ? <>Loading..</> : <>Submit</>}</button>
        </form>
      </div>
      )}
    </div>
  );
};

export default App;