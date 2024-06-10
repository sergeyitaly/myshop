import clsx from 'clsx'
import style from './ValueBox.module.scss'


interface ValueBoxProps {
    color?: string
    title?: string | number
    value: string 
    isActive?: boolean
    onClick?: (value: string) => void
}


export const ValueBox = ({
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
            className={clsx(style.box, {[style.active]: isActive})}
            style={{background: color}}
            onClick={handleClick}
        >
            {!!value &&<span>{title}</span>}
        </button>
    )
}