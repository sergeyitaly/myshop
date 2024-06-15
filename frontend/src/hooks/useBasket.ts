import { setOpenStatus } from "../store/basketSlice"
import { useAppDispatch, useAppSelector } from "../store/hooks"


export const useBasket = () => {

    const {openStatus} = useAppSelector(state => state.basket)
    const dispatch = useAppDispatch()

    const openBasket = () => {
        dispatch(setOpenStatus(true))
    }
    
    const closeBasket = () => {
        dispatch(setOpenStatus(false))
    }

    return {
        openStatus,
        openBasket,
        closeBasket
    }
}