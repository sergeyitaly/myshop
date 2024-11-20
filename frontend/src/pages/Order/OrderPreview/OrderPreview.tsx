import clsx from 'clsx'
import { useBasket } from '../../../hooks/useBasket'
import styles from './OrderPreview.module.scss'
import { formatPrice } from '../../../functions/formatPrice'
import { OrderItemCard } from '../../../components/Cards/OrderItemCard/OrderItemCard'
import { ROUTE } from '../../../constants'
import { Product } from '../../../models/entities'
import { useNavigate } from 'react-router-dom'
import {useTranslation} from "react-i18next";

interface OrderPreviewProps {
	className?: string;
}


export const OrderPreview = ({
    className
}: OrderPreviewProps) => {

    const navigate = useNavigate();
    const { t, i18n } = useTranslation();


    const { basketItems, totalPrice, deleteFromBasket, changeCounter} = useBasket()

    const handleClickCard = (product: Product) => {
        navigate(ROUTE.PRODUCT+product.id_name)
    }


    return (
        <div className={clsx(className, styles.container )}>
            <div className={styles.spaceBetween}>
                <h2 className={styles.text}>{t('order_preview')}</h2>
            </div>
            <div className={styles.content}>
            {
                basketItems.map(({product, qty}) => (
                    product &&
                    <OrderItemCard 
                        key={product.id}
                        product={product}
                        qty={qty}
                        language={i18n.language}
                        stock={product.stock}
                        onClickDelete={deleteFromBasket}
                        onChangeCounter={(val) => changeCounter(product, val)}
                        onClickName={handleClickCard}
                        onClickPhoto={handleClickCard}
                    />
                ))
            }

            </div>
            <div className={styles.spaceBetween}>
                <p className={styles.text}>{t('total_sum')}</p>
                <p className={styles.text}>{formatPrice(totalPrice, 'UAH')}</p>
            </div>
        </div>
    )
}
