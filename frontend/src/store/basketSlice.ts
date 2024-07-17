import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { Product } from "../models/entities";

export interface BasketItemModel {
    productId: number
    qty: number
}

interface InitialStateModel {
    openStatus: boolean
    basketItems: BasketItemModel[]
    totalPrice: number
    bootstrapIdList: number[]
    products: Product[]
}

const initialState: InitialStateModel = {
    openStatus: false,
    basketItems: [],
    totalPrice: 0,
    bootstrapIdList: [],
    products: []
}

export const basketSlice = createSlice({
    name: 'basket',
    initialState,
    reducers: {
        setOpenStatus: (state, action: PayloadAction<boolean>) => {
            state.openStatus = action.payload
        },

        setBasketItems: (state, action: PayloadAction<BasketItemModel[]>) => {
            state.basketItems = action.payload
        },

        setTotalPrice: (state, action: PayloadAction<number>) => {
            state.totalPrice = action.payload
        },

        resetBasket: () => initialState,

        setBootstrapIdList: (state) => {
            state.bootstrapIdList = state.basketItems.map(({productId}) => productId)
        },

        setProducts: (state, action: PayloadAction<Product[]>) => {
            state.products = action.payload
        },

        addProduct: (state, action: PayloadAction<Product>) => {
            const isExist = state.products.some(({id}) => id === action.payload.id)
            if(!isExist) state.products.push(action.payload)
        },
      
        deleteProduct: (state, action: PayloadAction<Product>) => {
            state.products = state.products.filter(({id}) => id !== action.payload.id)
        }
       
    }
})

export const {
    setOpenStatus,
    setBasketItems,
    setTotalPrice,
    resetBasket,
    setBootstrapIdList,
    setProducts,
    addProduct,
    deleteProduct,
} = basketSlice.actions