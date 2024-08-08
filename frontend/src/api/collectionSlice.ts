import { queryString } from "object-query-string";
import { ENDPOINTS } from "../constants";
import { Collection, Product } from "../models/entities";
import { ShortServerResponce } from "../models/server-responce";
import { apiSlice } from "./mainApiSlice";
import { CollectionFilter, ProductFilter } from "../models/filters";

interface ProductFilterInCollection extends ProductFilter {
    collectionId: number
}

export const collectionApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({

        getAllCollections: builder.query<ShortServerResponce<Collection[]>, void>({
            query: () => `${ENDPOINTS.COLLECTIONS}/`
        }),

        getCollectionsByFilter: builder.query<ShortServerResponce<Collection[]>, CollectionFilter>({
            query: (queryBuilder) => {
                const qs = queryString(queryBuilder)
                return `${ENDPOINTS.COLLECTIONS}/?${qs}`
            }
        }),

        getOneCollectionById: builder.query<Collection, number>({
            query: (collectionId) => `${ENDPOINTS.COLLECTION}/${collectionId}/`
        }),

        getCollectionByName: builder.query<Collection, string>({
            query: (collectionName) => `${ENDPOINTS.COLLECTIONS}/?search=${collectionName}`,
            transformResponse: (responce: ShortServerResponce<Collection[]>) => responce.results[0]}),

        getAllProductsFromCollection: builder.query<ShortServerResponce<Product[]>, number>({
            query: (collectionId) => `${ENDPOINTS.COLLECTION}/${collectionId}/${ENDPOINTS.PRODUCTS}/`
        }),

        getProductsFromCollectionByProductFilter: builder.query<ShortServerResponce<Product[]>, ProductFilterInCollection>({
            query: (queryBuilder) => {
                const {collectionId, ...productQueryObj} = queryBuilder
                const qs = queryString(productQueryObj)
                return `${ENDPOINTS.COLLECTION}/${collectionId}/${ENDPOINTS.PRODUCTS}/?${qs}`
            }
        }),

        getProductsByPopularity: builder.query<ShortServerResponce<Product[]>, ProductFilter>({
            query: (filter) => {
                const qs = queryString(filter);
                return `${ENDPOINTS.PRODUCTS}/?${qs}`;
            }
        }),

        getDiscountProducts: builder.query<ShortServerResponce<Product[]>, void>({
            query: () => `${ENDPOINTS.PRODUCTS}/`
        }),


    })
})

export const { 
    useGetAllCollectionsQuery,
    useGetCollectionsByFilterQuery,
    useGetOneCollectionByIdQuery,
    useGetProductsFromCollectionByProductFilterQuery,
    useGetAllProductsFromCollectionQuery,
    useGetCollectionByNameQuery,
    useGetProductsByPopularityQuery,
    useGetDiscountProductsQuery
} = collectionApiSlice