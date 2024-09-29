import { useGetProductsByMainFilterQuery } from "../../api/productSlice"
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { AppSlider } from "../../components/AppSlider/AppSlider"
import { discountSettings } from "./sliderSettings/DiscountSetting"
import { useNavigate } from "react-router-dom"
import { ROUTE } from "../../constants"


export const ProductsWithDiscount = () => {

    const navigate = useNavigate()

    const {data, isLoading} = useGetProductsByMainFilterQuery({has_discount: true})

    const products = data?.results || []

    return (
        <AppSlider
            isLoading = {isLoading}
            sliderSettings={discountSettings}
        >
            {
                products.map((product) => {

                    const {id, photo, name, discount, photo_tumbnail, currency, price} = product

                    return (
                       
                            <PreviewCard
                                key={id}
                                photoSrc={photo}
                                previewSrc={photo_tumbnail}
                                title={name}
                                discount={discount}
                                price={price}
                                currency={currency}
                                onClick = {() => navigate(`${ROUTE.PRODUCT}${id}`)}
                            />
                    )
                })
            }
        </AppSlider>
    )
}