import styles from './Cart.module.scss';
import CartSVG from './cart.svg';

export const Cart = () => {
    return (
        <button className={styles.button}>
            <img
                className={styles.icon}
                src={CartSVG}
                alt="Cart icon"
            />
        </button>
    );
};
