import { ChangeEvent, useEffect } from "react"
import { useAppDispatch, useAppSelector } from "../store/hooks"
import { setOpenState, setValue } from "../store/searchSlice"
import { useDebounce } from 'use-debounce'

export const useSearch = () => {

    const {open, value} = useAppSelector(state => state.searchBar)
    const dispatch = useAppDispatch()
    const [debounceValue] = useDebounce(value, 300)
    

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
        debounceValue,
        openSearchBar,
        closeSearchBar,
        toggleSearchBar,
        handleChange
    }
}