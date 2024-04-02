import { createRootRoute, Outlet } from '@tanstack/react-router';
import { Footer } from '../layout/Footer/Footer';
import { Header } from '../layout/Header/Header';

export const Route = createRootRoute({
    component: () => (
        <>
            <Header />
            <Outlet />
            <Footer />
        </>
    ),
});
