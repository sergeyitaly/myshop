import styles from './not-found.module.scss';
import Img404 from './404 error.png';
import { useTranslation } from 'react-i18next'; // Import the useTranslation hook
import { Link as RouterLink } from 'react-router-dom'; // Import RouterLink for navigation

export const NotFound = () => {
    const { t } = useTranslation(); // Initialize translation hook

    return (
        <main className={styles.main}>
            <img
                className={styles.img}
                src={Img404}
                alt="404"
            />
            <h2 className={styles.message}>{t('not_found_message')}</h2>
            <RouterLink to="/" className={styles.link}>
                {t('return_to_home')}
            </RouterLink>
        </main>
    );
};
