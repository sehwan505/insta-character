import { useSelector, useDispatch } from 'react-redux'
import { addName, remove } from './features/user/userSlice'
import { useState } from "react"

function App() {
  const name = useSelector((state) => state.user.name)
  const [inputName, setInputName] = useState("")
  const dispatch = useDispatch()


  const onChange = (e) => {
    setInputName(e.target.value)
  }

  return (
    <div className="App">
      <header className="App-header">
          <h2>{name}</h2>
          <input type="text" value={inputName} onChange={onChange} />
          <button onClick={() => dispatch(addName(inputName))}>add name</button>
      </header>
    </div>
  );
}

export default App;
