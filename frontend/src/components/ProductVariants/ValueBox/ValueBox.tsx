import clsx from 'clsx'
import style from './ValueBox.module.scss'


interface ValueBoxProps {
    className?: string
    color?: string
    title?: string | number
    value: string 
    isActive?: boolean
    onClick?: (value: string) => void
}


export const ValueBox = ({
    className,
    color,
    title,
    value,
    isActive,
    onClick
}: ValueBoxProps) => {

    const handleClick = () => {
        onClick && onClick(value)
    }

    return (
        <button
            className={clsx(style.box, {[style.active]: isActive}, className)}
            style={{background: color}}
            onClick={handleClick}
        >
            {!!value &&<span>{title}</span>}
        </button>
    )
}