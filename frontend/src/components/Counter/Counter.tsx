import style from './Counter.module.scss'


interface CounterProps {
    value: number
    onReduce?: () => void
    onIncrement?: () => void
}

export const Counter = ({
    value,
    onIncrement,
    onReduce
}: CounterProps) => {
    return (
        <div className={style.container}>
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