import SearchSVG from './search.svg';
import styles from './Search.module.scss';

export const Search = () => {
    return (
        <button className={styles.button}>
            <img
                className={styles.icon}
                src={SearchSVG}
                alt="search icon"
            />
        </button>
    );
};
