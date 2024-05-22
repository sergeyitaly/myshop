// Cart.tsx
import React from 'react';
import styles from './Cart.module.scss';
import image from './Rectangle 88.svg';

interface Product {
    id: number;
    name: string;
    material: string;
    price: number;
    quantity: number;
    imageUrl: string;
}

interface CartProps {
    onClose: () => void;
    isOpen: boolean;
}

const Cart: React.FC<CartProps> = ({ onClose, isOpen }) => {
    const [cartItems] = React.useState<Product[]>([
        {
            id: 1,
            name: 'Кольє Інвіда',
            material: 'Срібло 925 проби',
            price: 7500,
            quantity: 1,
            imageUrl: image,
        },
    ]);

    const total = cartItems.reduce((acc, item) => acc + item.price, 0);
    const [counter, setCounter] = React.useState(1);

    if (!isOpen) return null;

    return (
        <div className={styles.modalBackground}>
            <div className={styles.modalContent}>
                <div>
                    <span className={styles.closeButton} onClick={onClose}>
                        &times;
                    </span>
                    <h2>Корзина</h2>
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
                                                        onClick={() => setCounter(counter - 1)}
                                                    >
                                                        -
                                                    </button>
                                                    <p className={styles.count}>{counter}</p>
                                                    <button
                                                        className={styles.inkCount}
                                                        onClick={() => setCounter(counter + 1)}
                                                    >
                                                        +
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                        <p>В наявності</p>
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
    );
};

export default Cart;
