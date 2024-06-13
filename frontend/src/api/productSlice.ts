import { queryString } from "object-query-string";
import { ENDPOINTS } from "../constants";
import { Product } from "../models/entities";
import { ServerResponce } from "../models/server-responce";
import { apiSlice } from "./mainApiSlice";
import { ProductFilter } from "../models/filters";

export const productApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({

        getAllProducts: builder.query<ServerResponce<Product[]>, void>({
            query: () => `${ENDPOINTS.PRODUCTS}/`
          }),

        getManyProductsByFilter: builder.query<ServerResponce<Product[]>, ProductFilter>({
            query: (queryBuilder) => {
                const qs = queryString(queryBuilder)
                return `${ENDPOINTS.PRODUCTS}/?${qs}`
            }
        }),

        getOneProductById: builder.query<Product, number>({
            query: (productId) => `${ENDPOINTS.PRODUCT}/${productId}/`
        })
    })
})

export const {
    useGetAllProductsQuery,
    useGetManyProductsByFilterQuery,
    useGetOneProductByIdQuery
} = productApiSlice