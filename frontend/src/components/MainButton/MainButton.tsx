import { ButtonHTMLAttributes, DetailedHTMLProps } from 'react'
import clsx from 'clsx'
import style from './MainButton.module.scss'


interface MainButtonProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
    title: string
    colored?: boolean
}

export const MainButton = ({
    title,
    className,
    colored,
    ...props
}: MainButtonProps) => {
    return (
        <button 
            className={clsx(style.button, {[style.coloredButton]: colored}, className)}
            {...props}
        >
            {title}
        </button>
    )
}