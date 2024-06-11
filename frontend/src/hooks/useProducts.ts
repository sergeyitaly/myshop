import { useEffect, useState } from "react"
import { Product } from "../models/entities"
import { getProducts } from "../api/api"


export const useProducts = () => {

    const [products, setProducts] = useState<Product[]>([])

    useEffect(() => {

        const fetchData = async () => {
            const products = await getProducts()
            setProducts(products)
        }
        fetchData()
      }, [])
    

    return {
        products
    }
}