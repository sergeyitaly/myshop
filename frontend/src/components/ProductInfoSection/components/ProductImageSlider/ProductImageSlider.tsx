import Slider from "react-slick"
import { ProductImage } from "../../../../models/entities"
import { settings } from "./SliderSettings"
import { ProductImageSlide } from "../ProductImageSlide/ProductImageSlide";

interface ProductImageSliderProps {
    images: ProductImage[]
    className?: string,
    onClickZoom?: (src: string) => void
}

export const ProductImageSlider = ({
    images,
    className,
    onClickZoom
}: ProductImageSliderProps) => {

    const handleClickZoom = (src: string) => {
        onClickZoom && onClickZoom(src)
    }

    return (
        <>
            {
                images.length > 1 ?
                <Slider {...settings} className={className}>
                    {
                        images.map((image) => (
                            <ProductImageSlide
                                key={image.id}
                                src={image.images}
                                alt={image.id}
                                onClickZoom={handleClickZoom}
                            />
                        ))
                    }
                </Slider>
                : 
                <div className={className}>
                    <ProductImageSlide
                        src={images[0].images}
                        alt={images[0].id}
                        onClickZoom={handleClickZoom}
                    />
                </div>
            }
        </>
    )
}