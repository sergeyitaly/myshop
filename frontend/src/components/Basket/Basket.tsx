import { useEffect, useRef } from 'react'
import styles from './Basket.module.scss'
import { useBasket } from '../../hooks/useBasket'
import useClickOutside from '../../hooks/useClickOutside'
import { MainButton } from '../UI/MainButton/MainButton'
import { AppIcon } from '../SvgIconComponents/AppIcon'
import { EmptyBasket } from './components/EmptyBasket/EmptyBasket'
import clsx from 'clsx'
import { useNavigate } from 'react-router-dom'
import { ROUTE } from '../../constants'
import { formatNumber } from '../../functions/formatNumber'
import { BasketItem } from '../Cards/BasketItem/BasketItem'
import {AnimatePresence, motion} from 'framer-motion'
import { box, item, modal } from './motion.setings'
import { Product } from '../../models/entities'

export const Basket = (): JSX.Element => {

    const navigate = useNavigate()

    const {
        openStatus, 
        basketItems, 
        totalPrice, 
        isEmptyBasket,
        productQty,
        closeBasket, 
        deleteFromBasket, 
        changeCounter,
    } = useBasket()

    const basketBox = useRef<HTMLDivElement | null>(null)
    
    useClickOutside(basketBox, closeBasket)

    useEffect(() => {
        document.body.style.overflow = openStatus ? 'hidden' : 'visible'

        return () => {document.body.style.overflow = 'visible'}
        
    }, [openStatus])


    const handleClickBlueButton = () => {
        closeBasket()
        if(isEmptyBasket){
            return navigate(ROUTE.HOME)
        }
        navigate(ROUTE.ORDER)
    }

    const handleCkickName = (product: Product) => {
        navigate(ROUTE.PRODUCT+product.id)
        closeBasket()
    }

    return (
        <AnimatePresence>
            {
                openStatus && 
                <motion.div 
                    className={styles.container}
                    variants={modal}
                    initial='hidden'
                    animate='visible'
                    exit='hidden'
                >
                    <motion.div 
                        ref={basketBox}
                        className={styles.box}
                        variants={box}
                    >
                        <header className={clsx(styles.header, {
                            [styles.endline]: isEmptyBasket
                        })}>
                            <h4 className={styles. titleContainer}>
                                <span className={styles.title}>Кошик</span>
                                <span className={styles.counter}>{`(${productQty})`}</span>
                            </h4>
                            <button onClick={closeBasket}>
                                <AppIcon iconName='cross'/>
                            </button>
                        </header>
                                   
                        <div  
                            className={clsx(styles.content, {
                                    [styles.center]: isEmptyBasket
                                })}
                        >
                            {
                                !isEmptyBasket ?
                                basketItems.map((basketItem) => {
                                    const {product, qty, productId} = basketItem
                                    return (
                                    product &&
                                        <motion.div 
                                            key={productId}
                                            variants={item}
                                            layout = {true}
                                        >
                                            <BasketItem
                                                product={product}
                                                qty={qty}
                                                color={{color: product.color_value || '', name: product.color_name || ''}}
                                                size={product.size || ''}
                                                onClickDelete={deleteFromBasket}
                                                onClickName={handleCkickName}
                                                onChangeCounter={changeCounter}
                                            />
                                        </motion.div>
                                    )})
                                :
                                <EmptyBasket/>
                            }
                        </div>
                        
                        {
                            !isEmptyBasket &&
                            <div className={styles.totalPrice}>
                                <span>Загальна сума</span>   
                                <span>{formatNumber(totalPrice)} грн</span>   
                            </div>
                        }
                        <div className={styles.actions}>
                            <MainButton
                                title= {isEmptyBasket ? 'Повернутися на головну' : 'Оформити замовлення'}
                                color='blue'
                                onClick={handleClickBlueButton}
                            />
                            <MainButton
                                title='Продовжити покупки'
                                onClick={closeBasket}
                            />
                        </div>
                    </motion.div>
                </motion.div>
            }
        </AnimatePresence>
    )
} 