import { useState } from "react";
import productImgMin from "../../assets/collection/Rectangle 63.svg";
import productImgMax from "../../assets/collection/Rectangle 45.svg";
import arrow from "./icons/fluent_ios-arrow-24-regular.svg";
import style from "./ProductPage.module.scss";

const ProductPage = () => {
  const [counter, setCounter] = useState(1);
  const handleIncrementCounter = () => {
    setCounter(counter + 1);
  };

  const handleDecrementCounter = () => {
    if (counter === 1) return;

    setCounter(counter - 1);
  };

  return (
    <>
      <div className={style.container}>
        <div className={style.images}>
          <img className={style.imgMin} src={productImgMin} alt="invida" />
          <img className={style.imgMax} src={productImgMax} alt="invida" />
        </div>
        <div>
          <div className={style.prodName}>
            <p>Кольє Інвіда</p>
            <p className={style.prodPrice}>10 500,00 грн</p>
          </div>
          <p className={style.inStock}>В наявності</p>
          <p className={style.colorName}>Колір: позолота</p>
          <div className={style.setColor}>
            <div className={style.firstColor} />
            <div className={style.secondColor} />
          </div>
          <p className={style.size}>Розмір:</p>
          <div className={style.selectSize}>
            <div className={style.sizeNumber}>
              <div className={style.sizeBox}>30</div>
              <div className={style.sizeBox}>40</div>
            </div>
            <div className={style.counter}>
              <button
                className={style.decCount}
                onClick={handleDecrementCounter}
              >
                -
              </button>
              <p className={style.count}>{counter}</p>
              <button
                className={style.inkCount}
                onClick={handleIncrementCounter}
              >
                +
              </button>
            </div>
          </div>
          <div className={style.buyBtn}>
            <button type="button" className={style.addBtn}>
              Додати до кошика
            </button>
            <button type="button" className={style.buyNow}>
              Купити зараз
            </button>
          </div>
          <p className={style.descrTitle}>Опис:</p>
          <p className={style.description}>
            Кольє з срібла з позолотою — це вишуканий та універсальний аксесуар,
            який додасть розкоші будь-якому образу. Ось загальна характеристика
            такого кольє:
            <br /> Матеріал: Кольє виготовлене з високоякісного срібла 925
            проби, на яке нанесено шар золота. Позолота може виконуватися
            різними способами, зокрема, методом електро- або хімічного
            осадження.
          </p>
          <div className={style.roll}>
            <p className={style.usageTitle}>Застосування:</p>
            <img src={arrow} alt="arrow" />
          </div>
          <div className={style.roll}>
            <p className={style.careTitle}>Догляд:</p>
            <img src={arrow} alt="arrow" />
          </div>
        </div>
      </div>
    </>
  );
};

export default ProductPage;
