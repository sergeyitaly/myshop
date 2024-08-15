import Slider from "react-slick"
import { ReactNode, useState } from "react"
import { settings } from "./sliderSettings"
import style from './ProductSlider.module.scss'
import clsx from "clsx"

interface ProductSliderProps {
    children: ReactNode
}

export const ProductSlider = ({
    children,
}: ProductSliderProps) => {

    const [disabled, setDisabled] = useState<boolean>(false);

    return (
        <Slider 
            className={clsx(style.slider, {
                [style.disabled]: disabled
            })}
            {...settings} 
            afterChange={() => setDisabled(false)} 
            swipeEvent={() => setDisabled(true)}
        >
            {children}
        </Slider>
    )
}