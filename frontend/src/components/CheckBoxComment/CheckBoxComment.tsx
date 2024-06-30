import { DetailedHTMLProps, HTMLAttributes } from "react"
import clsx from "clsx"
import styles from './CheckBoxComment.module.scss'

interface CheckBoxCommentProps extends DetailedHTMLProps<HTMLAttributes<HTMLParagraphElement>, HTMLParagraphElement> {
    text: string
}

export const CheckBoxComment = ({
    text,
    className,
    ...props
}: CheckBoxCommentProps) => {
    return (
        <p className={clsx(styles.container, className)} {...props}>
            {text}
        </p>
    )
}