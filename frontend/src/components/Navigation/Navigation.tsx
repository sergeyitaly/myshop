import { Link } from 'react-router-dom';
import { useLinks } from '../../utils/links';  // Ensure the path is correct
import styles from './Navigation.module.scss';

export const Navigation = () => {
  const links = useLinks();  // Call the function to get the links

  return (
    <nav className={styles.navigation}>
      {links.map(({ href, name }) => (
        <Link
          className={styles.link}
          key={href}  // Use href as the key to ensure uniqueness
          to={href}
        >
          {name}
        </Link>
      ))}
    </nav>
  );
};
