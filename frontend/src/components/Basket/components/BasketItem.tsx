import { Product, ProductVariantsModel } from "../../../models/entities"
import { AvailableLable } from "../../AvailableLabel/AvailableLabel"
import { Counter } from "../../Counter/Counter"
import { ProductVariants } from "../../ProductVariants/ProductVariants"
import { ValueBox } from "../../ProductVariants/ValueBox/ValueBox"
import styles from './BasketItem.module.scss'

interface BasketItemProps {
    product: Product
    variants: ProductVariantsModel
}


export const BasketItem = ({
    product,
    variants
}: BasketItemProps) => {

    const {photo, name, available, price, currency} = product

    return (
        <div className={styles.container}>
            <div className={styles.image}>
                <img src={photo} />
            </div>
            <div className={styles.info}>
                <h4>{name}</h4>
                <h5>Срібло 925 проби </h5>
                <ProductVariants
                    title="Колір"
                >
                    {
                        variants.colors.map(({color}) => (
                            <ValueBox
                                key={color}
                                value={color}
                                color={color}
                                isActive={color === product.color}
                            />
                        ))
                    }
                </ProductVariants>
                <div className={styles. counterBox}>
                    <ProductVariants
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
                    value={10}
                    // onIncrement={handleIncrement}
                    // onReduce={handleDecrement}
                    />  
                </div>
                <AvailableLable
                    isAvailable = {available}
                />
                <span>{price} {currency}</span>
            </div>
        </div> 
    ) 
}