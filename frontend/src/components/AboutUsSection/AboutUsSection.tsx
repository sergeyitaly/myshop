import { useEffect, useState } from 'react';
import styles from './AboutUsSection.module.scss';
import { Link } from 'react-router-dom';
import vase from './vase.png';
import { useTranslation } from 'react-i18next';
import i18next from 'i18next';

export const AboutUsSection = () => {
    const { t } = useTranslation();
    const [width, setWidth] = useState(window.innerWidth);
    useEffect(() => {
    }, [i18next.language]);

    useEffect(() => {
        const handleResize = () => {
            setWidth(window.innerWidth);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    let content = t('about_us_content');

    if (width < 515) {
        content = content.slice(0, 158);
    }

    return (
        <section className={styles.section} style={{ backgroundImage: `url(${vase})` }}>
            <div className={styles.content}>
                <span className={styles.blue}>KOLORYT</span>
                {content}
            </div>
            <Link to="/" className={styles.link}>
                {t('more_about_us')}
            </Link>
        </section>
    );
};
