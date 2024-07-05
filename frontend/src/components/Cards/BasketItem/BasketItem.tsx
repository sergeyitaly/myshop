import { formatCurrency } from "../../../functions/formatCurrency"
import { formatNumber } from "../../../functions/formatNumber"
import { Product, ProductVariantsModel } from "../../../models/entities"
import { AvailableLable } from "../../AvailableLabel/AvailableLabel"
import { Counter } from "../../Counter/Counter"
import { ProductVariants } from "../../ProductVariants/ProductVariants"
import { ValueBox } from "../../ProductVariants/ValueBox/ValueBox"
import { IconButton } from "../../UI/IconButton/IconButton"
import styles from './BasketItem.module.scss'

interface BasketItemProps {
    product: Product
    qty: number
    variants: ProductVariantsModel
    onClickDelete: (product: Product) => void 
    onClickIncrement: (product: Product) => void 
    onClickDecrement: (product: Product) => void 
}


export const BasketItem = ({
    product,
    variants,
    qty,
    onClickDelete,
    onClickIncrement,
    onClickDecrement
}: BasketItemProps) => {

    const {photo, name, available, price, currency} = product

    const handleClickDelete = () => {
        onClickDelete && onClickDelete(product)
    }

    const handleClickIncrement = () => {
        onClickIncrement && onClickIncrement(product)
    }

    const handleClickDecrement = () => {
        onClickDecrement && onClickDecrement(product)
    }

    return (
        <div className={styles.container}>
            <div className={styles.imgWrapper}>
                <div className={styles.image}>
                    {photo && <img src={photo}/>}
                </div>
            </div>
            <div className={styles.info}>
                <div className={styles.header}>
                    <h4 className={styles.title}>{name}</h4>
                    <IconButton
                        className={styles.icon}
                        iconName="delete"
                        onClick={handleClickDelete}
                    />
                </div>
                <ProductVariants
                    className={styles.characteristic}
                    title="Колір"
                >
                    {
                        variants.colors.map(({color}) => (
                            <ValueBox
                                key={color}
                                value={color}
                                color={color}
                                isActive={color === product.color_value}
                            />
                        ))
                    }
                </ProductVariants>
                <div className={styles. counterBox}>
                    <ProductVariants
                        className={styles.characteristic}
                        title="Розмір"
                    >
                       {
                        variants.sizes.map((size) => (
                            <ValueBox
                                key={size}
                                value={size}
                                title={size}
                                isActive={size === product.size}
                            />
                        ))
                    }
                    </ProductVariants>
                    <Counter
                        className={styles.selfTop}
                        value={qty}
                        onIncrement={handleClickIncrement}
                        onReduce={handleClickDecrement}
                    />  
                </div>
                <AvailableLable
                    isAvailable = {available}
                />
                <div className={styles.control}>
                    <span>{formatNumber(price) } {formatCurrency(currency)}</span>
                </div>
            </div>
        </div> 
    ) 
}