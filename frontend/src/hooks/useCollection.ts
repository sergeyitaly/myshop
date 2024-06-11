import { useEffect, useState } from "react"
import { Collection } from "../models/entities"
import { getCollectionNameById } from "../api/api"




export const useCollection = (id?: number) => {

    const [collection, setCollection] = useState<Collection | null>(null)

    useEffect(() => {

        const fetchData = async () => {
            const newCollection = id ? await getCollectionNameById(id) : null
            setCollection(newCollection)
            
        }

        fetchData()    
    }, [id])

    return {
        collection
    }
}