import { Outlet, useLocation } from 'react-router-dom';
import { Footer } from '../Footer/Footer';
import { Header } from '../Header/Header';
import { Basket } from '../../components/Basket/Basket';
import { AppSnackbar } from '../../components/Snackbar/Shackbar';
import { useBootstrap } from '../../hooks/useBootstrap';
import { useEffect } from 'react';
import { Breadcrumbs } from '../Breadcrumbs/Breadcrumbs';
// import { useHistory } from 'react-router-dom';

export const Layout = ({
    withHeader,
    withFooter,
}: {
    withHeader: boolean;
    withFooter: boolean;
}) => {
    // const history = useHistory();

    const {isLoadingBasket} = useBootstrap()

    const location = useLocation()

    useEffect(() => {
        window.scrollTo({top: 0, left: 0, behavior: 'smooth'})
    }, [location.pathname]) 
   

    return (
        <>
            {withHeader && <Header basketLoadingStatus={isLoadingBasket}/>}
            <Breadcrumbs/>
            <Outlet />
            {withFooter && <Footer />}
            {

            }
            <Basket />
            <AppSnackbar/>
        </>
    );
};
