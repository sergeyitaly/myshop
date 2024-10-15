import { queryString } from "object-query-string";
import { ENDPOINTS } from "../constants";
import { Product } from "../models/entities";
import { apiSlice } from "./mainApiSlice";
import { MainFilter, ProductFilter } from "../models/filters";
import axios from "axios";
import { apiBaseUrl } from "./api";

// Response interface for /api/products/filter/
interface FilterProductsResponse {
  price_min: number;
  price_max: number;
  overall_price_min: number;
  overall_price_max: number;
  next: string | null;
  previous: string | null;
  count: number;
  results: Product[];
}

// Response interface for /api/products/
interface ProductsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Product[];
}

export const productApiSlice = apiSlice.injectEndpoints({
  endpoints: builder => ({
    // Endpoint to fetch all products with pagination
    getAllProducts: builder.query<ProductsResponse, { page: number; search?: string }>({
      query: ({ page, search }) => {
        const queryParams = new URLSearchParams({ page: page.toString() });
        if (search) queryParams.append('search', search);
        return `${ENDPOINTS.PRODUCTS}/?${queryParams.toString()}`;
      },
    }),

    // Endpoint to fetch products by ID list
    getManyProductsByIdList: builder.query<Product[], number[]>({
      queryFn: async (idList) => {
        const products = await Promise.all(idList.map(async (id) => {
          const { data } = await axios.get<Product>(`${apiBaseUrl}/api/${ENDPOINTS.PRODUCT}/${id}/`);
          return data;
        }));
        return { data: products };
      }
    }),

    // Endpoint to fetch products by filter with pagination
    getManyProductsByFilter: builder.query<FilterProductsResponse, ProductFilter>({
      query: (queryBuilder) => {
        const qs = queryString(queryBuilder);
        return `${ENDPOINTS.PRODUCTS}/?${qs}`;
      }
    }),

    // Endpoint to fetch a single product by ID
    getOneProductById: builder.query<Product, number>({
      query: (productId) => `${ENDPOINTS.PRODUCT}/${productId}/`
    }),
   
    getOneProductByIdName: builder.query<Product, string>({
      query: (idName) => `${ENDPOINTS.PRODUCT}/${idName}/`
    }),

    // Endpoint to fetch products by main filter with pagination
    getProductsByMainFilter: builder.query<FilterProductsResponse, MainFilter>({
      query: (queryBuilder) => {
        const qs = queryString(queryBuilder);
        return `${ENDPOINTS.FILTER}/?${qs}`;
      }
    })
  })
});

export const {
  useGetAllProductsQuery,
  useGetManyProductsByFilterQuery,
  useGetOneProductByIdQuery,
  useGetManyProductsByIdListQuery,
  useGetProductsByMainFilterQuery,
  useGetOneProductByIdNameQuery
} = productApiSlice;
