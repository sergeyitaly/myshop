import Slider from "react-slick"
import { ReactNode } from "react"
import { settings } from "./sliderSettings"
import { PageContainer } from "../containers/PageContainer"
import style from './ProductSlider.module.scss'

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
                className={style.slider}
                {...settings} 
                beforeChange={() => onAllowClick(false)}  
                afterChange={() => onAllowClick(true)} 
            >
              {children}
            </Slider>
        </PageContainer>
    </section>
    )
}