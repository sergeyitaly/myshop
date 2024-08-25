import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { ProductSliderSection } from "../../components/ProductSliderSection/ProductSliderSection"


export const BestSellersSection = () => {

    const {data, isLoading, isSuccess} = useGetProductsByMainFilterQuery({
        page_size: 100
      })      
    return (
        <ProductSliderSection
            isSuccess = {isSuccess}
            isLoading = {isLoading}
            translateField="bestsellers"
            products={data?.results}
        />
    )
}