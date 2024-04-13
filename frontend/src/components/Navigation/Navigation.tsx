import styles from './Navigation.module.scss';
import { links } from '../../utils/links';
import {Link} from 'react-router-dom';


export const Navigation = () => {

    return (
        <nav className={styles.navigation}>
            {links.map(({ href, name }) => (
                <Link
                    className={styles.link}
                    key={name}
                    to={href}
                >
                    {name}
                </Link>
            ))}
        </nav>
    );
};
