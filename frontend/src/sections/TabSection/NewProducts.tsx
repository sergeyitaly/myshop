import { AppSlider } from "../../components/AppSlider/AppSlider"
import { CategoryCard } from "../../components/Cards/CategoryCard/CategoryCard"
import { useGetAllCollectionsQuery } from "../../api/collectionSlice"
import { newProductsSettings } from "./sliderSettings/NewProductSetting"
import { useAppTranslator } from "../../hooks/useAppTranslator"
import { useNavigate } from "react-router-dom"
import { ROUTE, screens } from "../../constants"
import { useMediaQuery } from "@mui/material"


export const NewProducts = () => {

    const navigate = useNavigate()

    const isMobile = useMediaQuery(screens.maxMobile)

    const {data, isLoading} = useGetAllCollectionsQuery()    

    const collections = data?.results || []

    const {getCollectionName} = useAppTranslator()

    return (
        <AppSlider
            isLoading = {isLoading}
            sliderSettings={newProductsSettings}
            qtyOfPreloaderCards={isMobile ? 1 : 2}
        >
            {
                collections.map((collection) => {

                    const {id, photo, photo_thumbnail_url} = collection

                    return (
                            <CategoryCard
                                key={id}
                                title={getCollectionName(collection)}
                                photoSrc={photo}
                                previewSrc={photo_thumbnail_url}
                                onClick={() => navigate(`${ROUTE.COLLECTION}${id}`)}
                            />
                    )
                })
            }
        </AppSlider>
    )
}