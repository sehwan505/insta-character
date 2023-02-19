import { createSlice } from '@reduxjs/toolkit'

export const userSlice = createSlice({
  name: 'user',
  initialState: {
    name: "",
    instagramId: ""
  },
  reducers: {
    addName: (state, action) => {
      state.name = action.payload
    },
    setInstagramId: (state, action) => {
      state.instagramId = action.payload
    },
    remove: (state) => {
      state.name = ""
      state.instagramId = ""
    }
  },
})

// Action creators are generated for each case reducer function
export const { addName, setInstagramId, remove } = userSlice.actions

export default userSlice.reducer