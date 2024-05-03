import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import imgProductMax from "../../img/Rectangle 45.svg";
import style from "./CarouselProductDesktop.module.scss";

const CarouselProductMobile = () => {
  const settings = {
    dots: true,
    lazyLoad: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    initialSlide: 2,
    variableWidth: false,
  };
  return (
    <>
      <Slider className={style.swiperContainer} {...settings}>
        <div className={style.swiperSlide}>
          <img className={style.imgMob} src={imgProductMax} alt="invida" />
        </div>
        <div className={style.swiperSlide}>
          <img src={imgProductMax} alt="invida" />
        </div>
        <div className={style.swiperSlide}>
          <img src={imgProductMax} alt="invida" />
        </div>
        <div className={style.swiperSlide}>
          <img src={imgProductMax} alt="invida" />
        </div>
      </Slider>
    </>
  );
};

export default CarouselProductMobile;
