 // Ensure this path is correct
import { BurgerMenu } from '../../components/BurgerMenu/BurgerMenu';
import { Logo } from '../../components/Logo/Logo';
import { Navigation } from '../../components/Navigation/Navigation';
import { Search } from '../../components/Search/Search';
import { useBasket } from '../../hooks/useBasket';
import { IconButton } from '../../components/UI/IconButton/IconButton';
import { PageContainer } from '../../components/containers/PageContainer';
import styles from './Header.module.scss';
import { SearchWindow } from '../../components/SearchWindow/SearchWindow';

export const Header = () => {
    const {openBasket, productQty} = useBasket()

    

    return (
        <header className={styles.header}>
            <PageContainer className={styles.container}>
                <BurgerMenu />
                <Logo className={styles.logo} />
                <Navigation />
                <div className={styles.control}>
                    <Search />
                    {/* <Cart onClose={handleCloseCart} isOpen={cartOpen} /> */}
                    <IconButton
                        className={styles.headerButton}
                        iconName='cart'
                        badgeValue={productQty}
                        onClick={openBasket}
                    />
                </div>
            </PageContainer>
            <SearchWindow/>
        </header>
    );
};

export default Header;
