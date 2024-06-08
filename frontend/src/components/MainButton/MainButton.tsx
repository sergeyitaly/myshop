import { ButtonHTMLAttributes, DetailedHTMLProps } from 'react'
import clsx from 'clsx'
import style from './MainButton.module.scss'


interface MainButtonProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
    title: string
}

export const MainButton = ({
    title,
    className,
    ...props
}: MainButtonProps) => {
    return (
        <button 
            className={clsx(style.button, className)}
            {...props}
        >
            {title}
        </button>
    )
}