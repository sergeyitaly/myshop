import { ChangeEvent } from "react"
import { AppInput } from "../../../components/UI/AppInput/AppInput"
import { MainButton } from "../../../components/UI/MainButton/MainButton"
import styles from './FeedbackModalForm.module.scss'
import { useFormik } from "formik"
import {object, string} from 'yup'
import { useAppTranslator } from "../../../hooks/useAppTranslator"



interface FeedbackModalFormProps {
    isLoading: boolean
    onSubmit: () => void
    onChange: (fieldName: string, value: string) => void
}

export const FeedbackModalForm = ({
    isLoading,
    onChange,
    onSubmit
}: FeedbackModalFormProps) => {

    const {t} = useAppTranslator()

    const validationSchema = object({
        email: string().email(t("error_email")),
    })

    const {
        handleChange: handleChangeFormik,
        handleSubmit,
        handleBlur,
        errors,
        touched
    } = useFormik({
        initialValues: {
            name: '',
            email: '',
            comment: ''
        },
        validationSchema: validationSchema,
        onSubmit: () => {
            onSubmit()
        },

    })

    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        handleChangeFormik(e)
        onChange(e.target.name, e.target.value)
    }

    return (
        <form 
            className={styles.modal}
            onSubmit={handleSubmit}
        >
            <h1>Залиште свої дані для зворотнього зв'язку</h1>
            <AppInput
                label="name"
                name="name"
                onChange={handleChange}
            />
            <AppInput
                name='email'
                label="email"
                error = {touched.email && !!errors.email}
                helperText={errors.email}
                onChange={handleChange}
                onBlur={handleBlur}
            />
            <textarea 
                name="comment"
                className={styles.textarea}
                placeholder="comment..."
                onChange={handleChange}
            />
            <MainButton
                color="blue"
                title={isLoading ? "Надсилаю..." : "Надіслати"}
                type="submit"
            />

        </form>
    )
}