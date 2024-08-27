import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { MainFilter } from '../models/filters';
import { Product } from '../models/entities';
import { apiBaseUrl } from './api';

// Define the response type for filter products
interface FilterResponse {
    price_min: number;
    price_max: number;
    has_discount: boolean;
    overall_price_min: number;
    overall_price_max: number;
    next: string | null;
    previous: string | null;
    count: number;
    results: Product[];
}

// Create the filter API slice
export const filterApiSlice = createApi({
    reducerPath: 'filterApi',
    baseQuery: fetchBaseQuery({ baseUrl: apiBaseUrl }), // Adjust base URL if needed
    endpoints: (builder) => ({
        getFilterData: builder.query<FilterResponse, MainFilter>({
            query: (filter) => ({
                url: '/api/products/filter/',
                params: filter, // Pass query params here
            }),
        }),
    }),
});

export const { useGetFilterDataQuery } = filterApiSlice;
