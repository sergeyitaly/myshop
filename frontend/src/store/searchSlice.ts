import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface SearchSlice {
    open: boolean,
    value: string,
}

const initialState: SearchSlice = {
    open: false,
    value: ''
}

export const searchSlice = createSlice({
    name: 'search',
    initialState,
    reducers: {
        setOpenState: (state, action: PayloadAction<boolean>) => {
            state.open = action.payload
        },

        setValue: (state, action: PayloadAction<string>) => {
            state.value = action.payload
        }
    }
})

export const {
    setOpenState,
    setValue
} = searchSlice.actions