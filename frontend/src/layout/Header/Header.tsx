// Header.tsx
import { useState } from 'react';
import Cart from '../../components/Cart/Cart'; // Ensure this path is correct
import { BurgerMenu } from '../../components/BurgerMenu/BurgerMenu';
import { Logo } from '../../components/Logo/Logo';
import { Navigation } from '../../components/Navigation/Navigation';
import { Search } from '../../components/Search/Search';
import styles from './Header.module.scss';

export const Header = () => {
    const [cartOpen, setCartOpen] = useState(false);

    const handleCloseCart = () => {
        setCartOpen(false);
    };

    return (
        <header className={styles.header}>
            <div className={styles.container}>
                <BurgerMenu />
                <Logo className={styles.logo} />
                <Navigation />
                <Search />
                <Cart onClose={handleCloseCart} isOpen={cartOpen} />
            </div>
        </header>
    );
};

export default Header;
