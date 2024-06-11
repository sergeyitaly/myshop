import { useEffect, useState } from "react"
import { Product } from "../models/entities"
import { getCollectionProducts } from "../api/api"


export const useCollectionProducts = (collectionId?: number) => {

    const [products, setProducts] = useState<Product[]>([])

    useEffect(() => {
        const fetchData = async () => {
                if(collectionId){
                    console.log(collectionId);
                    
                    const fetchedProducts = await getCollectionProducts(collectionId)
                    setProducts(fetchedProducts.results)
                }
        }
        fetchData()
    }, [collectionId])

    return {
        products
    }
}