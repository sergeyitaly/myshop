import { useEffect, useState } from "react"
import { Collection } from "../models/entities"
import { getCollectionsByFilter } from "../api/api"


export const useCollectionByName = (name?: string) => {
    const [collection, setCollection] = useState<Collection | null>(null)

    useEffect(() => {

        const fetchData = async () => {
            try{
                const responce = name ? await getCollectionsByFilter({search: name}) : null
                if(responce) setCollection(responce.results[0])
            }
            catch(err){
                console.error(err)
            }
        }

        fetchData()    
    }, [name])

    return {
        collection
    }
}