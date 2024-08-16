// api/filterApiSlice.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { MainFilter } from '../models/filters'; // Adjust the import if necessary

interface FilterResponse {
    price_min: number;
    price_max: number;
    // Other filter-related fields if necessary
}

export const filterApiSlice = createApi({
    reducerPath: 'filterApi',
    baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
    endpoints: (builder) => ({
        getFilterData: builder.query<FilterResponse, MainFilter>({
            query: (filter) => ({
                url: 'products/filter',
                method: 'POST', // Adjust if necessary
                body: filter,
            }),
        }),
        // Other endpoints if necessary
    }),
});

export const { useGetFilterDataQuery } = filterApiSlice;
