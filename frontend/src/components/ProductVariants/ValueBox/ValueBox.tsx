import clsx from 'clsx'
import style from './ValueBox.module.scss'


interface ValueBoxProps {
    color?: string
    value?: string | number
    isActive?: boolean
}


export const ValueBox = ({
    color,
    value,
    isActive
}: ValueBoxProps) => {
    return (
        <div
            className={clsx(style.box, {[style.active]: isActive})}
            style={{background: color}}
        >
            {!!value &&<span>{value}</span>}
        </div>
    )
}