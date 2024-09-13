import { ENDPOINTS } from "../constants";
import { OrderDTO } from "../models/dto";
import { apiSlice } from "./mainApiSlice";
import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

export interface CreateOrderErrorResponce {
    status: number
    data: {
        name: string
    }
}

export const collectionApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        createOrder: builder.mutation<string, OrderDTO>({
            query: (body) => ({
                body,
                method: 'POST',
                url: `${ENDPOINTS.ORDER}/`
            }),
            transformErrorResponse: (baseQueryReturnValue: CreateOrderErrorResponce) => {
                return baseQueryReturnValue
            },
        })
    })
})

export const {
    useCreateOrderMutation
} = collectionApiSlice

