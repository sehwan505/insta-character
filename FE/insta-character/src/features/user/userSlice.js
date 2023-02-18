import { createSlice } from '@reduxjs/toolkit'

export const userSlice = createSlice({
  name: 'user',
  initialState: {
    name: "",
  },
  reducers: {
    addName: (state, action) => {
      state.name = action.payload
    },
    remove: (state) => {
      state.name = ""
    }
  },
})

// Action creators are generated for each case reducer function
export const { addName, remove } = userSlice.actions

export default userSlice.reducer