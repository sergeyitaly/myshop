import clsx from "clsx"
import { ProductVariantSkeleton } from "../../../ProductVariants/ProductVariantSkeleton"
import { Skeleton } from "../../../Skeleton/Skeleton"
import style from './ProductControl.module.scss'
import { AvailableLabelSkeleton } from "../../../AvailableLabel/AvailableLabelSkeleton"

export const ProductControlSkeleton = () => {
    return (
        <div className={style.container}>
            <Skeleton className={clsx(style.title, style.title_skeleton)}/>
            <Skeleton className={clsx(style.price, style.price_skeleton)}/>
            <AvailableLabelSkeleton/>
            <ProductVariantSkeleton 
                className={style.color}
            />
            <div className={style.sizeArea}>
                <ProductVariantSkeleton/>

            </div>
            <Skeleton className={clsx(style.add, style.button_skeleton) }/>
            <Skeleton className={clsx(style.buy, style.button_skeleton)}/>
        </div>
    )
}