import SearchSVG from './search.svg';
import styles from './Search.module.scss';
import { ButtonHTMLAttributes, DetailedHTMLProps } from 'react';

interface SearchProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {

}

export const Search = ({
    ...props
}: SearchProps) => {
    return (
        <button className={styles.button} {...props}>
            <img
                className={styles.icon}
                src={SearchSVG}
                alt="search icon"
            />
        </button>
    );
};
