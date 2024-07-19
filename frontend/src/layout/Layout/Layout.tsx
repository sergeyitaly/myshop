import { Outlet } from 'react-router-dom';
import { Footer } from '../Footer/Footer';
import { Header } from '../Header/Header';
import {CustomSeparator} from "../../components/Breadcrumbs/Breadcrumbs";
import { Basket } from '../../components/Basket/Basket';
import { AppSnackbar } from '../../components/Snackbar/Shackbar';
import { useBootstrap } from '../../hooks/useBootstrap';
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
   

    return (
        <>
            {withHeader && <Header basketLoadingStatus={isLoadingBasket}/>}
            <CustomSeparator
                // history={history}
            />
            <Outlet />
            {withFooter && <Footer />}
            {

            }
            <Basket />
            <AppSnackbar/>
        </>
    );
};
