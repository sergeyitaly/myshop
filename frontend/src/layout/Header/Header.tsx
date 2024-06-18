 // Ensure this path is correct
import { BurgerMenu } from '../../components/BurgerMenu/BurgerMenu';
import { Logo } from '../../components/Logo/Logo';
import { Navigation } from '../../components/Navigation/Navigation';
import { Search } from '../../components/Search/Search';
import styles from './Header.module.scss';
import { HeaderIconButton } from './components/HeaderIconButton/HeaderIconButton';
import { useBasket } from '../../hooks/useBasket';

export const Header = () => {
    const {openBasket} = useBasket()

    

    return (
        <header className={styles.header}>
            <div className={styles.container}>
                <BurgerMenu />
                <Logo className={styles.logo} />
                <Navigation />
                <div className={styles.control}>
                    <Search />
                    {/* <Cart onClose={handleCloseCart} isOpen={cartOpen} /> */}
                    <HeaderIconButton
                        onClick={openBasket}
                    />
                </div>
            </div>
        </header>
    );
};

export default Header;
