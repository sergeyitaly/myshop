import { useField } from "formik"
import { DetailedHTMLProps, TextareaHTMLAttributes, useEffect } from "react"
import clsx from "clsx"
import styles from './FormikTextArea.module.scss'

interface FormikTextAreaProps extends DetailedHTMLProps<TextareaHTMLAttributes<HTMLTextAreaElement>, HTMLTextAreaElement> {
    name: string
}

export const FormikTextArea = ({
    className,
    ...props
}: FormikTextAreaProps) => {

    const [field, meta, helpers] = useField(props)

    console.log(meta.value);
    

    useEffect(() => {

        return () => {
            helpers.setValue('')
        }
    }, [helpers])


    return (
        <textarea className={clsx(styles.textaarea, className)} {...field} {...props}/>
    )
}