import { useGetProductsByMainFilterQuery } from "../../api/productSlice"
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { AppSlider } from "../../components/AppSlider/AppSlider"
import { popularSettings } from "./sliderSettings/PopularProductSetting"
import { useNavigate } from "react-router-dom"
import { ROUTE } from "../../constants"


export const PopularProducts = () => {

    const navigate = useNavigate()

    const {data, isLoading} = useGetProductsByMainFilterQuery({popularity: 1})

    const products = data?.results || []

    return (
        <AppSlider
            isLoading = {isLoading}
            sliderSettings={popularSettings}
        >
            {
                products.map((product) => {

                    const {id, photo, name, discount, photo_tumbnail} = product

                    return (
                            <PreviewCard
                                key={id}
                                photoSrc={photo}
                                previewSrc={photo_tumbnail}
                                title={name}
                                discount={discount}
                                price={product.price}
                                currency={product.currency}
                                onClick={() => navigate(`${ROUTE.PRODUCT}${id}`)}
                            />
                    )
                })
            }
        </AppSlider>
    )
}