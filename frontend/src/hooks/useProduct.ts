import { useEffect, useState } from "react";
import { Product, ProductVariantsModel } from "../models/entities";
import { getProductNameById, getProducts } from "../api/api";
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../constants";


const initialVariants: ProductVariantsModel = {
    colors: [],
    sizes: []
}

export const useProduct = (productId?: number | string) => {

    const [isLoading, setLoading] = useState<boolean>(true)
    const [isFetching, setFetching] = useState<boolean>(false)
    const [product, setProduct] = useState<Product | null>(null);
    const [products, setProducts] = useState<Product[]>([])
    const [variants, setVariants] = useState<ProductVariantsModel>(initialVariants)

    const navigate = useNavigate()

    useEffect(() => {
        setFetching(true)
        if(!productId){
          setLoading(false)
          setFetching(false)
          return
        }
        fetchData(productId)
    }, [productId]);

    useEffect(() => {
        if(products.length){
            const colors = products.map(product => ({color: product.color}))
            const sizes = products.map(product => product.size)
            setVariants({colors, sizes})
        }
    }, [products])

    const fetchData = async (id: number | string) => {
        try {
          const productData = await getProductNameById(id);
          const theSameProducts = await getProducts(`name=${productData.name}`)
          setProducts(theSameProducts);
          
          setProduct(productData);
        } catch (error) {
          console.error('Error fetching product:', error);
        } finally {
          setLoading(false);
          setFetching(false)
        }
      };

      const changeColor = (value: string) => {
        if(product){
          const matchProduct = products.find(item => ((item.size === product.size) && (item.color === value)))
          if(matchProduct) {
            navigate(`${ROUTE.PRODUCT}${matchProduct.id}`)
            return
          }
          const matchColor = products.find(item => item.color === value) 
          if(matchColor) navigate(`${ROUTE.PRODUCT}${matchColor.id}`)
        }
      }
      
      const changeSize = (value: string) => {
        if(product){
          const matchProduct = products.find(item => ((item.color === product.color) && (item.size === value)))
          if(matchProduct) {
            navigate(`${ROUTE.PRODUCT}${matchProduct.id}`)
            return
          }
          const matchColor = products.find(item => item.size === value) 
          if(matchColor) navigate(`${ROUTE.PRODUCT}${matchColor.id}`)
        }
      }

    


    return {
        product,
        products,
        isLoading,
        isFetching,
        variants,
        changeColor,
        changeSize
    }
}