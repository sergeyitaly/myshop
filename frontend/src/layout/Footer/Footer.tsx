import { Link } from '@tanstack/react-router';
import styles from './Footer.module.scss';
import VisaImg from './visa.svg';

export const Footer = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.content}>
                <nav className={styles.nav}>
                    <p className={styles.title}>Зв’язатись з нами</p>
                    <Link
                        className={styles.link}
                        to="/"
                    >
                        Контакти
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
                    <p className={styles.title}>Інфо</p>
                    <Link
                        className={styles.link}
                        to="/"
                    >
                        Про нас
                    </Link>
                    <Link
                        className={styles.link}
                        to="/"
                    >
                        Оплата і доставка
                    </Link>
                    <Link
                        className={styles.link}
                        to="/"
                    >
                        Повернення & Відшкодування
                    </Link>
                </nav>
                <nav className={styles.nav}>
                    <p>
                        2024 <span className={styles.koloryt}>KOLORYT</span>
                    </p>
                    <Link
                        className={styles.link}
                        to="/"
                    >
                        Політика конфіденційності
                    </Link>
                    <p className={styles.payment}>
                        Оплата:
                        <img
                            src={VisaImg}
                            alt="visa icon"
                        />
                    </p>
                </nav>
            </div>
        </footer>
    );
};
