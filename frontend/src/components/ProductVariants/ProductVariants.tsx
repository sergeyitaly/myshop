import clsx from 'clsx'
import style from './ProductVariants.module.scss'
import { ReactNode } from 'react'

interface ProductVariantsProps {
    title: string
    className?: string
    value?: string
    children: ReactNode
}

export const ProductVariants = ({
    title,
    className,
    value,
    children
}: ProductVariantsProps) => {
    return (
        <div 
            className={clsx(style.container, className) }
        >
            <p>{title}: {value}</p>
            <div className={style.contentСontainer}>
                {children}
            </div>
        </div>
    )
}