import { useSelector, useDispatch } from 'react-redux'
import { addName, remove } from './features/user/userSlice'
import React, { useState } from "react";
import "./styles.css";
import axios from 'axios';

const App = () => {
  const [instagramId, setInstagramId] = useState("");
  const [mbtiType, setMbtiType] = useState("");
  const [mbtiDescription, setMbtiDescription] = useState([]);

  const handleInputChange = (event) => {
    setInstagramId(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchMbtiData();
  };

  const fetchMbtiData = async () => {
    fetch(`https://k-army-project-irpqk.run.goorm.site/insta/${instagramId}`);
    
    axios.get(`https://k-army-project-irpqk.run.goorm.site/user/classification_by_media/${instagramId}`)
    .then(function (response) {
      const data = response.data;
      const mbti = data.response;
      setMbtiType(mbti);

      axios.get(`https://k-army-project-irpqk.run.goorm.site/user/generate_characteristic_description/${mbti}`)
        .then(function (response) {
          setMbtiDescription(response.data.response);
          console.log(response.data.response);
        })
        .catch(function (error) {
          console.error(error);
        });
    })
    .catch(function (error) {
      console.error(error);
    });
  };

  return (
    <div className="container">
      {mbtiType ? (
        <div className="mbti-container">
          <h2>{mbtiType}</h2>
          <ul>
            {mbtiDescription.map((description, index) => (
              <li key={index}>{description}</li>
            ))}
          </ul>
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
          <button type="submit">Submit</button>
        </form>
      </div>
      )}
    </div>
  );
};

export default App;