import style from './Counter.module.scss'


interface CounterProps {
    value: number
}

export const Counter = ({
    value
}: CounterProps) => {
    return (
        <div className={style.container}>
            <button>-</button>
            <span>{value}</span>
            <button>+</button>
        </div>
    )
}