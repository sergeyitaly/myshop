import { PayloadAction, createSlice } from "@reduxjs/toolkit";

export interface BasketItemModel {
    productId: number
    qty: number
}

interface InitialStateModel {
    openStatus: boolean
    basketItems: BasketItemModel[]
    totalPrice: number
}

const initialState: InitialStateModel = {
    openStatus: false,
    basketItems: [],
    totalPrice: 0
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
        }
    }
})

export const {
    setOpenStatus,
    setBasketItems,
    setTotalPrice
} = basketSlice.actions