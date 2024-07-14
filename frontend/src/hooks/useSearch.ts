import { ChangeEvent, useEffect } from "react"
import { useAppDispatch, useAppSelector } from "../store/hooks"
import { setOpenState, setValue } from "../store/searchSlice"

export const useSearch = () => {

    const {open, value} = useAppSelector(state => state.searchBar)
    const dispatch = useAppDispatch()

    useEffect(() => {
        dispatch(setValue(''))
    }, [open, dispatch])

    const openSearchBar = () => {
        dispatch(setOpenState(true))
    }
   
    const closeSearchBar = () => {
        dispatch(setOpenState(false))
    }

    const toggleSearchBar = () => {
        dispatch(setOpenState(!open))
    }

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        dispatch(setValue(event.target.value))
    }

    return {
        open,
        value,
        openSearchBar,
        closeSearchBar,
        toggleSearchBar,
        handleChange
    }
}