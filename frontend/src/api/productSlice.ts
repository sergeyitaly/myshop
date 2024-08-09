import { queryString } from "object-query-string";
import { ENDPOINTS } from "../constants";
import { Product } from "../models/entities";
import { ServerResponce, ShortServerResponce } from "../models/server-responce";
import { apiSlice } from "./mainApiSlice";
import { MainFilter, ProductFilter } from "../models/filters";
import axios from "axios";
import { apiBaseUrl } from "./api";

export const productApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({

        getAllProducts: builder.query<ServerResponce<Product[]>, void>({
            query: () => `${ENDPOINTS.PRODUCTS}/`
          }),

        getManyProductsByIdList: builder.query<Product[], number[]>({
            queryFn: async (idList) => {
                const products = await Promise.all(idList.map(async (id) => {
                    const {data} = await axios.get<Product>(`${apiBaseUrl}/api/${ENDPOINTS.PRODUCT}/${id}/`)
                    return data
                }))

                return {data: products}
            }
        }),

        getManyProductsByFilter: builder.query<ServerResponce<Product[]>, ProductFilter>({
            query: (queryBuilder) => {
                const qs = queryString(queryBuilder)
                return `${ENDPOINTS.PRODUCTS}/?${qs}`
            }
        }),

        getOneProductById: builder.query<Product, number>({
            query: (productId) => `${ENDPOINTS.PRODUCT}/${productId}/`
        }),

        getProductsByMainFilter: builder.query<ShortServerResponce<Product[]>, MainFilter>({
            query: (queryBuilder) => {
                const qs = queryString(queryBuilder)
                return `${ENDPOINTS.FILTER}/?${qs}`
            }
        })
    })
})

export const {
    useGetAllProductsQuery,
    useGetManyProductsByFilterQuery,
    useGetOneProductByIdQuery,
    useGetManyProductsByIdListQuery,
    useGetProductsByMainFilterQuery
} = productApiSlice