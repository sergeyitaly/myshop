import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import styles from './BurgerMenu.module.scss';
import { links } from '../../utils/links';
import { Link } from '@tanstack/react-router';
export const BurgerMenu = () => {
    const [isOpen, setIsOpen] = useState(false);
    return (_jsxs("div", { className: styles.burger_container, children: [_jsxs("button", { className: [styles.burger, isOpen && styles.button_open].join(' '), onClick: () => setIsOpen((prev) => !prev), children: [_jsx("div", { className: styles.bar1 }), _jsx("div", { className: styles.bar2 }), _jsx("div", { className: styles.bar3 })] }), _jsxs("nav", { className: [styles.menu, isOpen && styles.menu_open].join(' '), children: [_jsxs("div", { className: styles.logo_container, children: [_jsx("h2", { className: styles.title, children: "Koloryt" }), _jsxs("button", { className: [
                                    styles.burger,
                                    isOpen && styles.button_open,
                                ].join(' '), onClick: () => setIsOpen((prev) => !prev), children: [_jsx("div", { className: styles.bar1 }), _jsx("div", { className: styles.bar2 }), _jsx("div", { className: styles.bar3 })] })] }), links.map(({ href, name }) => (_jsx(Link, { className: styles.link, to: href, children: name }, name)))] })] }));
};
