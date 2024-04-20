import { useState } from "react";
import productImgMin from "../../assets/collection/Rectangle 63.svg";
import productImgMax from "../../assets/collection/Rectangle 45.svg";
import ringQueen from "../../assets/collection/Rectangle 48.svg";
import braceletQueen from "../../assets/collection/Rectangle 69.svg";
import ringsSet from "../../assets/collection/Rectangle 70.svg";
import earrings from "../../assets/collection/Rectangle 71.svg";
import arrowBottom from "./icons/fluent_ios-arrow-24-regular.svg";
import arrowUp from "./icons/arrow-Up.svg";
import negativeIcon from "./icons/-.svg";
import positiveIcon from "./icons/+.svg";
import style from "./ProductPage.module.scss";

const ProductPage = () => {
  const [counter, setCounter] = useState(1);
  const [isVisible, setIsVisible] = useState(false);

  const handleIncrementCounter = () => {
    setCounter(counter + 1);
  };

  const handleDecrementCounter = () => {
    if (counter === 1) return;
    setCounter(counter - 1);
  };

  const onToggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  return (
    <>
      <div className={style.container}>
        <div className={style.images}>
          <img className={style.imgMin} src={productImgMin} alt="invida" />
          <img className={style.imgMax} src={productImgMax} alt="invida" />
        </div>
        <div>
          <div className={style.priceTitle}>
            <div className={style.prodTitle}>
              <p className={style.prodName}>Кольє Інвіда</p>
              <p className={style.prodPrice}>10 500,00 грн</p>
            </div>
            <p className={style.inStock}>В наявності</p>
          </div>
          <p className={style.colorName}>Колір: позолота</p>
          <div className={style.setColor}>
            <div className={style.firstColor} />
            <div className={style.secondColor} />
          </div>
          <p className={style.size}>Розмір:</p>
          <div className={style.selectSize}>
            <div className={style.sizeNumber}>
              <div className={style.firstSizeBox}>30</div>
              <div className={style.secondSizeBox}>40</div>
            </div>
            <div className={style.counter}>
              <button
                className={style.decCount}
                onClick={handleDecrementCounter}
              >
                <img
                  className={style.negativeIcon}
                  src={negativeIcon}
                  alt="-"
                />
              </button>
              <p className={style.count}>{counter}</p>
              <button
                className={style.inkCount}
                onClick={handleIncrementCounter}
              >
                <img
                  className={style.positiveIcon}
                  src={positiveIcon}
                  alt="+"
                />
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
          <p className={style.title}>Опис:</p>
          <p className={style.description}>
            Кольє з срібла з позолотою — це вишуканий та універсальний аксесуар,
            який додасть розкоші будь-якому образу. Ось загальна характеристика
            такого кольє:
            <br /> Матеріал: Кольє виготовлене з високоякісного срібла 925
            проби, на яке нанесено шар золота. Позолота може виконуватися
            різними способами, зокрема, методом електро- або хімічного
            осадження.
          </p>

          <div className={isVisible ? `${style.noBorder}` : `${style.roll}`}>
            <p className={isVisible ? `${style.title}` : `${style.titleRoll}`}>
              Застосування:
            </p>

            <button
              onClick={onToggleVisibility}
              className={style.arrBtn}
              type="button"
            >
              {isVisible ? (
                <img src={arrowUp} alt="arrow" />
              ) : (
                <img src={arrowBottom} alt="arrow" />
              )}
            </button>
          </div>

          {isVisible && (
            <div className={style.boxUsageDescr}>
              <p className={style.usageDescr}>
                Підходить для повсякденного носіння, а також стане чудовим
                доповненням до вечірнього або урочистого вбрання.
              </p>
            </div>
          )}
          <div className={isVisible ? `${style.noBorder}` : `${style.roll}`}>
            <p className={style.title}>Догляд:</p>

            <button
              onClick={onToggleVisibility}
              className={style.arrBtn}
              type="button"
            >
              {isVisible ? (
                <img src={arrowUp} alt="arrow" />
              ) : (
                <img src={arrowBottom} alt="arrow" />
              )}
            </button>
          </div>
          {isVisible && (
            <div className={style.boxCareDescr}>
              <p className={style.careDescr}>
                Чистка: Використовуйте м'яку тканину або спеціалізований розчин
                для чищення срібла. Не використовуйте абразивні засоби, оскільки
                вони можуть пошкодити покриття. <br />
                <br />
                Зберігання: Зберігайте кольє окремо від інших ювелірних виробів,
                щоб уникнути подряпин. Використовуйте м'яку тканинну сумочку або
                коробку з м'яким покриттям. Уникайте контакту з хімікатами: Не
                допускайте контакту кольє з парфумами, косметикою, миючими
                засобами та іншими хімікатами, які можуть пошкодити позолоту.
                <br />
                <br />
                Носіння: Намагайтеся надягати кольє після того, як ви нанесли
                косметику та парфуми, та знімати перед купанням, спортом або
                сном. Дотримуючись цих рекомендацій, ви зможете довше зберігати
                красу та блиск вашого кольє з срібла з позолотою.
              </p>
            </div>
          )}
        </div>
      </div>
      <div className={style.collectionContainer}>
        <p className={style.collectionTitle}>Також з цієї колекції</p>
        <ul className={style.collectionList}>
          <li>
            <img className={style.collectionImg} src={ringQueen} />
            <p className={style.collectionItemName}>Каблучка Queen</p>
            <p className={style.collectionItemPrice}>7 300,00 грн</p>
          </li>
          <li>
            <img
              className={style.collectionImg}
              src={braceletQueen}
              alt="bracelet"
            />
            <p className={style.collectionItemName}>Браслет Oueen</p>
            <p className={style.collectionItemPrice}>8 300,00 грн.</p>
          </li>
          <li>
            <img className={style.collectionImg} src={ringsSet} alt="rings" />
            <p className={style.collectionItemName}>Сет з каблучок</p>
            <p className={style.collectionItemPrice}>10 300,00 грн.</p>
          </li>
          <li>
            <img
              className={style.collectionImg}
              src={earrings}
              alt="earrings"
            />
            <p className={style.collectionItemName}>Сережки з цитрином</p>
            <p className={style.collectionItemPrice}>5 600,00 грн</p>
          </li>
        </ul>
      </div>
    </>
  );
};

export default ProductPage;
