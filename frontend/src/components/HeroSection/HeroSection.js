import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Link } from '@tanstack/react-router';
import styles from './HeroSection.module.scss';
import Arrow from './arrow.svg';
export const HeroSection = () => {
    return (_jsx("section", { className: styles.section, children: _jsxs("div", { className: styles.content, children: [_jsx("h2", { className: styles.title, children: "Koloryt -" }), _jsx("p", { className: styles.description, children: "\u043C\u0456\u0441\u0446\u0435, \u0434\u0435 \u043A\u043E\u0436\u0435\u043D \u0437\u043C\u043E\u0436\u0435 \u0437\u043D\u0430\u0439\u0442\u0438 \u0449\u043E\u0441\u044C \u043E\u0441\u043E\u0431\u043B\u0438\u0432\u0435 \u0434\u043B\u044F \u0441\u0432\u043E\u0433\u043E \u0434\u043E\u043C\u0443, \u0449\u043E \u0432\u0456\u0434\u043E\u0431\u0440\u0430\u0436\u0430\u0442\u0438\u043C\u0435 \u0443\u043A\u0440\u0430\u0457\u043D\u0441\u044C\u043A\u0443 \u043A\u0443\u043B\u044C\u0442\u0443\u0440\u0443 \u0442\u0430 \u0442\u0440\u0430\u0434\u0438\u0446\u0456\u0457." }), _jsxs(Link, { className: styles.link, to: "/", children: ["\u0414\u0438\u0432\u0438\u0442\u0438\u0441\u044F \u0432\u0441\u0456 \u0442\u043E\u0432\u0430\u0440\u0438", ' ', _jsx("img", { src: Arrow, alt: "arrow icon" })] })] }) }));
};
