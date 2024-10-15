import { useGetProductsByMainFilterQuery } from "../../api/productSlice"
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { AppSlider } from "../../components/AppSlider/AppSlider"
import { lightSettings } from "./sliderSettings/LightSettings"
import styles from './TabSection.module.scss'
import { useNavigate } from "react-router-dom"
import { ROUTE } from "../../constants"
import { useAppTranslator } from "../../hooks/useAppTranslator"


export const LightSection = () => {

    const navigate = useNavigate()

    const {data, isLoading} = useGetProductsByMainFilterQuery({category: '5'})

    const products = data?.results || []

    const {getTranslatedProductName} = useAppTranslator()

    
    

    return (
        <AppSlider
            isLoading = {isLoading}
            sliderSettings={lightSettings}
        >
            {
                products.map((product) => {

                    const {id, photo, id_name, discount, photo_tumbnail} = product

                    return (
                            <PreviewCard
                                key={id}
                                className={styles.lightCard}
                                photoSrc={photo}
                                previewSrc={photo_tumbnail}
                                title={getTranslatedProductName(product)}
                                discount={discount}
                                price={product.price}
                                currency={product.currency}
                                onClick={() => navigate(`${ROUTE.PRODUCT}${id_name}`)}
                            />
                    )
                })
            }
        </AppSlider>
    )
}