import clsx from 'clsx'
import { MapComponent } from '../MapComponent'
import { Skeleton } from '../Skeleton/Skeleton'
import style from './ProductVariants.module.scss'
import { ValueBoxSkeleton } from './ValueBox/ValueBoxSkeleton'

interface ProductVariantSkeletonProps {
    className?: string
}

export const ProductVariantSkeleton = ({
    className
}: ProductVariantSkeletonProps) => {
    return (
        <div 
            className={clsx(style.container, className)}
        >
            <Skeleton className={style.variant_name}/>
            <div className={style.contentСontainer}>
                <MapComponent
                    qty={3}
                    component={<ValueBoxSkeleton/>}
                />
            </div>
        </div>
    )
}