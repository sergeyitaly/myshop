import { Autoplay, Grid, Pagination } from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const allCollectionSettings: SwiperOptions = 
    {
        grid: {
            rows: 1,
            fill: 'row'
        },
        slidesPerView: 1,
        pagination: {
            clickable: true,
        },
        spaceBetween: 20,
        modules: [Grid, Pagination, Autoplay],
        breakpoints:{
            480: {
                grid: {
                    rows: 1
                },
                slidesPerView: 2
            },
            740: {
                grid: {
                    rows: 1
                },
                slidesPerView: 4
            }
        }
    }