import { Swiper } from "swiper/react"
import {Grid, Pagination} from 'swiper/modules'

import 'swiper/css/bundle';
import 'swiper/css/grid';
import 'swiper/css/pagination';

import style from './ProductSlider.module.scss'

interface ProductSliderProps {
    children: JSX.Element[]
}

export const ProductSlider = ({
    children,
}: ProductSliderProps) => {



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