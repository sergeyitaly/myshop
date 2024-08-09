import { ROUTE } from '../../constants';
import styles from './HeroSection.module.scss';
import Arrow from './arrow.svg';
import backgroundImage from './collection.jpg'
import { Link } from 'react-router-dom';

export const HeroSection = () => {
    return (
        <section className={styles.section}>
            <div className={styles.background} style={{ backgroundImage: `url(${backgroundImage})` }}></div>
            <div className={styles.content}>
                <h2 className={styles.title}>Koloryt -</h2>
                <p className={styles.description}>
                    місце, де кожен зможе знайти щось особливе для свого дому,
                    що відображатиме українську культуру та традиції.
                </p>
                <Link
                    className={styles.link}
                    to={ROUTE.PRODUCTS}
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
