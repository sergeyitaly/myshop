import { useRef, useState } from 'react';
import styles from './BurgerMenu.module.scss';
import { Link } from 'react-router-dom';
import useBlockScroll from '../../hooks/useBlockScroll';
import useClickOutside from '../../hooks/useClickOutside';

const links = [
    { name: 'Колекції', href: '/collections' },
    { name: 'Нові надходження', href: '/*' },
    { name: 'Всі колекції', href: '/*' },
    { name: 'Знижки', href: '/*' },
    { name: 'Про нас', href: '/*' },
    { name: 'Контакти', href: '/*' },
];

export const BurgerMenu = () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const ref = useRef<HTMLDivElement>(null);

    useBlockScroll(isOpen);
    useClickOutside(ref, () => setIsOpen(false));

    return (
        <div className={styles.burger_container}>
            <button
                className={[styles.burger, isOpen && styles.button_open].join(
                    ' '
                )}
                onClick={() => setIsOpen((prev) => !prev)}
            >
                <div className={styles.bar1}></div>
                <div className={styles.bar2}></div>
                <div className={styles.bar3}></div>
            </button>

            <nav
                ref={ref}
                className={[styles.menu, isOpen && styles.menu_open].join(' ')}
            >
                <div className={styles.logo_container}>
                    <button
                        className={[
                            styles.burger,
                            isOpen && styles.button_open,
                        ].join(' ')}
                        onClick={() => setIsOpen((prev) => !prev)}
                    >
                        <div className={styles.bar1}></div>
                        <div className={styles.bar2}></div>
                        <div className={styles.bar3}></div>
                    </button>
                </div>

                {links.map(({ href, name }) => (
                    <Link
                        key={name}
                        className={styles.link}
                        to={href}
                        onClick={() => setIsOpen((prev) => !prev)}
                    >
                        {name}
                    </Link>
                ))}
            </nav>
        </div>
    );
};
