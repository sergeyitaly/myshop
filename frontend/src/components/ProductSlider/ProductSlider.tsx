import Slider from "react-slick"
import { ReactNode } from "react"
import { settings } from "./sliderSettings"
import style from './ProductSlider.module.scss'
import { PageContainer } from "../containers/PageContainer"

interface ProductSliderProps {
    title: string
    children: ReactNode
    onAllowClick: (status: boolean) => void
}

export const ProductSlider = ({
    title,
    children,
    onAllowClick
}: ProductSliderProps) => {

    return (
    <section>
        <PageContainer>
            <h2 className={style.title}>{title}</h2>
            <Slider 
            {...settings} 
            beforeChange={() => onAllowClick(false)}  
            afterChange={() => onAllowClick(true)} >
              {children}
            </Slider>
        </PageContainer>
    </section>
    )
}