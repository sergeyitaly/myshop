import clsx from 'clsx'
import style from './Counter.module.scss'


interface CounterProps {
    value: number
    className?: string
    onReduce?: () => void
    onIncrement?: () => void
}

export const Counter = ({
    value,
    className,
    onIncrement,
    onReduce
}: CounterProps) => {
    return (
        <div className={clsx(style.container, className)}>
            <button
                onClick={onReduce}
            >-</button>
            <span>{value}</span>
            <button
                onClick={onIncrement}
            >+</button>
        </div>
    )
}