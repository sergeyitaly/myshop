import { Swiper, SwiperSlide } from "swiper/react"
import { SwiperOptions } from "swiper/types";

import 'swiper/css/bundle';
import 'swiper/css/grid';
import 'swiper/css/pagination';

import style from './AppSlider.module.scss'
import { defaultAppSliderOptions } from "./defaultSwiperSettings";
import { PreviewLoadingCard } from "../Cards/PreviewCard/PreviewLoagingCard";



interface ProductSliderProps {
    isLoading?: boolean
    children: JSX.Element[]
    sliderSettings?: SwiperOptions
    qtyOfPreloaderCards?: number
}

export const AppSlider = ({
    isLoading,
    children,
    qtyOfPreloaderCards = 4,
    sliderSettings = defaultAppSliderOptions 
}: ProductSliderProps) => {

    console.log(children);
    
    const preloaderArray =  Array.from({length: qtyOfPreloaderCards}, (_, i) => i); 

    return (
        <Swiper 
            className={style.slider}
            {...sliderSettings}
        >
           
            {
                isLoading ?
                preloaderArray.map((_, i) => (
                    <SwiperSlide
                        key = {i}
                    >
                        <PreviewLoadingCard/>
                    </SwiperSlide>
                ))
                :
                children.map((child) => (
                    <SwiperSlide
                        key={child.key}
                    >
                        {child}
                    </SwiperSlide>
                ))
            }
        </Swiper>
    )
}