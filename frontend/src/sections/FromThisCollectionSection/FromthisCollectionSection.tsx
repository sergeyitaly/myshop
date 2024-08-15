import { skipToken } from "@reduxjs/toolkit/query";
import { useGetAllProductsFromCollectionQuery } from "../../api/collectionSlice";
import { ProductSliderSection } from "../../components/ProductSliderSection/ProductSliderSection";




  interface FromThisCollectionProps {
    collectionId?: number
  }

export const FromThisCollectionSection = ({collectionId}: FromThisCollectionProps) => {

    
    const { data } = useGetAllProductsFromCollectionQuery(collectionId ?? skipToken);

    return (
       <ProductSliderSection
            translateField="also_from_this_collection"
            products={data?.results}
       />
    )
}