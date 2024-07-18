 // Ensure this path is correct
import { BurgerMenu } from '../../components/BurgerMenu/BurgerMenu';
import { Logo } from '../../components/Logo/Logo';
import { Navigation } from '../../components/Navigation/Navigation';
import { useBasket } from '../../hooks/useBasket';
import { IconButton } from '../../components/UI/IconButton/IconButton';
import { PageContainer } from '../../components/containers/PageContainer';
import styles from './Header.module.scss';
import { SearchWindow } from '../../components/SearchWindow/SearchWindow';
import { useSearch } from '../../hooks/useSearch';
import { useNavigate } from 'react-router-dom';
import { ROUTE } from '../../constants';
import { Product } from '../../models/entities';
import { AnimatePresence } from 'framer-motion';



export const Header = () => {
    const {openBasket, isLoading, productQty} = useBasket()

    const {open, value, debounceValue, toggleSearchBar, handleChange, closeSearchBar} = useSearch()

    const navigate = useNavigate()

    const handleClickProduct = (product: Product) => {
        navigate(`${ROUTE.PRODUCT}${product.id}`)
        closeSearchBar()
    }

    return (
        <header className={styles.header}>
            <PageContainer className={styles.container}>
                <BurgerMenu />
                <Logo className={styles.logo} />
                <Navigation />
                <div className={styles.control}>
                    <IconButton
                        className={styles.headerButton}
                        iconName='search' 
                        onClick={toggleSearchBar}
                    />
                    {/* <Cart onClose={handleCloseCart} isOpen={cartOpen} /> */}
                    <IconButton
                        disabled = {isLoading}
                        className={styles.headerButton}
                        iconName='cart'
                        badgeValue={productQty}
                        onClick={openBasket}
                    />
                </div>
            </PageContainer>
            <AnimatePresence>
                {
                    open &&    
                    <SearchWindow
                        value={value}
                        queryText={debounceValue}
                        onChange={handleChange}
                        onClickClose={closeSearchBar}
                        onClickProduct={handleClickProduct}
                    />
                }
            </AnimatePresence>
        </header>
    );
};

export default Header;
