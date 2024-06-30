import { useField } from "formik"
import { DetailedHTMLProps, TextareaHTMLAttributes, useEffect } from "react"
import styles from './FormikTextArea.module.scss'
import clsx from "clsx"

interface FormikTextAreaProps extends DetailedHTMLProps<TextareaHTMLAttributes<HTMLTextAreaElement>, HTMLTextAreaElement> {
    name: string
}

export const FormikTextArea = ({
    className,
    ...props
}: FormikTextAreaProps) => {

    const [field, _, helpers] = useField(props)

    useEffect(() => {

        return () => {
            helpers.setValue('')
        }
    }, [helpers])


    return (
        <textarea className={clsx(styles.textaarea, className)} {...field} {...props}/>
    )
}