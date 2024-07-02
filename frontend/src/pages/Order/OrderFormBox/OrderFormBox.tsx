import { ReactNode } from "react"
import styles from './OrderFormBox.module.scss'

interface OrderFormBoxProps {
    title: string
    children: ReactNode
}

export const OrderFormBox = ({
    title,
    children,
}: OrderFormBoxProps) => {
    return (
        <div>
            <h2 className={styles.title}>{title}</h2>
            <>{children}</>
        </div>
    )
}