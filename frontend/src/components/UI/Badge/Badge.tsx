import clsx from "clsx"
import styles from './Badge.module.scss'

interface BadgeProps {
    className?: string
    value: number
}

export const Badge = ({
    className,
    value
}: BadgeProps) => {
    return (
        <span className={clsx(styles.wrapper, className)}>
          {value}
        </span>
    )
}