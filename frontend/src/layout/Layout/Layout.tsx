import { Outlet } from 'react-router-dom';
import { Footer } from '../Footer/Footer';
import { Header } from '../Header/Header';

export const Layout = ({
    withHeader,
    withFooter,
}: {
    withHeader: boolean;
    withFooter: boolean;
}) => {
    return (
        <>
            {withHeader && <Header />}
            <Outlet />
            {withFooter && <Footer />}
        </>
    );
};
