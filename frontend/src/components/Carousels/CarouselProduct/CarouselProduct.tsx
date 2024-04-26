import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import productImageMob from "../../../assets/collection/invidaMob.svg";
import style from "./CarouselProduct.module.scss";

const CarouselProduct = () => {
  const settings = {
    dots: true,
    fade: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    waitForAnimate: false,
  };
  return (
    <div className={style.sliderContaine}>
      <Slider {...settings}>
        <div>
          <img src={productImageMob} />
        </div>
        <div>
          <img src={productImageMob} />
        </div>
        <div>
          <img src={productImageMob} />
        </div>
        <div>
          <img src={productImageMob} />
        </div>
      </Slider>
    </div>
  );
};

export default CarouselProduct;
