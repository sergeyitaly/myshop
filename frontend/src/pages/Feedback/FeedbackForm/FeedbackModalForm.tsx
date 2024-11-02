import { ChangeEvent } from "react";
import { AppInput } from "../../../components/UI/AppInput/AppInput";
import { MainButton } from "../../../components/UI/MainButton/MainButton";
import styles from './FeedbackModalForm.module.scss';
import { useFormik } from "formik";
import { object, string } from 'yup';
import { useAppTranslator } from "../../../hooks/useAppTranslator";

interface FeedbackModalFormProps {
    isLoading: boolean;
    onSubmit: (values: { name?: string; email?: string; comment?: string }) => Promise<void>; // Fields are optional
    onChange: (fieldName: string, value: string) => void;
    translatedLabels: {
        name: string;
        email: string;
        comment: string;
    };
}

export const FeedbackModalForm = ({
    isLoading,
    onChange,
    onSubmit,
    translatedLabels
}: FeedbackModalFormProps) => {

    const { t } = useAppTranslator();

    const validationSchema = object({
        email: string().email(t("error_email")), // Only email validation
        name: string(), // Optional field
        comment: string() // Optional field
    });

    const {
        handleChange: handleChangeFormik,
        handleSubmit,
        handleBlur,
        errors,
        touched,
    } = useFormik({
        initialValues: {
            name: '',
            email: '',
            comment: ''
        },
        validationSchema: validationSchema,
        onSubmit: (values) => {
            onSubmit(values); // Call the passed onSubmit function
        },
    });

    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        handleChangeFormik(e);
        onChange(e.target.name, e.target.value);
    };

    return (
        <form 
            className={styles.modal}
            onSubmit={handleSubmit}
        >
            <h1>Залиште свої дані для зворотнього зв'язку</h1>
            <AppInput
                label={translatedLabels.name} // Use translated labels
                name="name"
                onChange={handleChange}
            />
            <AppInput
                name='email'
                label={translatedLabels.email} // Use translated labels
                error={touched.email && !!errors.email}
                helperText={errors.email}
                onChange={handleChange}
                onBlur={handleBlur}
            />
            <textarea 
                name="comment"
                className={styles.textarea}
                placeholder={translatedLabels.comment} // Use translated labels
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
