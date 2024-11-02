import { MapComponent } from '../../../MapComponent'
import { Skeleton } from '../../../Skeleton/Skeleton'
import { ProductControlSkeleton } from '../ProductControl/ProductControlSkeleton'
import styles from './ProductInfo.module.scss'

export const ProductInfoSkeleton = () => {
    return (
        <div className={styles.container}>
            <div className={styles.productInfo}>
                <ProductControlSkeleton/>
                <div>
                    <Skeleton className={styles.description_skeleton_header}/>
                    <MapComponent
                        qty={7}
                        component={<Skeleton
                            className={styles.description_skeleton_paragraph}
                        />}
                    />
                </div>
            </div>

            {/* {translatedAdditionalFields &&
                translatedAdditionalFields.map(({ name, value }, index) => (
                    <DropDown
                        key={index}
                        className={styles.applyDropdown}
                        changebleParam={product.id}
                        title={name}
                        content={value}
                    />
                ))} */}
        </div>
    )
}