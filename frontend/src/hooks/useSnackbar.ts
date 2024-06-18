import { AlertColor } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../store/hooks"
import { closeSnackbar, openSnackbar } from "../store/snackbarSlice"


export const useSnackbar = () => {

    const {message, openStatus, severity} = useAppSelector(state => state.snackbar)

    const dispatch = useAppDispatch()

    const openInfo = (message: string, severity?: AlertColor) => {
        dispatch(openSnackbar({message, severity}))
    }

    const closeInfo = () => {
        dispatch(closeSnackbar())
    }

    return {
        message,
        openStatus,
        severity,
        openInfo,
        closeInfo
    }
}