import LogoSVG from './logo.svg';
import styles from './Logo.module.scss';

export const Logo = ({ className }: { className?: string }) => {
    return (
        <div className={className !== undefined ? className : ''}>
            <img
                className={styles.logo}
                src={LogoSVG}
                alt="Koloryt Logo"
            />
        </div>
    );
};
