import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { useGetAllCollectionsQuery } from "../../api/collectionSlice"
import { AppSlider } from "../../components/AppSlider/AppSlider"


export const AllCollections = () => {


    
    const {data, isLoading} = useGetAllCollectionsQuery()

    const collections = data?.results || []

    

    return (
        <AppSlider 
            isLoading = {isLoading}
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
                        />
                    )
                })
            }
        </AppSlider>
    )
}