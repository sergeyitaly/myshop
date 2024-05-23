import React, { useState } from "react"; // Make sure to import React
import styles from "./style.module.scss";
import image from "./Rectangle 88.svg";
import positiveIcon from "./+.svg";
import negativeIcon from "./Line 18.svg";

interface Product {
  id: number;
  name: string;
  material: string;
  price: number;
  quantity: number;
  imageUrl: string;
}

const CartModal: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const [cartItems] = useState<Product[]>([
    {
      id: 1,
      name: "Кольє Інвіда",
      material: "Срібло 925 проби ",
      price: 7500,
      quantity: 1,
      imageUrl: image,
    },
  ]);

  const total = cartItems.reduce((acc, item) => acc + item.price, 0);
  const [counter, setCounter] = useState(1);

  const handleDecrementCounter = () => {
    if (counter === 1) return;
    setCounter(counter - 1);
  };

  const handleIncrementCounter = () => {
    if (counter === 1) return;
    setCounter(counter + 1);
  };

  // const onToggleVisibility = () => {
  //     setIsVisible(!isVisible);
  // };
  // const onToggleVisibility1 = () => {
  //     setIsVisible1(!isVisible1);
  // };

  return (
    <div>
      <div className={styles.modalBackground}>
        <div className={styles.modalContent}>
          <div>
            <span className={styles.closeButton} onClick={onClose}>
              &times;
            </span>
            <h2> Корзина </h2>
            <ul>
              {cartItems.map((item) => (
                <li key={item.id}>
                  <div className={styles.cartItem}>
                    <div>
                      <img src={item.imageUrl} alt={item.name} />
                    </div>
                    <div>
                      <div>{item.name}</div>
                      <div>{item.material}</div>
                      <div className={styles.setColor}>
                        <div className={styles.firstColor} />
                        <div className={styles.secondColor} />
                      </div>
                      <div>
                        <p className={styles.size}>Розмір:</p>
                        <div className={styles.selectSize}>
                          <div className={styles.sizeNumber}>
                            <div className={styles.firstSizeBox}>30</div>
                            <div className={styles.secondSizeBox}>40</div>
                          </div>
                          <div className={styles.counter}>
                            <button
                              className={styles.decCount}
                              onClick={handleDecrementCounter}
                            >
                              <img src={negativeIcon} alt="-" />
                            </button>
                            <p className={styles.count}>{counter}</p>
                            <button
                              className={styles.inkCount}
                              onClick={handleIncrementCounter}
                            >
                              <img src={positiveIcon} alt="+" />
                            </button>
                          </div>
                        </div>
                      </div>
                      <p> В наявності </p>
                      <div>{item.price} грн.</div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p>Загальна вартість ${total}</p>
            <button className={styles.to_order}>Оформити замовлення</button>
          </div>
        </div>
      </div>
      <div>
        <p>Загальна вартість ${total}</p>
        <button className={styles.to_order}>Оформити замовлення</button>
      </div>
    </div>
  );
};

export default CartModal;
