import { useField } from "formik"
import styles from './FormikCheckBox.module.scss'
import clsx from "clsx"

interface FormikCheckBoxProps {
    className?: string
    name: string
} 


export const FormikCheckBox = ({
    className,
    ...props
}: FormikCheckBoxProps) => {

    const [field] = useField(props)

    return (
        <label className={clsx(styles.label, className) }>
            <input type="checkbox" {...field}/>
            <div className={styles.rectangle}>
                <span className={styles.point}/>
            </div>
        </label>
    )
}