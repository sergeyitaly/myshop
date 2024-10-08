import { ROUTE } from '../../constants';
import styles from './HeroSection.module.scss';
import Arrow from './arrow.svg';
import backgroundImage from './collection.jpg';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next'; // Import the useTranslation hook
import { PageContainer } from '../containers/PageContainer';

export const HeroSection = () => {
    const { t } = useTranslation(); // Initialize translation hook

    return (
        <section className={styles.section}>
            <PageContainer className={styles.container}>
                {/* <div className={styles.background} style={{ backgroundImage: `url(${backgroundImage})` }}></div> */}
                <div className={styles.imageContainer}>
                    <img  src={backgroundImage} alt="" />
                </div>
                <div className={styles.content}>
                    <h2 className={styles.title}>Koloryt -</h2>
                    <p className={styles.description}>
                        {t("heroDescription")} {/* Localized text */}
                    </p>
                    <Link
                        className={styles.link}
                        to={ROUTE.PRODUCTS}
                    >
                        {t("viewAllProducts")} {/* Localized text */}
                        <img
                            src={Arrow}
                            alt={t("arrowIcon")} // Localized alt text
                        />
                    </Link>
                </div>
            </PageContainer>
        </section>
    );
};
