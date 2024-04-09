import { jsx as _jsx } from "react/jsx-runtime";
import LogoSVG from './logo.svg';

import styles from './Logo.module.scss';
export const Logo = ({ className }) => {
    return (_jsx("div", { className: className !== undefined ? className : '', children: _jsx("img", { className: styles.logo, src: LogoSVG, alt: "Koloryt Logo" }) }));
};
