import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import styles from './AboutUsSection.module.scss';
import { Link } from '@tanstack/react-router';
export const AboutUsSection = () => {
    let content = " — це унікальний проект, створений командою з шести осіб, які об'єднали свою пристрасть до української культури та бажання просувати її через домашній декор. Магазин спеціалізується на продукції з українською тематикою, пропонуючи широкий асортимент товарів для дому, включаючи кераміку, скло та різноманітні аксесуари.";
    const [width, setWidth] = useState(window.innerWidth);
    if (width < 515) {
        content = content.slice(0, 158);
    }
    useEffect(() => {
        const handleResize = () => {
            setWidth(window.innerWidth);
        };
        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);
    return (_jsxs("section", { className: styles.section, children: [_jsxs("div", { className: styles.content, children: [_jsx("span", { className: styles.blue, children: "KOLORYT" }), content] }), _jsx(Link, { to: '/', className: styles.link, children: "\u0411\u0456\u043B\u044C\u0448\u0435 \u043F\u0440\u043E \u043D\u0430\u0441" })] }));
};
