import { formatCurrency } from "../../../functions/formatCurrency"
import { formatNumber } from "../../../functions/formatNumber"
import { Color, Product } from "../../../models/entities"
import { AppImage } from "../../AppImage/AppImage"
import { AvailableLable } from "../../AvailableLabel/AvailableLabel"
import { Counter } from "../../Counter/Counter"
import { ProductVariants } from "../../ProductVariants/ProductVariants"
import { ValueBox } from "../../ProductVariants/ValueBox/ValueBox"
import { IconButton } from "../../UI/IconButton/IconButton"
import styles from './BasketItem.module.scss'

interface BasketItemProps {
    product: Product
    qty: number
    color: Color
    size: string
    onClickDelete: (product: Product) => void 
    onClickName?: (product: Product) => void
    onClickPhoto?: (product: Product) => void
    onChangeCounter?: (product: Product, qty: number) => void
}


export const BasketItem = ({
    product,
    color,
    size,
    qty,
    onClickDelete,
    onClickName,
    onClickPhoto,
    onChangeCounter
}: BasketItemProps) => {

    const {photo, name, available, price, currency} = product


    const handleClickDelete = () => {
        onClickDelete && onClickDelete(product)
    }

    const handleClickName = () => {
        onClickName && onClickName(product)
    }

    const handleClickPhoto = () => {
        onClickPhoto && onClickPhoto(product)
    } 
    
    const handleChangeCounter = (value: number) => {
        onChangeCounter && onChangeCounter(product, value)
    }


    return (
        <div className={styles.container}>
            <button 
                className={styles.imgWrapper}
                onClick={handleClickPhoto}
            >
                <AppImage
                    src={photo}
                    alt={name}
                />
            </button>
            <div className={styles.info}>
                <div className={styles.header}>
                    <h4 
                        className={styles.title}
                        onClick={handleClickName}
                    >{name}</h4>
                    <IconButton
                        className={styles.icon}
                        iconName="delete"
                        onClick={handleClickDelete}
                    />
                </div>
                <ProductVariants
                    className={styles.characteristic}
                    title="Колір"
                    value={color.name}
                >
                    <ValueBox
                        className={styles.noPointer}
                        value={color.color}
                        color={color.color}
                    />
                </ProductVariants>
                <div className={styles. counterBox}>
                    <ProductVariants
                        className={styles.characteristic}
                        title="Розмір"
                    >
                        <ValueBox
                            className={styles.noPointer}
                            key={size}
                            value={size}
                            title={size}
                            isActive
                        />
                    </ProductVariants>
                    <Counter
                        className={styles.selfTop}
                        value={qty}
                        onChangeCounter={handleChangeCounter}
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