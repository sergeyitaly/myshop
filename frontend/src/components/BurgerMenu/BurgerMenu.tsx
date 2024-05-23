// BurgerMenu.tsx
import { useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './BurgerMenu.module.scss';
import useBlockScroll from '../../hooks/useBlockScroll';
import useClickOutside from '../../hooks/useClickOutside';

const links = [
    { name: 'Колекції', href: '/collections' },
    { name: 'Нові надходження', href: '/new-arrivals' },
    { name: 'Всі колекції', href: '/all-collections' },
    { name: 'Знижки', href: '/discounts' },
    { name: 'Про нас', href: '/about' },
    { name: 'Контакти', href: '/contact' },
    { name: 'Замовлення', href: '/order' },
];

export const BurgerMenu = () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const ref = useRef<HTMLDivElement>(null);

    useBlockScroll(isOpen);
    useClickOutside(ref, () => setIsOpen(false));

    return (
        <div className={styles.burger_container}>
            <button
                className={[styles.burger, isOpen && styles.button_open].join(' ')}
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
                        className={[styles.burger, isOpen && styles.button_open].join(' ')}
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
                        onClick={() => setIsOpen(false)}
                    >
                        {name}
                    </Link>
                ))}
            </nav>
        </div>
    );
};
