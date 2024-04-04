import { jsx as _jsx } from "react/jsx-runtime";
import SearchSVG from './search.svg';
import styles from './Search.module.scss';
export const Search = () => {
    return (_jsx("button", { className: styles.button, children: _jsx("img", { className: styles.icon, src: SearchSVG, alt: "search icon" }) }));
};
