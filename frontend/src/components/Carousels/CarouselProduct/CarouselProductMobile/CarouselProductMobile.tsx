import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import productImageMob from "../../../../assets/collection/invidaMob.svg";
import style from "./CarouselProductMobile.module.scss";

const CarouselProductMobile = () => {
  const settings = {
    dots: true,
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
          <img className={style.imgMob} src={productImageMob} alt="invida" />
        </div>
        <div className={style.swiperSlide}>
          <img src={productImageMob} alt="invida" />
        </div>
      </Slider>
    </>
  );
};

export default CarouselProductMobile;
