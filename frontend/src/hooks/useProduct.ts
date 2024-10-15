import { useEffect, useState } from "react";
import { Product, ProductVariantsModel } from "../models/entities";
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../constants";
import { useGetOneProductByIdNameQuery, useGetProductsByMainFilterQuery } from "../api/productSlice";
import { skipToken } from "@reduxjs/toolkit/query";


const initialVariants: ProductVariantsModel = {
    colors: [],
    sizes: []
}

export const useProduct = (idName: string) => {

    const [variants, setVariants] = useState<ProductVariantsModel>(initialVariants)
    // const [counter, setCounter] = useState<number>(1)

    const {
      data: product, 
      isLoading: isLoadingProduct, 
      isFetching
    } = useGetOneProductByIdNameQuery(idName)

    const {
      data: productsResponce, 
      isLoading: isLoadingProducts,
      isFetching: isFetchingProducts
    } = useGetProductsByMainFilterQuery(product ? {name: product.name} : skipToken)

    const products = productsResponce?.results

    const navigate = useNavigate()

    useEffect(() => {
        if(products?.length){
            const allColors = products.map(product => product.color_value).filter(color => !!color) as string[]
            const uniqueColors = new Set(allColors)
            const colors = Array.from(uniqueColors).map(color => {
              const prod = products.find(product => product.color_value === color) as Product
              const uniqueColor = prod.color_value as string
              return {color: uniqueColor}
            })


            const allSizes = products.map(product => product.size).filter(size => !!size) as string[]
            const sizes = new Set(allSizes)
            
            setVariants({colors, sizes: Array.from(sizes)})
        }
    }, [products])

      const changeColor = (value: string) => {
        if(product && products){
          const matchProduct = products.find(item => ((item.size === product.size) && (item.color_value === value)))
          if(matchProduct) {
            navigate(`${ROUTE.PRODUCT}${matchProduct.id_name}`)
            return
          }
          const matchColor = products.find(item => item.color_value === value) 
          if(matchColor) navigate(`${ROUTE.PRODUCT}${matchColor.id_name}`)
        }
      }
      
      const changeSize = (value: string) => {
        if(product && products){
          const matchProduct = products.find(item => ((item.color_value === product.color_value) && (item.size === value)))
          if(matchProduct) {
            navigate(`${ROUTE.PRODUCT}${matchProduct.id_name}`)
            return
          }
          const matchColor = products.find(item => item.size === value) 
          if(matchColor) navigate(`${ROUTE.PRODUCT}${matchColor.id_name}`)
        }
      }


    return {
        product,
        products,
        isLoading: isLoadingProduct || isLoadingProducts,
        isFetching: isFetching || isFetchingProducts,
        variants,
        changeColor,
        changeSize
    }
}