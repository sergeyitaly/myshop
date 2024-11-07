import { AppInput } from "../../../components/UI/AppInput/AppInput";
import { MainButton } from "../../../components/UI/MainButton/MainButton";
import styles from './FeedbackModalForm.module.scss';
import { useFormik } from "formik";
import { object, string } from 'yup';
import { useAppTranslator } from "../../../hooks/useAppTranslator";
import { initialValues } from "./initialValue";

interface FeedbackModalFormProps {
    isLoading: boolean;
    onSubmit: (values: { name: string; email: string; comment: string }) => void
}

export const FeedbackModalForm = ({
    isLoading,
    onSubmit,
}: FeedbackModalFormProps) => {

    const { t } = useAppTranslator();

    const validationSchema = object({
        email: string().email(t("error_email")), // Only email validation
        name: string(), // Optional field
        comment: string() // Optional field
    });

    const {
        errors,
        touched,
        handleChange,
        handleSubmit,
        handleBlur,
    } = useFormik({
        initialValues,
        validationSchema: validationSchema,
        onSubmit: (values) => {
            onSubmit(values); // Call the passed onSubmit function
        },
    });

    


    return (
        <form 
            className={styles.modal}
            onSubmit={handleSubmit}
        >
            <h1>{t('left_data')}</h1>
            <AppInput
                label={t("name")} // Use translated labels
                name="name"
                onChange={handleChange}
            />
            <AppInput
                name='email'
                label={t('email')} // Use translated labels
                error={touched.email && !!errors.email}
                helperText={errors.email}
                onChange={handleChange}
                onBlur={handleBlur}
            />
            <textarea 
                name="comment"
                className={styles.textarea}
                placeholder={t("add_comment")} // Use translated labels
                onChange={handleChange}
            />
            <MainButton
                color="blue"
                title={isLoading ? `${t('sending')}...` : t('send')}
                type="submit"
            />
        </form>
    );
};
