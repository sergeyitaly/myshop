import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { AboutUsSection } from "../components/AboutUsSection/AboutUsSection";
import { HeroSection } from "../components/HeroSection/HeroSection";
import styles from "./home.module.scss";
export const Home = () => {
    return (_jsxs("main", { className: styles.main, children: [_jsx(HeroSection, {}), _jsx(AboutUsSection, {})] }));
};
