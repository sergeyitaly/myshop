import React from "react";
import Slider, { Settings } from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import productImgMax from "../../img/Rectangle 45.svg";
import ringQueen from "../../img/Rectangle 45.svg";
import braceletQueen from "../../img/Rectangle 45.svg";
import ringsSet from "../../img/Rectangle 45.svg";
import earrings from "../../img/Rectangle 45.svg";
import style from "./CarouselProductDesktop.module.scss";

const CarouselProductDesktop: React.FC = () => {
  const settings: Settings = {
    customPaging: function (i: number) {
      let imgSrc;
      switch (i) {
        case 0:
          imgSrc = productImgMax;
          break;
        case 1:
          imgSrc = ringQueen;
          break;
        case 2:
          imgSrc = braceletQueen;
          break;
        case 3:
          imgSrc = ringsSet;
          break;
        case 4:
          imgSrc = earrings;
          break;
        default:
          imgSrc = productImgMax;
      }
      return <img src={imgSrc} alt={`Thumbnail ${i}`} />;
    },
    arrows: false,
    dots: true,
    dotsClass: "slick-dots slick-thumb",
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };

  return (
    <div className={style.sliderContainer}>
      <div className={style.slider}>
        <Slider {...settings}>
          <div className={style.mainBox}>
            <img
              className={style.mainImg}
              src={productImgMax}
              alt="Product Image Max"
            />
          </div>
          <div>
            <img className={style.slickImg} src={ringQueen} alt="Ring Queen" />
          </div>
          <div>
            <img
              className={style.slickImg}
              src={braceletQueen}
              alt="Bracelet Queen"
            />
          </div>
          <div>
            <img className={style.slickImg} src={ringsSet} alt="Rings Set" />
          </div>
          <div>
            <img className={style.slickImg} src={earrings} alt="Earrings" />
          </div>
        </Slider>
      </div>
    </div>
  );
};

export default CarouselProductDesktop;
