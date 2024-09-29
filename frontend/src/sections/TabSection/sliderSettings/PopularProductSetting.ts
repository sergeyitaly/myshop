import { Grid, Pagination } from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const popularSettings: SwiperOptions = 
    {
        grid: {
            rows: 2,
            fill: 'row'
        },
        slidesPerView: 2,
        pagination: {
            clickable: true,
        },
        spaceBetween: 20,
        modules: [Grid, Pagination],
        breakpoints:{
            740: {
                grid: {
                    rows: 1
                },
                slidesPerView: 4
            }
        }
    }