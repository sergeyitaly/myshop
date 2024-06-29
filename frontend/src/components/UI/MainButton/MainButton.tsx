import { ButtonHTMLAttributes, DetailedHTMLProps } from 'react'
import clsx from 'clsx'
import style from './MainButton.module.scss'


interface MainButtonProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
    title: string
    color?: 'blue' | 'black'
}

export const MainButton = ({
    title,
    className,
    color,
    ...props
}: MainButtonProps) => {
    return (
        <button 
            className={clsx(
                style.button, 
                {
                    [style.blue]: color === 'blue',
                    [style.black]: color === 'black'
                }, className)}
            {...props}
        >
            {title}
        </button>
    )
}