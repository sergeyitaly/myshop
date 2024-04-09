import { BurgerMenu } from '../../components/BurgerMenu/BurgerMenu';
import { Cart } from '../../components/Cart/Cart';
import { Logo } from '../../components/Logo/Logo';
import { Navigation } from '../../components/Navigation/Navigation';
import { Search } from '../../components/Search/Search';
import styles from './Header.module.scss';

export const Header = () => {
    return (
        <header className={styles.header}>
            <div className={styles.container}>
                <BurgerMenu />
                <Logo />
                <Navigation />
                <Search />
                <Cart />
            </div>
        </header>
    );
};