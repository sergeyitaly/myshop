import { AlertColor} from "@mui/material";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface SnackbarInitialModel {
    openStatus: boolean
    severity?: AlertColor
    message: string
}

interface OpenPayload {
    severity?: AlertColor
    message: string
}

const initialState: SnackbarInitialModel = {
    openStatus: false,
    severity: 'info',
    message: ''
}

export const snackbarSlice = createSlice({
    name: 'snackbar',
    initialState,
    reducers: {
        openSnackbar: (state, action: PayloadAction<OpenPayload>) => {
            state.openStatus = true
            state.message = action.payload.message
            state.severity = action.payload.severity  
        },
      
        closeSnackbar: (state) => {
            state.openStatus = false
        },
    }
})

export const {
    openSnackbar,
    closeSnackbar
} = snackbarSlice.actions