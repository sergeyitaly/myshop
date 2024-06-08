import Slider from "react-slick"
import { ReactNode } from "react"
import { settings } from "./sliderSettings"
import style from './ProductSlider.module.scss'
import { PageContainer } from "../StyledComponents/PageContainer"

interface ProductSliderProps {
    title: string
    children: ReactNode
}

export const ProductSlider = ({
    title,
    children
}: ProductSliderProps) => {

    return (
    <section>
        <PageContainer>
            <h2 className={style.title}>{title}</h2>
            <Slider {...settings}>
              {children}
            </Slider>
        </PageContainer>
    </section>
    )
}