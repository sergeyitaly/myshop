import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { apiBaseUrl } from './api'


export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: `${apiBaseUrl}/api` }),
  tagTypes: ['Products'],
  endpoints: () => ({
    
  })
})
