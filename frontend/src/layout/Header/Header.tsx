import { useState } from 'react'; // Import useState for managing dropdown state
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
import { useTranslation } from 'react-i18next'; // Import the hook for translations

interface HeaderProps {
    basketLoadingStatus: boolean
}

export const Header = ({
    basketLoadingStatus
}: HeaderProps) => {
    const [isDropdownOpen, setDropdownOpen] = useState(false); // State for dropdown
    const { openBasket, productQty } = useBasket();
    const { open, value, debounceValue, toggleSearchBar, handleChange, closeSearchBar } = useSearch();
    const navigate = useNavigate();
    const { i18n } = useTranslation(); // Use the useTranslation hook

    const handleClickProduct = (product: Product) => {
        navigate(`${ROUTE.PRODUCT}${product.id}`);
        closeSearchBar();
    };

    const handleLanguageChange = (lang: string) => {
        i18n.changeLanguage(lang); // Change the language
        setDropdownOpen(false); // Close dropdown after selection
    };

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
                    <IconButton
                        disabled={basketLoadingStatus}
                        className={styles.headerButton}
                        iconName='cart'
                        badgeValue={productQty}
                        onClick={openBasket}
                    />
                    {/* Language Switcher Dropdown */}
                    <div className={styles.languageSwitcher}>
                        <button 
                            className={styles.dropdownButton} 
                            onClick={() => setDropdownOpen(!isDropdownOpen)}
                        >
                            {i18n.language === 'en' ? 'EN' : 'UK'}
                        </button>
                        {isDropdownOpen && (
                            <div className={styles.dropdownMenu}>
                                <button onClick={() => handleLanguageChange('en')}>EN</button>
                                <button onClick={() => handleLanguageChange('uk')}>UK</button>
                            </div>
                        )}
                    </div>
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
