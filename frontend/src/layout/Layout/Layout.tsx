import { Outlet } from 'react-router-dom';
import { Footer } from '../Footer/Footer';
import { Header } from '../Header/Header';
import {CustomSeparator} from "../../components/Navigation/Breadcrumbs";
// import { useHistory } from 'react-router-dom';

export const Layout = ({
    withHeader,
    withFooter,
}: {
    withHeader: boolean;
    withFooter: boolean;
}) => {
    // const history = useHistory();


    return (
        <>
            {withHeader && <Header />}
            <CustomSeparator
                // history={history}
            />
            <Outlet />
            {withFooter && <Footer />}
        </>
    );
};
