import { jsx as _jsx } from "react/jsx-runtime";
import styles from './Cart.module.scss';
import CartSVG from './cart.svg';
export const Cart = () => {
    return (_jsx("button", { className: styles.button, children: _jsx("img", { className: styles.icon, src: CartSVG, alt: "Cart icon" }) }));
};
