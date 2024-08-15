import { Product, ProductVariantsModel } from '../../../../models/entities'
import { DropDown } from '../DropDown/DropDown'
import { ProductControl } from '../ProductControl/ProductControl'
import styles from './ProductInfo.module.scss'

interface ProductInfoProps {
    product: Product
    discountPrice: number | null
    productVariants: ProductVariantsModel
    onChangeColor: (color: string) => void
    onChangeSize: (size: string) => void
}

export const ProductInfo = ({
    product,
    discountPrice,
    productVariants,
    onChangeColor,
    onChangeSize
}: ProductInfoProps) => {

    

    return (
        <div className={styles.container}>
            <div className={styles.productInfo}>
                <ProductControl 
                    discountPrice={discountPrice}
                    product={product}
                    variants={productVariants}
                    onChangeColor={onChangeColor}
                    onChangeSize={onChangeSize}
                />
                <div className={styles.description}>
                    <h3>Опис:</h3>
                    <p>{product.description ? product.description : 'опис товару поки що відсутній'}</p>
                </div>
            </div>

            {
                product.additional_fields &&
                product.additional_fields.map(({name, value}, index) => (
                    <DropDown
                        key = {index}
                        className={styles.applyDropdown}
                        changebleParam={product.id}
                        title={name}
                        content={value}
                    />
                ))
            }
        </div>
    )
}