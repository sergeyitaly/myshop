import { jsx as _jsx } from "react/jsx-runtime";
import { Link } from '@tanstack/react-router';
import styles from './Navigation.module.scss';
import { links } from '../../utils/links';
export const Navigation = () => {
    return (_jsx("nav", { className: styles.navigation, children: links.map(({ href, name }) => (_jsx(Link, { className: styles.link, to: href, children: name }, name))) }));
};
