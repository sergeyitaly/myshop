import { Grid, Pagination, Navigation} from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const defaultAppSliderOptions: SwiperOptions = {
    grid: {
        rows: 2,
        fill: 'row'
    },
    slidesPerView: 2,
    pagination: {
        clickable: true,
    },
    spaceBetween: 20,
    modules: [Grid, Pagination, Navigation],
    breakpoints:{
        740: {
            grid: {
                rows: 1
            },
            slidesPerView: 4
        }
    },
    autoplay:{
        delay: 1000,
        pauseOnMouseEnter: true
    }
} 