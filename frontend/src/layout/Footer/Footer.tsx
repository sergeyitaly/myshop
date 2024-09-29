import { Link } from 'react-router-dom';
import styles from './Footer.module.scss';
import VisaImg from './visa.svg';
import { Logo } from '../../components/Logo/Logo';
import { useTranslation } from 'react-i18next'; // Import the useTranslation hook
import { LanguageDropDown } from './LanguageDropDown/LanguageDropDown';

export const Footer = () => {
    const { t } = useTranslation(); // Initialize translation hook


    return (
        <footer className={styles.footer}>
            <Logo 
                className={styles.logo}    
                type='short'
            />
            <div className={styles.content}>
                <nav className={styles.nav}>
                    <p className={styles.title}>{t('contact_us')}</p> {/* Localized text */}
                    <Link
                        className={styles.link}
                        to="/contacts"
                    >
                        {t('contacts')}
                    </Link>
                    <Link
                        className={styles.link}
                        to="/"
                    >
                        Instagram
                    </Link>
                    <Link
                        className={styles.link}
                        to="/"
                    >
                        Facebook
                    </Link>
                </nav>
                <nav className={styles.nav}>
                    <p className={styles.title}>{t('info')}</p> {/* Localized text */}
                    <Link
                        className={styles.link}
                        to="/about"
                    >
                        {t('about_us')}
                    </Link>
                    <Link
                        className={styles.link}
                        to="/payment_delivery"
                    >
                        {t('payment_delivery')}
                    </Link>
                    <Link
                        className={styles.link}
                        to="/"
                    >
                        {t('returns_refunds')}
                    </Link>
                </nav>
                <nav className={styles.nav}>
                    <p>
                        2024 <span className={styles.koloryt}>KOLORYT</span>
                    </p>
                    <Link
                        className={styles.link}
                        to="/privacy_policy"
                    >
                        {t('privacy_policy')}
                    </Link>
                    <p className={styles.payment}>
                        {t('payment')}: {/* Localized text */}
                        <img
                            src={VisaImg}
                            alt="visa icon"
                        />
                    </p>
                    <LanguageDropDown/>
                </nav>
            </div>
        </footer>
    );
};
