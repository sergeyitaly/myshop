import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BurgerMenu } from '../../components/BurgerMenu/BurgerMenu';
import { Cart } from '../../components/Cart/Cart';
import { Logo } from '../../components/Logo/Logo';
import { Navigation } from '../../components/Navigation/Navigation';
import { Search } from '../../components/Search/Search';
import styles from './Header.module.scss';
export const Header = () => {
    return (_jsx("header", { className: styles.header, children: _jsxs("div", { className: styles.container, children: [_jsx(BurgerMenu, {}), _jsx(Logo, { className: styles.logo }), _jsx(Navigation, {}), _jsx(Search, {}), _jsx(Cart, {})] }) }));
};
