import { useGetProductsByMainFilterQuery } from "../../api/productSlice"
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { AppSlider } from "../../components/AppSlider/AppSlider"
import { discountSettings } from "./sliderSettings/DiscountSetting"
import { useNavigate } from "react-router-dom"
import { ROUTE, screens } from "../../constants"
import { useAppTranslator } from "../../hooks/useAppTranslator"
import { useMediaQuery } from "@mui/material"


export const ProductsWithDiscount = () => {

    const navigate = useNavigate()

    const isMobile = useMediaQuery(screens.maxMobile)

    const {data, isLoading} = useGetProductsByMainFilterQuery({has_discount: true})

    const products = data?.results || []

    const {getTranslatedProductName} = useAppTranslator()

    return (
        <AppSlider
            isLoading = {isLoading}
            sliderSettings={discountSettings}
            qtyOfPreloaderCards={isMobile ? 2 : 4}n
        >
            {
                products.map((product) => {

                    const {id, id_name, photo, discount, photo_tumbnail, currency, price} = product

                    return (
                       
                            <PreviewCard
                                key={id}
                                photoSrc={photo}
                                previewSrc={photo_tumbnail}
                                title={getTranslatedProductName(product)}
                                discount={discount}
                                price={price}
                                currency={currency}
                                onClick = {() => navigate(`${ROUTE.PRODUCT}${id_name}`)}
                            />
                    )
                })
            }
        </AppSlider>
    )
}