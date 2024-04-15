import styles from './not-found.module.scss';
import Img404 from './404 error.png';

export const NotFound = () => {
    return (
        <main className={styles.main}>
            <img
                className={styles.img}
                src={Img404}
                alt="404"
            />
            <h2 className={styles.message}>Opps ця сторінка не знайдена</h2>
            <a className={styles.link}>Повернутися на голову сторінку</a>
        </main>
    );
};
