import {Settings} from "react-slick";

export const settings: Settings = {
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 4,
    initialSlide: 0,
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
          }
        },
        {
          breakpoint: 740,
          settings: {
            centerPadding: '100px',
            infinite: true,
            slidesToShow: 2,
            slidesToScroll: 2,
            rows: 2,
            slidesPerRow: 1
          }
        },
    ]
}