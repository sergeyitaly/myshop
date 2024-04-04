import LogoSVG from './logo.svg';
import styles from './Logo.module.scss';
import { Link } from 'react-router-dom';

export const Logo = ({ className }: { className?: string }) => {
    return (
        <div className={className !== undefined ? className : ''}>
            <Link to={'/'}>
                <img
                    className={styles.logo}
                    src={LogoSVG}
                    alt="Koloryt Logo"
                />
            </Link>
        </div>
    );
};
