import { useSelector, useDispatch } from 'react-redux'
import { addName, remove } from './features/user/userSlice'
import React, { useState } from "react";
import "./styles.css";

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
    try {
      fetch(`https://k-army-project-irpqk.run.goorm.site/insta/${instagramId}`);
      const res2 = fetch(`https://k-army-project-irpqk.run.goorm.site/user/classification_by_media/${instagramId}`);
      const data2 = res2.json();
      setMbtiType(data2.mbtiType);
      const res3 = fetch(`https://k-army-project-irpqk.run.goorm.site/user/generate_characteristic_description/${data2.mbtiType}`);
      const data3 = res3.json();
      setMbtiDescription(data3.mbtiDescription);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
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
      {mbtiType && (
        <div className="mbti-container">
          <h2>{mbtiType}</h2>
          <ul>
            {mbtiDescription.map((description, index) => (
              <li key={index}>{description}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default App;