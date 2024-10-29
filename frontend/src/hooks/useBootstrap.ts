import { skipToken } from "@reduxjs/toolkit/query"
import { useGetManyProductsByIdListQuery } from "../api/productSlice"
import { useEffect } from "react"
import { STORAGE } from "../constants"
import { BasketItemModel } from "../models/entities"
import { useAppDispatch } from "../store/hooks"
import { setProducts } from "../store/basketSlice"

const getBasketIdList = (): string[] => {
    const localStorageBasket = localStorage.getItem(STORAGE.BASKET)
    const localStorageBasketArray: BasketItemModel[] = localStorageBasket ? JSON.parse(localStorageBasket) : []
    return localStorageBasketArray.map(({productIdName}) => productIdName) 
}


export const useBootstrap = () => {

    const dispatch = useAppDispatch()

    const idList = getBasketIdList()

    const {data, isLoading} = useGetManyProductsByIdListQuery(idList.length ? idList : skipToken)

    useEffect(() => {
        if(data){
            dispatch(setProducts(data))
        }
    }, [data])

    return {
        isLoadingBasket: isLoading,
        basketProducts: data
    }
}