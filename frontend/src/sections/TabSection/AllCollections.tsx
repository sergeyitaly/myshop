import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { useGetAllCollectionsQuery } from "../../api/collectionSlice"
import { AppSlider } from "../../components/AppSlider/AppSlider"
import { allCollectionSettings } from "./sliderSettings/AllCollectionSetting"
import { useNavigate } from "react-router-dom"
import { ROUTE } from "../../constants"


export const AllCollections = () => {


    const navigate = useNavigate()
    
    const {data, isLoading} = useGetAllCollectionsQuery()

    const collections = data?.results || []

    

    return (
        <AppSlider 
            isLoading = {isLoading}
            sliderSettings={allCollectionSettings}
        >
            {
                collections.map((collection) => {

                    const {id, photo, name, photo_thumbnail_url, category} = collection

                    return (
                        <PreviewCard
                            key={id}
                            photoSrc={photo}
                            previewSrc={photo_thumbnail_url}
                            subTitle={category?.name}
                            title={name}
                            onClick={() => navigate(`${ROUTE.COLLECTION}${id}`)}
                        />
                    )
                })
            }
        </AppSlider>
    )
}