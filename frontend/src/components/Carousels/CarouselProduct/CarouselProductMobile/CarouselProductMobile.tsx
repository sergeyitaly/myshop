import React from "react";
import Slider, { Settings } from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import productImageMob from "../../../../assets/collection/invidaMob.svg";
import style from "./CarouselProductMobile.module.scss";

const CarouselProductMobile: React.FC = () => {
  const settings: Settings = {
    dots: true,
    lazyLoad: "ondemand", // Specify lazyLoad as "ondemand" or "progressive"
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    initialSlide: 2,
    variableWidth: false,
  };

  return (
    <div>
      <Slider className={style.swiperContainer} {...settings}>
        <div className={style.swiperSlide}>
          <img className={style.imgMob} src={productImageMob} alt="invida" />
        </div>
        <div className={style.swiperSlide}>
          <img src={productImageMob} alt="invida" />
        </div>
      </Slider>
    </div>
  );
};

export default CarouselProductMobile;
