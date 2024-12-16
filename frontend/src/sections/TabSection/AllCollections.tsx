import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { useGetAllCollectionsQuery } from "../../api/collectionSlice"
import { AppSlider } from "../../components/AppSlider/AppSlider"
import { allCollectionSettings } from "./sliderSettings/AllCollectionSetting"
import { useNavigate } from "react-router-dom"
import { ROUTE } from "../../constants"
import { useAppTranslator } from "../../hooks/useAppTranslator"


export const AllCollections = () => {


    const navigate = useNavigate()
    
    const {data, isLoading} = useGetAllCollectionsQuery()

    const collections = data?.results || []

    const { getCategoryName, getCollectionName } = useAppTranslator()

    return (
        <AppSlider 
            isLoading = {isLoading}
            sliderSettings={allCollectionSettings}
        >
            {
                collections.map((collection) => {

                    const {id, photo, photo_thumbnail_url, category} = collection

                    return (
                        <PreviewCard
                            key={id}
                            photoSrc={photo}
                            previewSrc={photo_thumbnail_url}
                            subTitle={category ? getCategoryName(category) : ''}
                            title={getCollectionName(collection)}
                            onClick={() => navigate(`${ROUTE.COLLECTION}${id}`)}
                        />
                    )
                })
            }
        </AppSlider>
    )
}