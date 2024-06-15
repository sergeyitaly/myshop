import { PayloadAction, createSlice } from "@reduxjs/toolkit";

const initialState = {
    openStatus: false
}

export const basketSlice = createSlice({
    name: 'basket',
    initialState,
    reducers: {
        setOpenStatus: (state, action: PayloadAction<boolean>) => {
            state.openStatus = action.payload
        },
    }
})

export const {
    setOpenStatus
} = basketSlice.actions