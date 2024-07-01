import styles from './OrderInfo.module.scss'


interface OrderInfoProps {
    text: string
}

export const OrderInfo = ({
    text
}: OrderInfoProps) => {
    return (
        <p className={styles.container}>
            {text}
        </p>
    )
}