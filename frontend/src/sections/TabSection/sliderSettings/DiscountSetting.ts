import { Autoplay, Grid, Pagination } from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const discountSettings: SwiperOptions = 
    {
        grid: {
            rows: 1,
            fill: 'row'
        },
        slidesPerView: 1.3,
        pagination: {
            clickable: true,
        },
        spaceBetween: 20,
        modules: [Grid, Pagination, Autoplay],
        breakpoints:{
            740: {
                grid: {
                    rows: 1
                },
                slidesPerView: 4
            }
        }
    }