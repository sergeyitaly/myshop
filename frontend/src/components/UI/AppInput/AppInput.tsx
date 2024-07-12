import clsx from "clsx"
import styles from './AppInput.module.scss'
import { ChangeEvent, DetailedHTMLProps, FocusEvent, InputHTMLAttributes, useState } from "react"

interface AppInputProps extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement>{
    label: string
    error: boolean
    helperText?: string
}

export const AppInput = ({
    label,
    error,
    helperText,
    ...props
}: AppInputProps) => {

    const {onChange, onFocus, onBlur} = props

    const [active, setActive] = useState<boolean>(false)
    const [value, setValue] = useState<string | number>('')


    const handleFocus = (e: FocusEvent<HTMLInputElement>) => {
        setActive(true)
        onFocus && onFocus(e)
    }

    const handleBlur = (e: FocusEvent<HTMLInputElement>) => {
        setActive(false)
        onBlur && onBlur(e)
    }

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setValue(e.target.value)
        onChange && onChange(e)
    }

    return (
        <label className={clsx(styles.label, {
            [styles.error]: error
        })}>
            <input
                autoComplete="off"
                className={clsx(styles.input)} 
                {...props}
                onFocus={handleFocus}
                onChange={handleChange}
                onBlur={handleBlur}
            />
            <span className={clsx({[styles.activeSpan]: active || value})}>{label}</span>
            {error && <p className={styles.errorMessage}>{helperText}</p>}
        </label>
    )
}