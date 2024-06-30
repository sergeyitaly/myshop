import { useEffect, useMemo } from "react"
import { STORAGE } from "../constants"
import { BasketItemModel, Product } from "../models/entities"
import { setBasketItems, setOpenStatus, setTotalPrice } from "../store/basketSlice"
import { useAppDispatch, useAppSelector } from "../store/hooks"
import { useSnackbar } from "./useSnackbar"
import { useGetManyProductsByIdListQuery } from "../api/productSlice"

export const useBasket = () => {

  
    const {openStatus, basketItems, totalPrice} = useAppSelector(state => state.basket)
    const dispatch = useAppDispatch()

    const {openInfo} = useSnackbar()

    const idList = useMemo(() => {
        return basketItems.map(({productId}) => productId )
    }, [basketItems])

    const {data} = useGetManyProductsByIdListQuery(idList)

    
    

    const getBasketContent = (): BasketItemModel[] => {
        const itemsString = localStorage.getItem(STORAGE.BASKET)
        return itemsString ? JSON.parse(itemsString) : []
    }

    const saveToLocalStorageAndUpdateState = (content: BasketItemModel[]) => {
        const serializedContent = JSON.stringify(content)
        localStorage.setItem(STORAGE.BASKET, serializedContent)
        dispatch(setBasketItems(content))
    }

    useEffect(() => {
        let total = 0
        if(data){
            const priceList = data.map(({id, price}) => {
                const matchedBasketItem = basketItems.find(({productId})=> productId === id)
                if(matchedBasketItem){
                    return +price*matchedBasketItem.qty
                }
                return 0
            })
            total = priceList.reduce((sum, current) => sum + current, 0)
        }
        dispatch(setTotalPrice(total))
    }, [data, basketItems, dispatch])

    useEffect(() => {
        dispatch(setBasketItems(getBasketContent()))
    }, [openStatus, dispatch])

    const openBasket = () => {
        dispatch(setOpenStatus(true))
    }
    
    const closeBasket = () => {
        dispatch(setOpenStatus(false))
    }

    const addToBasket = (product: Product, qty: number) => {
        const contentArray: BasketItemModel[] = getBasketContent()

        const newItem: BasketItemModel = {
            productId: product.id,
            qty
        }

        const alreadyInBasket = contentArray.some(({productId}) => productId === product.id)
        if(alreadyInBasket){
            return openInfo('Цей товар вже у кошику', 'info')
        } 

        contentArray.push(newItem)
        const newBasketContentString = JSON.stringify(contentArray)
        localStorage.setItem(STORAGE.BASKET, newBasketContentString)
        openInfo('Товар додано до кошика');
        dispatch(setBasketItems(contentArray))
    }

    const deleteFromBasket = (product: Product) => {
        const contentArray = getBasketContent().filter(({productId}) => product.id!==productId )
        saveToLocalStorageAndUpdateState(contentArray)
    }

    const increaceCounter = (product: Product) => {
        const contentArray: BasketItemModel[] = getBasketContent().map(({productId, qty}) => ({
            productId,
            qty: productId===product.id ? qty+1 : qty
        }))
        saveToLocalStorageAndUpdateState(contentArray)
    }
    
    const reduceCounter = (product: Product) => {
        const contentArray: BasketItemModel[] = getBasketContent().map(({productId, qty}) => ({
            productId,
            qty: productId===product.id && qty >1 ? qty-1 : qty
        }))
        saveToLocalStorageAndUpdateState(contentArray)
    }

    return {
        basketItems,
        openStatus,
        totalPrice,
        openBasket,
        closeBasket,
        addToBasket,
        deleteFromBasket,
        increaceCounter,
        reduceCounter,
        productQty: basketItems.length,
        isEmptyBasket: !basketItems.length
    }
}