import { useEffect, useMemo } from "react"
import { STORAGE } from "../constants"
import { BasketItemModel, Product } from "../models/entities"
import { setBasketItems, setOpenStatus, setTotalPrice, resetBasket, setProducts, addProduct, deleteProduct } from "../store/basketSlice"
import { useAppDispatch, useAppSelector } from "../store/hooks"
import { useSnackbar } from "./useSnackbar"
import { useAppTranslator } from "./useAppTranslator"
import { countDiscountPrice } from "../functions/countDiscountPrice"

export const useBasket = () => {

    const {openStatus, basketItems, totalPrice, products} = useAppSelector(state => state.basket)

    const {t} = useAppTranslator()

    const isEmptyBasket = !basketItems.length 

    const dispatch = useAppDispatch()

    const {openInfo} = useSnackbar()


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
            const priceList = products.map(({id, price, discount}) => {
                const matchedBasketItem = basketItems.find(({productId})=> productId === id)
                console.log(+discount);
                const disc = countDiscountPrice(price, discount)
                if(matchedBasketItem){
                    return disc ? disc*matchedBasketItem.qty : +price*matchedBasketItem.qty
                }
                return 0 
            })
            total = priceList.reduce((sum, current) => sum + current, 0)
            console.log(priceList);
            
        dispatch(setTotalPrice(total))
    }, [products, basketItems, dispatch])

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
        let contentArray: BasketItemModel[] = getBasketContent()
        dispatch(addProduct(product))

        const newItem: BasketItemModel = {
            productId: product.id,
            productIdName: product.id_name,
            qty
        }

        const alreadyInBasket = contentArray.some(({productId}) => productId === product.id)

        if(alreadyInBasket){
            contentArray = contentArray.map((item) => {
                if(item.productId === product.id){
                    return {
                        productId: item.productId,
                        productIdName: item.productIdName,
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
        openInfo(t('already_in_the_basket'));
        dispatch(setBasketItems(contentArray))
    }

    const deleteFromBasket = (product: Product) => {
        const contentArray = getBasketContent().filter(({productId}) => product.id!==productId )
        saveToLocalStorageAndUpdateState(contentArray)
        dispatch(deleteProduct(product))
    }

    const increaceCounter = (product: Product) => {
        const contentArray: BasketItemModel[] = getBasketContent().map(({productId, productIdName, qty}) => ({
            productId,
            productIdName,
            qty: productId===product.id ? qty+1 : qty
        }))
        saveToLocalStorageAndUpdateState(contentArray)
    }
    
    const reduceCounter = (product: Product) => {
        const contentArray: BasketItemModel[] = getBasketContent().map(({productId, productIdName, qty}) => ({
            productId,
            productIdName,
            qty: productId===product.id && qty >1 ? qty-1 : qty
        }))
        saveToLocalStorageAndUpdateState(contentArray)
    }

    const changeCounter = (product: Product, counter: number) => {
        const contentArray: BasketItemModel[] = getBasketContent().map(({productId, productIdName, qty}) => ({
            productId,
            productIdName,
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
        openBasket,
        closeBasket,
        addToBasket,
        deleteFromBasket,
        increaceCounter,
        reduceCounter,
        clearBasket,
        setItems,
        changeCounter,
        productQty: basketItems.length,
        isEmptyBasket
    }
}