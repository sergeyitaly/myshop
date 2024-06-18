import { AppIcon } from "../../../SvgIconComponents/AppIcon"
import styles from './EmptyBasket.module.scss'

export const EmptyBasket = () => {
    return (
        <div className={styles.container}>
            <AppIcon iconName="vase"/>
            <p>Ваш кошик порожній</p>
        </div>
    )
}