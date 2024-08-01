import clsx from 'clsx'
import style from './Counter.module.scss'
import { ChangeEvent, useEffect, useState } from 'react'


interface CounterProps {
    value: number
    className?: string
    onChangeCounter?: (number: number) => void
}

export const Counter = ({
    value,
    className,
    onChangeCounter
}: CounterProps) => {

    const [val, setVal] = useState<number>(value)

    useEffect(() => {
        onChangeCounter && onChangeCounter(val)
    }, [val])

    useEffect(() => {
        setVal(value)
    }, [value])

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const v = +e.target.value
        if(!isNaN(v))
        setVal(v)
    }


    const handleReduce = () => {
        if(val > 1){
            setVal(val - 1)
            onChangeCounter && onChangeCounter(val - 1)
        }
    }

    const handleIncrement = () => {
        setVal(val + 1)
        onChangeCounter && onChangeCounter(val + 1)
    }

    return (
        <div className={clsx(style.container, className)}>
            <button
                onClick={handleReduce}
            >-</button>
            <input 
                value={val}
                onChange={handleChange}
            />
            <button
                onClick={handleIncrement}
            >+</button>
        </div>
    )
}