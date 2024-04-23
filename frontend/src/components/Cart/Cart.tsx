import styles from './Cart.module.scss';
import CartSVG from './cart.svg';
import {useState} from "react";
import CartModal from "./CartComponent";

export const Cart = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleButtonClick = () => {
        setIsModalOpen(true)
    }

    const closeModal = () => {
      setIsModalOpen(false)
    }

    return (
        <>
            <button className={styles.button}
            onClick={handleButtonClick}>
                <img
                    className={styles.icon}
                    src={CartSVG}
                    alt="Cart icon"
                />
            </button>
            {isModalOpen && <CartModal onClose={closeModal} />}
        </>

    );
};
