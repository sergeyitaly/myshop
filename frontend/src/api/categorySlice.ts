import { queryString } from "object-query-string";
import { ENDPOINTS } from "../constants";
import { Category } from "../models/entities";
import { CategoryFilter } from "../models/filters";
import { ShortServerResponce } from "../models/server-responce";
import { apiSlice } from "./mainApiSlice";

export const categoryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({

        getAllCategories: builder.query<ShortServerResponce<Category[]>, void>({
            query: () => `${ENDPOINTS.CATEGORIES}/`
        }),
       
        getCategoriesByFilter: builder.query<ShortServerResponce<Category[]>, CategoryFilter>({
            query: (queryBuilder) => {
                const qs = queryString(queryBuilder)
                return `${ENDPOINTS.CATEGORIES}/?${qs}`
            }
        }),

        getOneCategoryById: builder.query<Category, number>({
            query: (categoryId) => `${ENDPOINTS.CATEGORY}/${categoryId}` 
        })
    })
})

export const {
    useGetAllCategoriesQuery,
    useGetCategoriesByFilterQuery,
    useGetOneCategoryByIdQuery
} = categoryApiSlice
