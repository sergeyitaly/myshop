import { useGetProductsByMainFilterQuery } from "../../api/productSlice"
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { AppSlider } from "../../components/AppSlider/AppSlider"


export const PopularProducts = () => {

    const {data, isLoading} = useGetProductsByMainFilterQuery({popularity: 1})

    const products = data?.results || []

    console.log(data);
    

    return (
        <AppSlider
            isLoading = {isLoading}
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
                            />
                    )
                })
            }
        </AppSlider>
    )
}