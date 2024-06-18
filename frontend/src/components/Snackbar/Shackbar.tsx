import { Alert, Snackbar } from "@mui/material"
import { useSnackbar } from "../../hooks/useSnackbar"


export const AppSnackbar = () => {

    const {openStatus, message, severity, closeInfo} = useSnackbar()

    const handleClose = () => {
        closeInfo()
    }

    return (
        <Snackbar open={openStatus} autoHideDuration={2000} onClose={handleClose}>
            <Alert
                onClose={handleClose}
                severity={severity}
                variant="filled"
                sx={{ width: '100%' }}
            >
                {message}
            </Alert>
        </Snackbar>
    )
}