import { ButtonHTMLAttributes, DetailedHTMLProps } from "react"
import styles from './TextButton.module.scss'
import clsx from "clsx"

interface TextButtonProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
    title: string
}

export const TextButton = ({
    title,
    ...props
}: TextButtonProps) => {
    return (
        <button
            {...props}
            className={clsx(styles.button, props.className)}
        >
            {title}
        </button>
    )
}