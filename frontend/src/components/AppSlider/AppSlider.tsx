import { Swiper, SwiperSlide } from "swiper/react"
import { Swiper as SwiperRef, SwiperOptions } from "swiper/types";


import 'swiper/css/bundle';
import 'swiper/css/grid';
import 'swiper/css/pagination';
import 'swiper/css/navigation';

import style from './AppSlider.module.scss'
import { defaultAppSliderOptions } from "./defaultSwiperSettings";
import { PreviewLoadingCard } from "../Cards/PreviewCard/PreviewLoagingCard";
import { useEffect, useRef, useState } from "react";
import { IconButton } from "../UI/IconButton/IconButton";



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


    const [paginationEl, setPaginationEl] = useState<HTMLElement | null>(null)
    const [totalBullets, setTotalBullets] = useState<number>(0)

    const controlContainer = useRef<HTMLDivElement>(null)
    const prevButton = useRef<HTMLButtonElement>(null)
    
    const preloaderArray =  Array.from({length: qtyOfPreloaderCards}, (_, i) => i); 

    const [swiperRef, setSwiperRef] = useState<SwiperRef | null>(null);


    useEffect(() => {

        if(swiperRef?.pagination){
            setTotalBullets(swiperRef.pagination.bullets.length)
        }
        
        if(paginationEl){
            controlContainer.current?.append(paginationEl)
        }
        
    }, [paginationEl, swiperRef, prevButton])
    

    useEffect(() => {
        if(swiperRef?.pagination){
            setTotalBullets(swiperRef.pagination.bullets.length);
        }
        
    }, [children.length])
   


const handlePrev = () => {
    swiperRef?.slidePrev()
}

const handleNext = () => {
    swiperRef?.slideNext()
}

   

    return (
        <Swiper 
            className={style.slider}
            onSwiper={setSwiperRef}
            onPaginationRender={(_, paginationEl) => setPaginationEl(paginationEl)}
            onSlideChange={(a) => console.log(a)
            }
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
            <div 
                ref = {controlContainer}
                className={style.control}
            
            >
                {
                    (totalBullets > 1) &&
                    <>
                        <IconButton
                            iconName="leftArrow"
                            onClick={handlePrev}
                        />
                        <IconButton
                            className={style.next}
                            iconName="rigrtArrow"
                            onClick={handleNext}
                        />
                    </>
                
                }
            </div>
        </Swiper>
    )
}