import { useEffect, useState } from 'react';
import styles from './AboutUsSection.module.scss';
import { Link } from '@tanstack/react-router';

export const AboutUsSection = () => {
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
        <section className={styles.section}>
            <div className={styles.content}>
                <span className={styles.blue}>KOLORYT</span>
                {content}
            </div>
            <Link to='/' className={styles.link}>Більше про нас</Link>
        </section>
    );
};
