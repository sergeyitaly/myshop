import { Outlet, useLocation } from 'react-router-dom';
import { Footer } from '../Footer/Footer';
import { Header } from '../Header/Header';
import { Basket } from '../../components/Basket/Basket';
import { AppSnackbar } from '../../components/Snackbar/Shackbar';
import { useBootstrap } from '../../hooks/useBootstrap';
import { useEffect } from 'react';
import { Breadcrumbs } from '../Breadcrumbs/Breadcrumbs';
import { useTranslation } from 'react-i18next';
import { STORAGE } from '../../constants';
import { InfoButton } from '../../components/InfoButton/InfoButton';
import styles from './Layout.module.scss'
import { useToggler } from '../../hooks/useToggler';
import { InfoModal } from '../InfoModal/InfoModal';
// import { useHistory } from 'react-router-dom';

export const Layout = () => {

    const {isLoadingBasket} = useBootstrap()
    const {openStatus, handleOpen, handleClose} = useToggler()

    const location = useLocation()

    const {i18n} = useTranslation()

    useEffect(() => {
       const savedLanguage = localStorage.getItem(STORAGE.LANGUAGE) 
       savedLanguage && i18n.changeLanguage(savedLanguage)
    }, [])
    
    useEffect(() => {
        handleOpen()
    }, [])


    useEffect(() => {
        window.scrollTo({top: 0, left: 0, behavior: 'smooth'})
    }, [location.pathname]) 
   
    const withHeader = true
    const withFooter = true

    return (
        <>
            {withHeader && <Header basketLoadingStatus={isLoadingBasket}/>}
            <Breadcrumbs/>
            <Outlet />
            {withFooter && <Footer />}
            {
                openStatus &&
                <InfoModal
                    onClose={handleClose}
                />
            }
            <Basket />
            <InfoButton
                className={styles.infoButton}
                onClick={handleOpen}
            />
            <AppSnackbar/>
        </>
    );
};
