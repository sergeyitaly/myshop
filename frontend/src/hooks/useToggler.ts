import { useState } from "react"


export const useToggler = (initialState: boolean = false) => {

    const [openStatus, setOpenStatus] = useState(initialState)

    const handleOpen = () => {
        setOpenStatus(true)
    }

    const handleClose = () => {
        setOpenStatus(false)
    }

    const handleToggle = () => {
        setOpenStatus(!openStatus)
    }

    return {
        openStatus,
        handleOpen,
        handleClose,
        handleToggle,
        setOpenStatus
    }
}