import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { ProductSliderSection } from "../../components/ProductSliderSection/ProductSliderSection"


export const BestSellersSection = () => {

    const {data} = useGetProductsByMainFilterQuery({
        page_size: 100
      })

      console.log(data?.results);
      

    return (
        <ProductSliderSection
            translateField="bestsellers"
            products={data?.results}
        />
    )
}