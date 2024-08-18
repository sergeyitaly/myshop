import { ReactNode } from "react"
import { Swiper, SwiperSlide } from "swiper/react"
import {Grid, Pagination} from 'swiper/modules'
import { screens } from "../../constants"
import { useMediaQuery } from "@mui/material"

import 'swiper/css/bundle';
import 'swiper/css/grid';
import 'swiper/css/pagination';

import style from './ProductSlider.module.scss'
import { grid } from "@mui/system"

interface ProductSliderProps {
    children: JSX.Element[]
}

export const ProductSlider = ({
    children,
}: ProductSliderProps) => {

    const isMobile = useMediaQuery(screens.maxMobile)


    return (
        <Swiper 
            className={style.slider}
            grid={{
                rows: 2,
                fill: 'row'
            }}
            slidesPerView={2}
            pagination={{
                clickable: true,
              }}
            spaceBetween={20}
            modules={[Grid, Pagination]}
            breakpoints={{
                740: {
                    grid: {
                        rows: 1
                    },
                    slidesPerView: 4
                }
            }}
        >
            {children}
        </Swiper>
    )
}