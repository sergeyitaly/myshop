import { useEffect, useState } from 'react';
import styles from './AboutUsSection.module.scss';
import { Link } from 'react-router-dom';
import vase from './vase.jpg'
import { useTranslation } from 'react-i18next';

export const AboutUsSection = () => {
    const { t } = useTranslation();

    let content =
        " — це унікальний проект, створений командою з шести осіб, які об'єднали свою пристрасть до української культури та бажання просувати її через домашній декор. Магазин спеціалізується на продукції з українською тематикою, пропонуючи широкий асортимент товарів для дому, включаючи кераміку, скло та різноманітні аксесуари.";
    const [width, setWidth] = useState(window.innerWidth);

    if (width < 515) {
        content = content.slice(0, 158);
    }

    useEffect(() => {
        const handleResize = () => {
            setWidth(window.innerWidth);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    return (
        <section className={styles.section} style={{ backgroundImage: `url(${vase})` }}>
            <div className={styles.content}>
                <span className={styles.blue}>KOLORYT</span>
                {content}
            </div>
            <Link
                to="/"
                className={styles.link}
            >
              {t('More about us')}
            </Link>
        </section>
    );
};
