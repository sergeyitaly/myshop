import { Link } from '@tanstack/react-router';
import styles from './HeroSection.module.scss';
import Arrow from './arrow.svg';

export const HeroSection = () => {
    return (
        <section className={styles.section}>
            <div className={styles.content}>
            <h2 className={styles.title}>Koloryt -</h2>
            <p className={styles.description}>
                місце, де кожен зможе знайти щось особливе для свого дому, що
                відображатиме українську культуру та традиції.
            </p>
            <Link
                className={styles.link}
                to="/"
            >
                Дивитися всі товари{' '}
                <img
                    src={Arrow}
                    alt="arrow icon"
                />
            </Link>
            </div>
           
        </section>
    );
};
