import { ReactNode } from "react"
import Slider from "react-slick"
import { settings } from "./settings"

interface AppCarouselProps {
    children: ReactNode
}

export const AppCarousel = ({children}: AppCarouselProps) => {
    return (
        <Slider {...settings}>
            {children}
        </Slider>
    )
}