import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { createRootRoute, Outlet } from '@tanstack/react-router';
import { Footer } from '../layout/Footer/Footer';
import { Header } from '../layout/Header/Header';
export const Route = createRootRoute({
    component: () => (_jsxs(_Fragment, { children: [_jsx(Header, {}), _jsx(Outlet, {}), _jsx(Footer, {})] })),
});
