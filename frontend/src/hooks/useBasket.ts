import { useEffect, useMemo } from "react"
import { STORAGE } from "../constants"
import { BasketItemModel, Product } from "../models/entities"
import { setBasketItems, setOpenStatus, setTotalPrice, resetBasket, setBootstrapIdList, setProducts, addProduct, deleteProduct } from "../store/basketSlice"
import { useAppDispatch, useAppSelector } from "../store/hooks"
import { useSnackbar } from "./useSnackbar"
import { useGetManyProductsByIdListQuery } from "../api/productSlice"
import { skipToken } from "@reduxjs/toolkit/query"

export const useBasket = () => {

  
    const {openStatus, basketItems, totalPrice, bootstrapIdList, products} = useAppSelector(state => state.basket)

    const isEmptyBasket = !basketItems.length 
    const isEmptyBootstrapIdList = !bootstrapIdList.length

    const dispatch = useAppDispatch()

    const {openInfo} = useSnackbar()

    const {data, isLoading} = useGetManyProductsByIdListQuery(!isEmptyBootstrapIdList ? bootstrapIdList : skipToken)

    useEffect(() => {
        if(data){
            dispatch(setProducts(data))
        }
    }, [data])


    const composedItems = useMemo(() => {
        return basketItems.map((basketItem) => {
            const product = products.find(({id}) => id === basketItem.productId)
                return {...basketItem, product: product ? product : null}
        })
    }, [products, basketItems]) 
    

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
            const priceList = products.map(({id, price}) => {
                const matchedBasketItem = basketItems.find(({productId})=> productId === id)
                if(matchedBasketItem){
                    return +price*matchedBasketItem.qty
                }
                return 0
            })
            total = priceList.reduce((sum, current) => sum + current, 0)
        dispatch(setTotalPrice(total))
    }, [data, basketItems, dispatch])

    useEffect(() => {
        dispatch(setBasketItems(getBasketContent()))
    }, [openStatus, dispatch])


    const bootstrap = () => {
        dispatch(setBootstrapIdList())
    }
    

    const openBasket = () => {
        dispatch(setOpenStatus(true))
    }
    
    const closeBasket = () => {
        dispatch(setOpenStatus(false))
    }

    const addToBasket = (product: Product, qty: number) => {
        let contentArray: BasketItemModel[] = getBasketContent()
        dispatch(addProduct(product))

        const newItem: BasketItemModel = {
            productId: product.id,
            qty
        }

        const alreadyInBasket = contentArray.some(({productId}) => productId === product.id)

        if(alreadyInBasket){
            contentArray = contentArray.map((item) => {
                if(item.productId === product.id){
                    return {
                        productId: item.productId,
                        qty: item.qty + qty
                    }
                }
                return item
            })
        } 

        if(!alreadyInBasket){
            contentArray.push(newItem)
        }

        const newBasketContentString = JSON.stringify(contentArray)
        localStorage.setItem(STORAGE.BASKET, newBasketContentString)
        openInfo('Товар додано до кошика');
        dispatch(setBasketItems(contentArray))
    }

    const deleteFromBasket = (product: Product) => {
        const contentArray = getBasketContent().filter(({productId}) => product.id!==productId )
        saveToLocalStorageAndUpdateState(contentArray)
        dispatch(deleteProduct(product))
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

    const changeCounter = (product: Product, counter: number) => {
        const contentArray: BasketItemModel[] = getBasketContent().map(({productId, qty}) => ({
            productId,
            qty: productId===product.id ? counter : qty
        }))
        saveToLocalStorageAndUpdateState(contentArray)
    }

    const setItems = (items: BasketItemModel[]) => {
        dispatch(setBasketItems(items))
    }

    const clearBasket = () => {
        localStorage.removeItem(STORAGE.BASKET)
        dispatch(resetBasket())
        dispatch(setProducts([]))
    }
  


    return {
        basketItems: composedItems, 
        openStatus,
        totalPrice,
        bootstrap,
        openBasket,
        closeBasket,
        addToBasket,
        deleteFromBasket,
        increaceCounter,
        reduceCounter,
        clearBasket,
        setItems,
        changeCounter,
        isLoading,
        productQty: basketItems.length,
        isEmptyBasket
    }
}