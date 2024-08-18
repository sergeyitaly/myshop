import { skipToken } from "@reduxjs/toolkit/query";
import { useGetAllProductsFromCollectionQuery } from "../../api/collectionSlice";
import { ProductSliderSection } from "../../components/ProductSliderSection/ProductSliderSection";
import { useTranslation } from 'react-i18next'; // Import the hook

  interface FromThisCollectionProps {
    collectionId?: number
  }

export const FromThisCollectionSection = ({collectionId}: FromThisCollectionProps) => {
    const { t } = useTranslation(); // Use the translation hook

    
    const { data, isSuccess } = useGetAllProductsFromCollectionQuery(collectionId ?? skipToken);

    return (
       <ProductSliderSection
            isSuccess = {isSuccess}
            translateField={t("also_from_this_collection")} 
            products={data?.results}
       />
    )
}