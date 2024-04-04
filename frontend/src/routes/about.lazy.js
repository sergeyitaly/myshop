import { jsx as _jsx } from "react/jsx-runtime";
import { createLazyFileRoute } from '@tanstack/react-router';
export const Route = createLazyFileRoute('/about')({
    component: About,
});
function About() {
    return (_jsx("div", { children: _jsx("h3", { children: "Welcome About!" }) }));
}
